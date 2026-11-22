"""
Oran Takip Sistemi
- Her 15 dakikada Sahadan'dan veri çeker
- Önceki oranlarla karşılaştırır
- Değişiklikleri Supabase'e kaydeder
- Telegram'a bildirim gönderir
"""

import time
import schedule
from datetime import datetime
from supabase_sync import get_supabase_client
from sahadan_api import fetch_sahadan_matches
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def send_telegram_notification(message):
    """Telegram'a bildirim gönder"""
    try:
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            print("Telegram bilgileri .env dosyasinda yok")
            return False
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(url, data=data, timeout=10)
        return response.status_code == 200
        
    except Exception as e:
        print(f"Telegram gonderim hatasi: {e}")
        return False

def calculate_change_percentage(old_value, new_value):
    """Yüzde değişim hesapla"""
    if old_value is None or old_value == 0:
        return 0
    return ((new_value - old_value) / old_value) * 100

def determine_change_direction(change_1, change_x, change_2):
    """Genel değişim yönünü belirle"""
    changes = [c for c in [change_1, change_x, change_2] if c is not None]
    if not changes:
        return 'none'
    
    positive = sum(1 for c in changes if c > 0)
    negative = sum(1 for c in changes if c < 0)
    
    if positive > negative:
        return 'up'
    elif negative > positive:
        return 'down'
    else:
        return 'mixed'

def check_odds_changes():
    """Ana fonksiyon - oran değişikliklerini kontrol et"""
    try:
        print("=" * 70)
        print(f"Oran kontrolu basladi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print("=" * 70)
        
        client = get_supabase_client()
        
        # ÖNCE: future_matches'te veri var mı kontrol et
        existing_matches_check = client.table('future_matches').select('id').limit(1).execute()
        
        if not existing_matches_check.data or len(existing_matches_check.data) == 0:
            print("⚠️ future_matches tablosu bos - kontrol atlanıyor")
            print("💡 Önce /yeniveri komutu ile veri çekin")
            print("=" * 70)
            return
        
        # 1. Sahadan'dan güncel maçları çek
        print("Sahadan'dan veri cekiliyor...")
        success, new_matches, error = fetch_sahadan_matches(days_ahead=2)
        
        if not success:
            print(f"Sahadan cekme hatasi: {error}")
            return
        
        print(f"{len(new_matches)} mac cekildi")
        
        # 2. Supabase'den mevcut maçları al
        print("Mevcut oranlar kontrol ediliyor...")
        existing_matches = client.table('future_matches').select('*').execute()
        
        # Mevcut maçları dictionary'e çevir (hızlı erişim için)
        existing_dict = {}
        for match in existing_matches.data:
            key = f"{match['home_team']}|{match['away_team']}|{match['datetime']}"
            existing_dict[key] = match
        
        print(f"Veritabaninda {len(existing_dict)} mac var")
        
        # 3. Değişiklikleri tespit et
        changes_detected = []
        
        for new_match in new_matches:
            key = f"{new_match['home_team']}|{new_match['away_team']}|{new_match['datetime']}"
            
            if key in existing_dict:
                existing = existing_dict[key]
                
                # Oranları karşılaştır
                old_1 = existing.get('odd_1')
                old_x = existing.get('odd_x')
                old_2 = existing.get('odd_2')
                
                new_1 = new_match.get('odd_1')
                new_x = new_match.get('odd_x')
                new_2 = new_match.get('odd_2')
                
                # None kontrolü
                if None in [old_1, old_x, old_2, new_1, new_x, new_2]:
                    continue
                
                # Değişiklik var mı?
                tolerance = 0.01  # ±0.01 tolerans
                if (abs(old_1 - new_1) > tolerance or 
                    abs(old_x - new_x) > tolerance or 
                    abs(old_2 - new_2) > tolerance):
                    
                    # 🔥 AKILLI FİLTRELER - Saçma değişiklikleri atla
                    
                    # 1. Çok yüksek oranları atla (>15) - placeholder olabilir
                    if any(odd > 15 for odd in [old_1, old_x, old_2, new_1, new_x, new_2]):
                        continue
                    
                    # 2. Çok düşük oranları atla (<1.01) - hata olabilir
                    if any(odd < 1.01 for odd in [old_1, old_x, old_2, new_1, new_x, new_2]):
                        continue
                    
                    # Değişim yüzdelerini hesapla (güncel için)
                    change_1 = calculate_change_percentage(old_1, new_1)
                    change_x = calculate_change_percentage(old_x, new_x)
                    change_2 = calculate_change_percentage(old_2, new_2)
                    
                    # 3. Aşırı değişimleri atla (max ±50% per odd)
                    if any(abs(change) > 50 for change in [change_1, change_x, change_2]):
                        continue
                    
                    # Toplam değişim
                    total_change = abs(change_1) + abs(change_x) + abs(change_2)
                    
                    # Yön belirle
                    direction = determine_change_direction(change_1, change_x, change_2)
                    
                    # Bu maç için daha önce değişiklik kaydedilmiş mi kontrol et
                    existing_change = client.table('odds_changes').select('*').eq(
                        'home_team', new_match['home_team']
                    ).eq('away_team', new_match['away_team']).eq(
                        'match_datetime', new_match['datetime']
                    ).execute()
                    
                    if existing_change.data and len(existing_change.data) > 0:
                        # Mevcut kayıt var - GÜNCELLE (ilk oranlar sabit kalır)
                        first_record = existing_change.data[0]
                        
                        # İlk oranlardan değişim hesapla
                        first_change_1 = calculate_change_percentage(first_record['first_odd_1'], new_1)
                        first_change_x = calculate_change_percentage(first_record['first_odd_x'], new_x)
                        first_change_2 = calculate_change_percentage(first_record['first_odd_2'], new_2)
                        first_total_change = abs(first_change_1) + abs(first_change_x) + abs(first_change_2)
                        first_direction = determine_change_direction(first_change_1, first_change_x, first_change_2)
                        
                        changes_detected.append({
                            'id': first_record['id'],
                            'match_datetime': new_match['datetime'],
                            'home_team': new_match['home_team'],
                            'away_team': new_match['away_team'],
                            'league': new_match.get('league'),
                            'first_odd_1': first_record['first_odd_1'],
                            'first_odd_x': first_record['first_odd_x'],
                            'first_odd_2': first_record['first_odd_2'],
                            'current_odd_1': new_1,
                            'current_odd_x': new_x,
                            'current_odd_2': new_2,
                            'change_1': round(first_change_1, 2),
                            'change_x': round(first_change_x, 2),
                            'change_2': round(first_change_2, 2),
                            'change_direction': first_direction,
                            'total_change': round(first_total_change, 2),
                            'is_update': True
                        })
                    else:
                        # İlk değişiklik - YENİ KAYIT
                        changes_detected.append({
                            'match_datetime': new_match['datetime'],
                            'home_team': new_match['home_team'],
                            'away_team': new_match['away_team'],
                            'league': new_match.get('league'),
                            'first_odd_1': old_1,
                            'first_odd_x': old_x,
                            'first_odd_2': old_2,
                            'current_odd_1': new_1,
                            'current_odd_x': new_x,
                            'current_odd_2': new_2,
                            'change_1': round(change_1, 2),
                            'change_x': round(change_x, 2),
                            'change_2': round(change_2, 2),
                            'change_direction': direction,
                            'total_change': round(total_change, 2),
                            'telegram_sent': False,
                            'is_update': False
                        })
                    
                    print(f"\nDegisiklik tespit edildi!")
                    print(f"   Mac: {new_match['home_team']} vs {new_match['away_team']}")
                    print(f"   MS1: {old_1} -> {new_1} ({change_1:+.1f}%)")
                    print(f"   MSX: {old_x} -> {new_x} ({change_x:+.1f}%)")
                    print(f"   MS2: {old_2} -> {new_2} ({change_2:+.1f}%)")
        
        # 4. Değişiklikleri kaydet
        if changes_detected:
            print(f"\n{len(changes_detected)} degisiklik kaydediliyor...")
            
            new_changes_count = 0
            updated_changes_count = 0
            
            for change in changes_detected:
                try:
                    if change.get('is_update'):
                        # Mevcut kaydı güncelle
                        client.table('odds_changes').update({
                            'current_odd_1': change['current_odd_1'],
                            'current_odd_x': change['current_odd_x'],
                            'current_odd_2': change['current_odd_2'],
                            'change_1': change['change_1'],
                            'change_x': change['change_x'],
                            'change_2': change['change_2'],
                            'change_direction': change['change_direction'],
                            'total_change': change['total_change'],
                            'last_updated_at': datetime.now().isoformat()
                        }).eq('id', change['id']).execute()
                        updated_changes_count += 1
                    else:
                        # Yeni kayıt oluştur
                        client.table('odds_changes').insert({
                            'match_datetime': change['match_datetime'],
                            'home_team': change['home_team'],
                            'away_team': change['away_team'],
                            'league': change['league'],
                            'first_odd_1': change['first_odd_1'],
                            'first_odd_x': change['first_odd_x'],
                            'first_odd_2': change['first_odd_2'],
                            'current_odd_1': change['current_odd_1'],
                            'current_odd_x': change['current_odd_x'],
                            'current_odd_2': change['current_odd_2'],
                            'change_1': change['change_1'],
                            'change_x': change['change_x'],
                            'change_2': change['change_2'],
                            'change_direction': change['change_direction'],
                            'total_change': change['total_change'],
                            'telegram_sent': False,
                            'first_detected_at': datetime.now().isoformat(),
                            'last_updated_at': datetime.now().isoformat()
                        }).execute()
                        new_changes_count += 1
                    
                    # Güncel oranları future_matches'te güncelle (her iki durumda da)
                    client.table('future_matches').update({
                        'odd_1': change['current_odd_1'],
                        'odd_x': change['current_odd_x'],
                        'odd_2': change['current_odd_2']
                    }).eq('home_team', change['home_team']).eq('away_team', change['away_team']).eq('datetime', change['match_datetime']).execute()
                    
                except Exception as e:
                    print(f"Kayit hatasi: {e}")
            
            print(f"Yeni: {new_changes_count}, Guncellenen: {updated_changes_count}")
            print(f"Guncel oranlar future_matches'te guncellendi")
            
            # 5. Telegram bildirimi gönder - TEK MESAJ TOPLU ÖZET
            if len(changes_detected) > 0:
                print(f"\nTelegram bildirimi gonderiliyor...")
                
                now = datetime.now().strftime('%d.%m.%Y %H:%M')
                message = f"""═══════════════════════════════
  ORAN DEGISIKLIKLERI TESPIT EDILDI
═══════════════════════════════

>> {len(changes_detected)} macta oran degisti

>> Guncel oranlarla analiz icin:
   https://betsmart-web.vercel.app/

>> Kontrol zamani: {now}

═══════════════════════════════"""
                
                try:
                    send_telegram_notification(message)
                    
                    # Tüm değişiklikleri telegram_sent = True yap
                    for change in changes_detected:
                        client.table('odds_changes').update({
                            'telegram_sent': True,
                            'telegram_sent_at': datetime.now().isoformat()
                        }).eq('home_team', change['home_team']).eq('away_team', change['away_team']).eq('match_datetime', change['match_datetime']).execute()
                    
                    print(f"   Bildirim gonderildi: {len(changes_detected)} mac")
                    
                except Exception as e:
                    print(f"   Telegram hatasi: {e}")
        else:
            print("\nOran degisikligi tespit edilmedi")
        
        print("=" * 70)
        print(f"Kontrol tamamlandi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print("=" * 70)
        
    except Exception as e:
        print(f"Genel hata: {e}")
        import traceback
        traceback.print_exc()

def run_scheduler():
    """Scheduler'ı başlat"""
    print("Oran Takip Sistemi Baslatildi")
    print(f"Her 10 dakikada bir calisacak")
    print(f"İlk kontrol 10 dakika sonra yapilacak")
    print(f"Baslangic: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print()
    
    # İlk kontrolü HEMEN YAPMA - /yeniveri komutu zaten ilk oranları kaydetti
    # 10 dakika sonra ilk kontrolü yap
    schedule.every(10).minutes.do(check_odds_changes)
    
    # Sonsuz döngü
    while True:
        schedule.run_pending()
        time.sleep(60)  # Her dakika kontrol et

if __name__ == '__main__':
    run_scheduler()

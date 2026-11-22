"""
Oran Takip Sistemi - Test (Tek seferlik çalışma)
"""
import sys
import os

# UTF-8 encoding zorla
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.append('C:\\Users\\worda\\Desktop\\BetSmart\\backend')

from datetime import datetime
from supabase_sync import get_supabase_client
from sahadan_api import fetch_sahadan_matches

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

def test_odds_tracker():
    """Test - tek seferlik kontrol"""
    try:
        print("=" * 70)
        print(f"🧪 TEST: Oran değişiklikleri kontrol ediliyor")
        print(f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print("=" * 70)
        
        client = get_supabase_client()
        
        # 1. Sahadan'dan güncel maçları çek
        print("\n📥 Sahadan'dan veri çekiliyor...")
        success, new_matches, error = fetch_sahadan_matches(days_ahead=2)
        
        if not success:
            print(f"❌ Hata: {error}")
            return
        
        print(f"✅ {len(new_matches)} maç çekildi")
        
        # 2. Supabase'den mevcut maçları al
        print("\n📊 Mevcut oranlar kontrol ediliyor...")
        existing_matches = client.table('future_matches').select('*').execute()
        
        existing_dict = {}
        for match in existing_matches.data:
            key = f"{match['home_team']}|{match['away_team']}|{match['datetime']}"
            existing_dict[key] = match
        
        print(f"📋 Veritabanında {len(existing_dict)} maç var")
        
        # 3. Değişiklikleri tespit et
        print("\n🔍 Değişiklikler aranıyor...")
        changes_detected = []
        
        for new_match in new_matches[:100]:  # İlk 100 maç (test için)
            key = f"{new_match['home_team']}|{new_match['away_team']}|{new_match['datetime']}"
            
            if key in existing_dict:
                existing = existing_dict[key]
                
                old_1 = existing.get('odd_1')
                old_x = existing.get('odd_x')
                old_2 = existing.get('odd_2')
                
                new_1 = new_match.get('odd_1')
                new_x = new_match.get('odd_x')
                new_2 = new_match.get('odd_2')
                
                if None in [old_1, old_x, old_2, new_1, new_x, new_2]:
                    continue
                
                tolerance = 0.01
                if (abs(old_1 - new_1) > tolerance or 
                    abs(old_x - new_x) > tolerance or 
                    abs(old_2 - new_2) > tolerance):
                    
                    # 🔥 AKILLI FİLTRELER
                    if any(odd > 15 for odd in [old_1, old_x, old_2, new_1, new_x, new_2]):
                        continue
                    if any(odd < 1.01 for odd in [old_1, old_x, old_2, new_1, new_x, new_2]):
                        continue
                    
                    change_1 = calculate_change_percentage(old_1, new_1)
                    change_x = calculate_change_percentage(old_x, new_x)
                    change_2 = calculate_change_percentage(old_2, new_2)
                    
                    if any(abs(change) > 100 for change in [change_1, change_x, change_2]):
                        continue
                    
                    total_change = abs(change_1) + abs(change_x) + abs(change_2)
                    direction = determine_change_direction(change_1, change_x, change_2)
                    
                    change_record = {
                        'match_datetime': new_match['datetime'],
                        'home_team': new_match['home_team'],
                        'away_team': new_match['away_team'],
                        'league': new_match.get('league'),
                        'old_odd_1': old_1,
                        'old_odd_x': old_x,
                        'old_odd_2': old_2,
                        'new_odd_1': new_1,
                        'new_odd_x': new_x,
                        'new_odd_2': new_2,
                        'change_1': round(change_1, 2),
                        'change_x': round(change_x, 2),
                        'change_2': round(change_2, 2),
                        'change_direction': direction,
                        'total_change': round(total_change, 2),
                        'telegram_sent': False
                    }
                    
                    changes_detected.append(change_record)
                    
                    print(f"\n🔔 Değişiklik #{len(changes_detected)}")
                    print(f"   {new_match['home_team']} vs {new_match['away_team']}")
                    print(f"   MS1: {old_1:.2f} → {new_1:.2f} ({change_1:+.1f}%)")
                    print(f"   MSX: {old_x:.2f} → {new_x:.2f} ({change_x:+.1f}%)")
                    print(f"   MS2: {old_2:.2f} → {new_2:.2f} ({change_2:+.1f}%)")
                    print(f"   Toplam değişim: {total_change:.1f}%")
        
        # 4. Kaydet
        if changes_detected:
            print(f"\n💾 {len(changes_detected)} değişiklik kaydediliyor...")
            
            success_count = 0
            for change in changes_detected:
                try:
                    client.table('odds_changes').insert(change).execute()
                    success_count += 1
                except Exception as e:
                    print(f"❌ Kayıt hatası: {e}")
            
            print(f"✅ {success_count}/{len(changes_detected)} değişiklik kaydedildi")
        else:
            print("\n✅ Oran değişikliği tespit edilmedi")
        
        print("\n" + "=" * 70)
        print("✅ Test tamamlandı")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_odds_tracker()

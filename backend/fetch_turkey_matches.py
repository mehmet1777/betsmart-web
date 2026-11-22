"""
Türkiye Ligi Maçlarını Çek - RapidAPI
"""

import requests
import json
from datetime import datetime

API_KEY = "66169584d0msh7057db92927118cp13bd3ejsn55faa1294dce"
API_HOST = "free-api-live-football-data.p.rapidapi.com"

def fetch_turkey_matches(date_str, show_details=False):
    """Türkiye ligi maçlarını çek"""
    
    headers = {
        "X-RapidAPI-Key": API_KEY,
        "X-RapidAPI-Host": API_HOST
    }
    
    if show_details:
        print("=" * 70)
        print(f"🇹🇷 TÜRKİYE LİGİ MAÇLARI - {date_str}")
        print("=" * 70)
    
    try:
        # Tarih formatı: YYYYMMDD
        date_param = date_str.replace("-", "")
        
        response = requests.get(
            f"https://{API_HOST}/football-get-matches-by-date",
            headers=headers,
            params={"date": date_param},
            timeout=10
        )
        
        print(f"\n📡 API Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Maçları çıkar
            matches = data.get('response', {}).get('matches', [])
            
            if show_details:
                print(f"✅ Toplam {len(matches)} maç bulundu\n")
            
            if not matches:
                if show_details:
                    print("⚠️ Bugün hiç maç yok")
                return []
            
            # Türk takımları listesi
            turkish_teams = [
                'galatasaray', 'fenerbahçe', 'fenerbahce', 'beşiktaş', 'besiktas',
                'trabzonspor', 'başakşehir', 'basaksehir', 'kasımpaşa', 'kasimpasa',
                'sivasspor', 'alanyaspor', 'konyaspor', 'gaziantep', 'antalyaspor',
                'kayserispor', 'samsunspor', 'rizespor', 'hatayspor', 'adana demirspor'
            ]
            
            # Türkiye maçlarını filtrele
            turkey_matches = []
            turkey_league_ids = set()
            
            if show_details:
                print("🔍 Türk takımları aranıyor...\n")
            
            for match in matches:
                home = match.get('home', {}).get('name', '').lower()
                away = match.get('away', {}).get('name', '').lower()
                
                # Türk takımı var mı kontrol et
                is_turkish = False
                for team in turkish_teams:
                    if team in home or team in away:
                        is_turkish = True
                        break
                
                if is_turkish:
                    turkey_matches.append(match)
                    league_id = match.get('leagueId')
                    if league_id:
                        turkey_league_ids.add(league_id)
                    
                    if show_details:
                        # Maçı yazdır
                        home_name = match.get('home', {}).get('name', 'Unknown')
                        away_name = match.get('away', {}).get('name', 'Unknown')
                        time = match.get('time', 'Unknown')
                        
                        print(f"🇹🇷 {home_name} vs {away_name}")
                        print(f"   ⏰ {time}")
                        print(f"   🏆 League ID: {league_id}")
                        print()
            
            # Sonuç
            if show_details:
                print("=" * 70)
                print(f"📊 SONUÇ")
                print("=" * 70)
                print(f"✅ {len(turkey_matches)} Türkiye ligi maçı bulundu")
                
                if turkey_league_ids:
                    print(f"🏆 Türkiye Ligi ID'leri: {sorted(turkey_league_ids)}")
            
            return turkey_matches
            
        else:
            print(f"❌ API Hatası: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return []
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        return []

def main():
    """Ana fonksiyon"""
    
    # Bugün
    today = datetime.now().strftime("%Y-%m-%d")
    
    print("🎯 Hangi tarihi kontrol etmek istersin?")
    print("1. Bugün (2026-11-09)")
    print("2. Dün (2026-11-08)")
    print("3. 3 gün önce (2026-11-06)")
    print("4. Geçen hafta sonu (2026-11-02)")
    
    # Otomatik olarak son 7 günü dene
    from datetime import timedelta
    
    dates_to_check = [
        (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(7)
    ]
    
    print("\n🔄 Son 7 günü kontrol ediyorum...")
    print("=" * 70)
    
    all_turkey_matches = []
    
    for date_str in dates_to_check:
        print(f"\n📅 {date_str} kontrol ediliyor...")
        matches = fetch_turkey_matches(date_str)
        
        if matches:
            all_turkey_matches.extend(matches)
            print(f"   ✅ {len(matches)} Türkiye maçı bulundu!")
        else:
            print(f"   ⚠️ Türkiye maçı yok")
    
    # Özet
    print("\n" + "=" * 70)
    print(f"📊 SON 7 GÜN ÖZET")
    print("=" * 70)
    print(f"✅ Toplam {len(all_turkey_matches)} Türkiye maçı bulundu")
    
    if all_turkey_matches:
        # JSON'a kaydet
        import os
        os.makedirs("data", exist_ok=True)
        
        with open("data/turkey_matches_last_7_days.json", 'w', encoding='utf-8') as f:
            json.dump({
                'date_range': f"{dates_to_check[-1]} - {dates_to_check[0]}",
                'match_count': len(all_turkey_matches),
                'matches': all_turkey_matches
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 data/turkey_matches_last_7_days.json dosyasına kaydedildi")
        
        # Ligleri göster
        league_ids = set(m.get('leagueId') for m in all_turkey_matches)
        print(f"\n🏆 Bulunan Lig ID'leri: {sorted(league_ids)}")
    
    print("\n" + "=" * 70)
    print("✅ İşlem tamamlandı!")
    print("=" * 70)

if __name__ == "__main__":
    main()

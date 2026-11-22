"""
Sahadan API'nin stabilitesini test et - API URL değişiyor mu, sadece tarih mi değişiyor?
"""
import requests
from datetime import datetime, timedelta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.sahadan.com/'
}

# Bugün, yarın, 3 gün sonra için test
test_dates = []
for days in range(5):  # 5 gün test edelim
    date = datetime.now() + timedelta(days=days)
    test_dates.append(date)

print("=" * 70)
print("SAHADAN API STABILITY TEST")
print("=" * 70)
print()

for test_date in test_dates:
    date_iso = test_date.strftime('%Y-%m-%d')
    date_display = test_date.strftime('%d.%m.%Y (%A)')
    
    # API URL
    url = (
        f"https://www.sahadan.com/api/index/betting-service-bulletin-soccer"
        f"?a=bs"
        f"&e=bsbp"
        f"&u=soccer"
        f"&application=mackolik.com"
        f"&language=tr"
        f"&country=tr"
        f"&date={date_iso}"
    )
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            soccer = data.get('data', {}).get('soccer', [])
            
            # İlk 3 ligin time field'ını kontrol et
            total_matches = sum(len(league.get('matches', [])) for league in soccer)
            
            print(f"{date_display}")
            print(f"  Status: {response.status_code} OK")
            print(f"  Leagues: {len(soccer)}")
            print(f"  Matches: {total_matches}")
            
            if len(soccer) >= 3:
                print(f"  Sample league times:")
                for i, league in enumerate(soccer[:3]):
                    league_time = league.get('time', 'N/A')
                    league_name = league.get('title', 'Unknown')
                    print(f"    - {league_name}: {league_time}")
            print()
        else:
            print(f"{date_display}")
            print(f"  Status: {response.status_code} ERROR")
            print(f"  Response: {response.text[:200]}")
            print()
            
    except Exception as e:
        print(f"{date_display}")
        print(f"  ERROR: {e}")
        print()

print("=" * 70)
print("SONUÇ:")
print("  Eğer tüm tarihler 200 OK dönüyorsa → API stabil, sadece date parametresi değişiyor")
print("  Eğer bazı tarihler hata dönüyorsa → API değişken, sınırlamalar var")
print("=" * 70)

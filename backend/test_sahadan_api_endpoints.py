"""
Sahadan API farklı endpoint'leri test et
"""
import requests
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.sahadan.com/'
}

tomorrow_iso = (datetime.now().replace(day=22)).strftime('%Y-%m-%d')

# Farklı endpoint varyasyonlarını test et
endpoints = [
    # 1. Kullandığımız endpoint (çalışıyor)
    {
        "name": "Mevcut (betting-service-bulletin-soccer)",
        "url": f"https://www.sahadan.com/api/index/betting-service-bulletin-soccer?a=bs&e=bsbp&u=soccer&application=mackolik.com&language=tr&country=tr&date={tomorrow_iso}"
    },
    # 2. Alternatif - iddaa-program (web sitesindeki)
    {
        "name": "İddaa Program (web sitesi)",
        "url": f"https://www.sahadan.com/api/iddaa-program/soccer?date={tomorrow_iso}"
    },
    # 3. Alternatif - iddaa-program tomorrow
    {
        "name": "İddaa Program /tomorrow",
        "url": "https://www.sahadan.com/api/iddaa-program/soccer/tomorrow"
    },
    # 4. Tarih parametresi olmadan
    {
        "name": "Betting service (tarih yok)",
        "url": "https://www.sahadan.com/api/index/betting-service-bulletin-soccer?a=bs&e=bsbp&u=soccer&application=mackolik.com&language=tr&country=tr"
    },
    # 5. Basit endpoint
    {
        "name": "İddaa Program (tarih yok)",
        "url": "https://www.sahadan.com/api/iddaa-program/soccer"
    }
]

print("=" * 70)
print("SAHADAN API ENDPOINTS TEST")
print("=" * 70)
print(f"Test tarihi: {tomorrow_iso}")
print()

for endpoint in endpoints:
    print(f"[{endpoint['name']}]")
    print(f"URL: {endpoint['url'][:80]}...")
    
    try:
        response = requests.get(endpoint['url'], headers=headers, timeout=10)
        
        if response.status_code == 200:
            try:
                data = response.json()
                soccer = data.get('data', {}).get('soccer', [])
                
                if soccer:
                    total_matches = sum(len(league.get('matches', [])) for league in soccer)
                    print(f"✓ Status: 200 OK")
                    print(f"  Leagues: {len(soccer)}, Matches: {total_matches}")
                    
                    # İlk lig örneği
                    first = soccer[0]
                    print(f"  First: {first.get('title')} (time: {first.get('time')})")
                else:
                    print(f"✓ Status: 200 OK ama data.soccer boş")
                    print(f"  Response keys: {list(data.keys())}")
            except Exception as e:
                print(f"✓ Status: 200 OK ama JSON parse hatası: {e}")
        else:
            print(f"✗ Status: {response.status_code}")
            
    except Exception as e:
        print(f"✗ ERROR: {e}")
    
    print()

print("=" * 70)
print("SONUÇ:")
print("  - Hangi endpoint'ler çalışıyor?")
print("  - Tarih parametresi değişince endpoint aynı kalıyor mu?")
print("=" * 70)

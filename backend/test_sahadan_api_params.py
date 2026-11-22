"""
Sahadan API parametrelerini test et - hangileri zorunlu, hangileri opsiyonel?
"""
import requests
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.sahadan.com/'
}

tomorrow_iso = "2026-11-22"

# Farklı parametre kombinasyonları
test_cases = [
    {
        "name": "Tam hali (tüm parametreler)",
        "params": "?a=bs&e=bsbp&u=soccer&application=mackolik.com&language=tr&country=tr&date=" + tomorrow_iso
    },
    {
        "name": "Sadece date",
        "params": "?date=" + tomorrow_iso
    },
    {
        "name": "date + application",
        "params": "?application=mackolik.com&date=" + tomorrow_iso
    },
    {
        "name": "date + language + country",
        "params": "?language=tr&country=tr&date=" + tomorrow_iso
    },
    {
        "name": "a,e,u + date",
        "params": "?a=bs&e=bsbp&u=soccer&date=" + tomorrow_iso
    },
    {
        "name": "Parametresiz (base URL)",
        "params": ""
    }
]

base_url = "https://www.sahadan.com/api/index/betting-service-bulletin-soccer"

print("=" * 70)
print("SAHADAN API PARAMETRE TEST")
print("=" * 70)
print()

for test in test_cases:
    url = base_url + test['params']
    print(f"[{test['name']}]")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            try:
                data = response.json()
                soccer = data.get('data', {}).get('soccer', [])
                
                if soccer:
                    total_matches = sum(len(league.get('matches', [])) for league in soccer)
                    print(f"✓ ÇALIŞIYOR")
                    print(f"  Leagues: {len(soccer)}, Matches: {total_matches}")
                else:
                    print(f"✗ 200 OK ama data boş")
            except Exception as e:
                print(f"✗ JSON hatası: {e}")
        else:
            print(f"✗ Status: {response.status_code}")
            
    except requests.exceptions.Timeout:
        print(f"✗ Timeout (15 saniye)")
    except Exception as e:
        print(f"✗ ERROR: {str(e)[:50]}")
    
    print()

print("=" * 70)
print("SONUÇ:")
print("  Hangi parametre kombinasyonu çalışıyor?")
print("  → Minimum gerekli parametreleri belirleyebiliriz")
print("=" * 70)

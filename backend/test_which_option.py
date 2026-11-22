"""
Sahadan API - options[0] ve options[1] ikisini de çek, karşılaştır
"""
import requests
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json',
    'Referer': 'https://www.sahadan.com/'
}

today = datetime.now().strftime('%Y-%m-%d')
url = f"https://www.sahadan.com/api/index/betting-service-bulletin-soccer?a=bs&e=bsbp&u=soccer&application=mackolik.com&language=tr&country=tr&date={today}"

print("SAHADAN - OPTIONS[0] vs OPTIONS[1] KARSILASTIRMA")
print("="*80)

response = requests.get(url, headers=headers, timeout=30)
data = response.json()

soccer_data = data.get('data', {}).get('soccer', [])

# İlk maçı bul
for league_group in soccer_data[:20]:
    matches = league_group.get('matches', [])
    
    if not matches:
        continue
    
    match = matches[0]
    home = match.get('team_A', '')
    away = match.get('team_B', '')
    
    markets = match.get('markets', [])
    
    for market in markets:
        if market.get('i') == 1:  # MS
            options = market.get('o', [])
            
            if len(options) >= 2:
                print(f"\nMAC: {home} vs {away}")
                print("-"*80)
                
                # OPTIONS[0]
                outcomes_0 = options[0].get('l', [])
                bookmaker_0 = options[0].get('b', '?')
                
                if len(outcomes_0) >= 3:
                    odd1_0 = outcomes_0[0].get('v', '-')
                    oddx_0 = outcomes_0[1].get('v', '-')
                    odd2_0 = outcomes_0[2].get('v', '-')
                    
                    print(f"OPTIONS[0] (Bookmaker ID: {bookmaker_0}):")
                    print(f"  1={odd1_0}, X={oddx_0}, 2={odd2_0}")
                
                # OPTIONS[1]
                outcomes_1 = options[1].get('l', [])
                bookmaker_1 = options[1].get('b', '?')
                
                if len(outcomes_1) >= 3:
                    odd1_1 = outcomes_1[0].get('v', '-')
                    oddx_1 = outcomes_1[1].get('v', '-')
                    odd2_1 = outcomes_1[2].get('v', '-')
                    
                    print(f"OPTIONS[1] (Bookmaker ID: {bookmaker_1}):")
                    print(f"  1={odd1_1}, X={oddx_1}, 2={odd2_1}")
                
                # Karşılaştır
                try:
                    diff_1 = float(odd1_1) - float(odd1_0)
                    diff_x = float(oddx_1) - float(oddx_0)
                    diff_2 = float(odd2_1) - float(odd2_0)
                    
                    print(f"\nFARK (OPTIONS[1] - OPTIONS[0]):")
                    print(f"  1: {diff_1:+.2f}, X: {diff_x:+.2f}, 2: {diff_2:+.2f}")
                    
                    if diff_1 > 0 and diff_x > 0 and diff_2 > 0:
                        print(f"\n  SONUC: OPTIONS[1] DAHA YUKSEK -> OPTIONS[1] = OLEY")
                        print(f"         OPTIONS[0] = NESINE")
                    else:
                        print(f"\n  SONUC: OPTIONS[0] DAHA YUKSEK -> OPTIONS[0] = OLEY")
                        print(f"         OPTIONS[1] = NESINE")
                        
                except:
                    pass
                
                # İlk maçı gösterdikten sonra dur
                break
    
    if home and away:
        break

print("\n" + "="*80)
print("SAHADAN_API.PY'DE SU AN:")
print("  outcomes = options[0].get('l', [])")
print("\nDEGISTIRME ONERILERI:")
print("  NESINE istiyorsan: options[0] kullan (dusuk oranlar)")
print("  OLEY istiyorsan: options[1] kullan (yuksek oranlar)")

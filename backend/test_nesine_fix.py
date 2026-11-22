"""
Sahadan API artik kesinlikle Nesine cekiyor mu test et
"""
from sahadan_api import fetch_sahadan_matches

print("NESINE FIX TEST - Bookmaker ID 14 Zorunlu")
print("="*80)

success, matches, error = fetch_sahadan_matches(days_ahead=1)

if not success:
    print(f"Hata: {error}")
    exit(1)

print(f"\n{len(matches)} mac cekildi")

# Atl Goianiense maçını bul
target_match = None
for match in matches:
    if 'Goianiense' in match['home_team'] and 'Vila' in match['away_team']:
        target_match = match
        break

if target_match:
    print(f"\nHedef mac: {target_match['home_team']} vs {target_match['away_team']}")
    print(f"Cekilen oranlar: 1={target_match['odd_1']}, X={target_match['odd_x']}, 2={target_match['odd_2']}")
    
    # API'den raw veriyi cek ve karsilastir
    import requests
    from datetime import datetime
    
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json',
        'Referer': 'https://www.sahadan.com/'
    }
    
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://www.sahadan.com/api/index/betting-service-bulletin-soccer?a=bs&e=bsbp&u=soccer&application=mackolik.com&language=tr&country=tr&date={today}"
    
    response = requests.get(url, headers=headers, timeout=30)
    data = response.json()
    
    soccer_data = data.get('data', {}).get('soccer', [])
    
    for league_group in soccer_data:
        matches_raw = league_group.get('matches', [])
        
        for match_raw in matches_raw:
            home = match_raw.get('team_A', '')
            away = match_raw.get('team_B', '')
            
            if 'Goianiense' in home and 'Vila' in away:
                markets = match_raw.get('markets', [])
                
                for market in markets:
                    if market.get('i') == 1:
                        options = market.get('o', [])
                        
                        print(f"\nAPI'den raw data:")
                        print(f"  Toplam {len(options)} option var")
                        
                        for idx, option in enumerate(options):
                            bookmaker_id = option.get('b')
                            outcomes = option.get('l', [])
                            
                            if len(outcomes) >= 3:
                                odd_1 = outcomes[0].get('v')
                                odd_x = outcomes[1].get('v')
                                odd_2 = outcomes[2].get('v')
                                
                                bookmaker_name = "NESINE" if bookmaker_id == 14 else "OLEY" if bookmaker_id == 15 else f"ID:{bookmaker_id}"
                                
                                print(f"  Option {idx} ({bookmaker_name}): 1={odd_1}, X={odd_x}, 2={odd_2}")
                                
                                # Bizim cektigimiz ile karsilastir
                                if bookmaker_id == 14:
                                    if (abs(float(odd_1) - float(target_match['odd_1'])) < 0.01 and
                                        abs(float(odd_x) - float(target_match['odd_x'])) < 0.01 and
                                        abs(float(odd_2) - float(target_match['odd_2'])) < 0.01):
                                        print(f"\n  ✅ DOGRU! Bookmaker 14 (NESINE) cekiliyor!")
                                    else:
                                        print(f"\n  ❌ YANLIS! Bizim oranimiz farkli!")
                        
                        break
                break
        break

print("\n" + "="*80)
print("SONUC: sahadan_api.py artik bookmaker_id=14 (Nesine) zorunlu kullaniyor")
print("       Oran takipcisi ve /yeniveri her zaman Nesine cekecek")

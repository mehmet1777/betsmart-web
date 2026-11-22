"""
Sahadan API tutarlılığını test et
Aynı maçı 5 kez çek, oranlar değişiyor mu?
"""
import requests
import time
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json',
    'Referer': 'https://www.sahadan.com/'
}

today = datetime.now().strftime('%Y-%m-%d')
url = f"https://www.sahadan.com/api/index/betting-service-bulletin-soccer?a=bs&e=bsbp&u=soccer&application=mackolik.com&language=tr&country=tr&date={today}"

print("SAHADAN API TUTARLILIK TESTI")
print("Ayni mac 5 kez cekiliyor, oranlar degisiyor mu?")
print("="*80)

target_match = None
target_home = "Atl Goianiense"
target_away = "Vila Nova"

results = []

for attempt in range(5):
    print(f"\nDENEME #{attempt + 1}:")
    print("-"*80)
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        data = response.json()
        
        soccer_data = data.get('data', {}).get('soccer', [])
        
        # Hedef maçı bul
        found = False
        for league_group in soccer_data:
            matches = league_group.get('matches', [])
            
            for match in matches:
                home = match.get('team_A', '')
                away = match.get('team_B', '')
                
                if target_home in home and target_away in away:
                    # MS market bul
                    markets = match.get('markets', [])
                    
                    for market in markets:
                        if market.get('i') == 1:  # MS
                            options = market.get('o', [])
                            
                            print(f"Mac: {home} vs {away}")
                            print(f"Options sayisi: {len(options)}")
                            
                            # Her option'ı göster
                            option_data = []
                            for idx, option in enumerate(options):
                                bookmaker_id = option.get('b', '?')
                                outcomes = option.get('l', [])
                                
                                if len(outcomes) >= 3:
                                    odd_1 = outcomes[0].get('v', '-')
                                    odd_x = outcomes[1].get('v', '-')
                                    odd_2 = outcomes[2].get('v', '-')
                                    
                                    print(f"  Option {idx} (Bookmaker {bookmaker_id}): 1={odd_1}, X={odd_x}, 2={odd_2}")
                                    
                                    option_data.append({
                                        'bookmaker_id': bookmaker_id,
                                        'odd_1': odd_1,
                                        'odd_x': odd_x,
                                        'odd_2': odd_2
                                    })
                            
                            results.append({
                                'attempt': attempt + 1,
                                'options': option_data
                            })
                            
                            found = True
                            break
                    
                    if found:
                        break
            
            if found:
                break
        
        if not found:
            print(f"Mac bulunamadi")
        
        # 2 saniye bekle
        if attempt < 4:
            time.sleep(2)
            
    except Exception as e:
        print(f"Hata: {e}")

# Analiz
print("\n" + "="*80)
print("ANALIZ:")
print("="*80)

if len(results) >= 2:
    # İlk ve son denemeyi karşılaştır
    first = results[0]
    last = results[-1]
    
    print(f"\nILK DENEME:")
    for opt in first['options']:
        print(f"  Bookmaker {opt['bookmaker_id']}: 1={opt['odd_1']}, X={opt['odd_x']}, 2={opt['odd_2']}")
    
    print(f"\nSON DENEME:")
    for opt in last['options']:
        print(f"  Bookmaker {opt['bookmaker_id']}: 1={opt['odd_1']}, X={opt['odd_x']}, 2={opt['odd_2']}")
    
    # Options sayısı aynı mı?
    if len(first['options']) != len(last['options']):
        print(f"\n⚠️  OPTIONS SAYISI DEGISTI!")
        print(f"   Ilk: {len(first['options'])} options")
        print(f"   Son: {len(last['options'])} options")
        print(f"   >> Sahadan API bazen tek, bazen cift option donduruyor!")
    else:
        print(f"\n✅ OPTIONS SAYISI SABIT: {len(first['options'])} options")
    
    # Bookmaker ID'leri aynı mı?
    first_ids = [opt['bookmaker_id'] for opt in first['options']]
    last_ids = [opt['bookmaker_id'] for opt in last['options']]
    
    if first_ids != last_ids:
        print(f"\n⚠️  BOOKMAKER ID'LER DEGISTI!")
        print(f"   Ilk: {first_ids}")
        print(f"   Son: {last_ids}")
        print(f"   >> API her seferinde farkli bookmaker donduruyor!")
    else:
        print(f"\n✅ BOOKMAKER ID'LER SABIT: {first_ids}")
    
    # Oranlar değişti mi?
    if len(first['options']) > 0 and len(last['options']) > 0:
        first_opt = first['options'][0]
        last_opt = last['options'][0]
        
        if (first_opt['odd_1'] != last_opt['odd_1'] or 
            first_opt['odd_x'] != last_opt['odd_x'] or 
            first_opt['odd_2'] != last_opt['odd_2']):
            print(f"\n⚠️  OPTIONS[0] ORANLARI DEGISTI!")
            print(f"   >> Sahadan API tutarsiz donderim yapiyor!")
        else:
            print(f"\n✅ OPTIONS[0] ORANLARI SABIT")

print("\n" + "="*80)
print("SONUC:")
print("  Eger options sayisi veya bookmaker ID degisiyorsa:")
print("  >> sahadan_api.py'de SABIT BOOKMAKER ID kullan (14 = Nesine)")
print("  >> options[0] yerine bookmaker_id=14 olan option'i sec")

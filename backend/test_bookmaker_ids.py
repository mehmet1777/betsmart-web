"""
Sahadan API - Bookmaker ID'lerini tespit et
"""
import requests
import json
from datetime import datetime

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json',
    'Referer': 'https://www.sahadan.com/'
}

today = datetime.now().strftime('%Y-%m-%d')

url = f"https://www.sahadan.com/api/index/betting-service-bulletin-soccer?a=bs&e=bsbp&u=soccer&application=mackolik.com&language=tr&country=tr&date={today}"

print("BOOKMAKER ID TESTI")
print("="*60)

response = requests.get(url, headers=headers, timeout=30)
data = response.json()

# Türkiye liglerini bul
soccer_data = data.get('data', {}).get('soccer', [])

bookmaker_ids = set()

print(f"Toplam lig: {len(soccer_data)}\n")

# İlk 50 ligi tara
for league_group in soccer_data[:50]:
    league_name = league_group.get('title', '')
    
    # Sadece Türkiye liglerini göster (veya popüler ligleri)
    if 'TÜRK' not in league_name.upper() and 'TURKEY' not in league_name.upper():
        continue
    
    matches = league_group.get('matches', [])
    
    if not matches:
        continue
    
    print(f"\nLIG: {league_name}")
    print(f"Maç sayısı: {len(matches)}")
    
    # İlk maçı incele
    match = matches[0]
    home = match.get('team_A', '')
    away = match.get('team_B', '')
    
    print(f"Maç: {home} vs {away}\n")
    
    markets = match.get('markets', [])
    
    for market in markets:
        if market.get('i') == 1:  # MS
            options = market.get('o', [])
            
            print(f"  MS Market - {len(options)} option:")
            
            for opt in options:
                b_id = opt.get('b')
                bookmaker_ids.add(b_id)
                
                outcomes = opt.get('l', [])
                if outcomes:
                    odd_1 = outcomes[0].get('v', '-')
                    odd_x = outcomes[1].get('v', '-') if len(outcomes) > 1 else '-'
                    odd_2 = outcomes[2].get('v', '-') if len(outcomes) > 2 else '-'
                    
                    print(f"    Bookmaker ID {b_id}: 1={odd_1}, X={odd_x}, 2={odd_2}")
            
            break
    
    break  # Sadece ilk Türkiye ligini göster

print("\n" + "="*60)
print(f"Tespit edilen Bookmaker ID'ler: {sorted(bookmaker_ids)}")
print("="*60)
print("\nTahminler:")
print("  14 = Nesine veya başka bir site")
print("  15 = Oley veya başka bir site")
print("\nNot: Hangi ID'nin Nesine/Oley olduğunu")
print("     sahadan.com web sitesinden karşılaştırarak bulabiliriz.")

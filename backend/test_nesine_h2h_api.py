"""
Nesine H2H API testi
Match ID nereden gelir? Sahadan UUID ile ilişkisi var mı?
"""

import requests
import json
from supabase_sync import get_supabase_client

print("="*80)
print("NESINE H2H API TEST")
print("="*80)

# Senin verdiğin örnek
test_match_id = "3389684"

print(f"\nTest Match ID: {test_match_id}")
print(f"URL: https://apistats.nesine.com/api/v3/HeadToHead/{test_match_id}/Summary?competitionHistoryCount=6")

try:
    response = requests.get(
        f"https://apistats.nesine.com/api/v3/HeadToHead/{test_match_id}/Summary?competitionHistoryCount=6",
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Accept': 'application/json'
        },
        timeout=15
    )
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"JSON response OK!")
        print(f"Response size: {len(response.text)} chars")
        
        # Data structure'ı incele
        if 'sc' in data and data['sc'] == 200:
            print(f"\nAPI Success Code: {data['sc']}")
            
            # Match bilgilerini bul
            d = data.get('d', {})
            
            # Takım isimleri
            if 'HT' in d and 'AT' in d:
                home_team = d['HT'].get('N', 'Unknown')
                away_team = d['AT'].get('N', 'Unknown')
                print(f"\nTakimlar:")
                print(f"  Home: {home_team}")
                print(f"  Away: {away_team}")
            
            # H2H data
            if 'SCH' in d:
                sch = d['SCH']
                if 'ML' in sch and len(sch['ML']) > 0:
                    h2h_matches = sch['ML']
                    print(f"\nH2H Maclari: {len(h2h_matches)} kategori")
                    
                    for category in h2h_matches:
                        tft = category.get('TFT', 0)
                        print(f"  Kategori TFT={tft}:")
                        
                        if 'TT' in category:
                            for tt in category['TT']:
                                ft = tt.get('FT', 0)
                                tms = tt.get('TMS', [])
                                print(f"    FT={ft}: {len(tms)} mac")
            
            print(f"\nBASARILI! Nesine H2H API calisiyor")
        else:
            print(f"API error code: {data.get('sc')}")
    else:
        print(f"HTTP Error: {response.status_code}")
        
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")

# Şimdi bu Match ID'yi nereden buluruz?
print("\n" + "="*80)
print("MATCH ID NASIL BULUNUR?")
print("="*80)

print("""
SORU: 3389684 gibi match ID'leri nereden bulacagiz?

YONTEM 1: Sahadan UUID -> Nesine Match ID mapping
   • Sahadan API'den UUID aliyoruz zaten
   • Nesine ID ile iliski var mi kontrol et
   
YONTEM 2: Nesine Bulletin API
   • Nesine'nin bulten API'si var mi?
   • Sahadan gibi match listesi ceker miyiz?
   
YONTEM 3: Supabase maclar ile eslestirlm
   • Takim isimleri + tarih ile ara
   • Nesine'de match search API'si var mi?
""")

# Test: Nesine bulletin API var mı?
print("\n" + "="*80)
print("NESINE BULLETIN API ARASTIRMASI")
print("="*80)

nesine_endpoints = [
    "https://apistats.nesine.com/api/v3/Bulletin",
    "https://apistats.nesine.com/api/v3/Matches/Today",
    "https://apistats.nesine.com/api/v3/Matches",
    "https://www.nesine.com/api/bulletin",
]

for endpoint in nesine_endpoints:
    print(f"\n{endpoint}")
    
    try:
        response = requests.get(
            endpoint,
            headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'},
            timeout=10
        )
        
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  JSON OK!")
                print(f"  Keys: {list(data.keys())[:10]}")
                
                # Match ID'leri ara
                json_str = json.dumps(data)
                if 'MID' in json_str or 'matchId' in json_str:
                    print(f"  MATCH IDs VAR!")
                    break
            except:
                print(f"  HTML response (size: {len(response.text)})")
                
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}")

print("\n" + "="*80)
print("SONRAKI ADIM:")
print("="*80)
print("""
1. Nesine bulletin API'sini bul (match listesi)
2. Match ID'leri cek
3. future_matches'e nesine_match_id ekle
4. H2H API'yi kullan: /HeadToHead/{nesine_match_id}/Summary

AVANTAJLAR:
   • JSON API (HTML parse yok!)
   • H2H + form data var
   • Hizli ve guvenilir
   • Zaten Nesine oranlarini kullaniyoruz
""")

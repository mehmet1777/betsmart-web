"""
Team ID'den Match ID'ye ulaşabilir miyiz?
"""

import requests
import json

print("="*80)
print("TEAM ID -> MATCH ID TEST")
print("="*80)

# Önce team ID'leri al
league_id = 73456
url = f"https://arsiv.mackolik.com/Standings/Data/FormData.aspx?id={league_id}"

response = requests.get(url, timeout=10)

print(f"Response status: {response.status_code}")
print(f"Response size: {len(response.text)} chars")
print(f"First 200 chars: {response.text[:200]}")

if response.status_code != 200 or not response.text.strip():
    print("ERROR: Empty or failed response")
    exit(1)

data = response.json()

print(f"\nLig ID: {league_id}")
print(f"Takim sayisi: {len(data)}")

# İlk 3 takımın ID'sini al
team_ids = [data[0][0], data[1][0], data[2][0]]
print(f"Ilk 3 takim ID: {team_ids}")

# Şimdi bu team ID'leri ile denemeler yapalım
print("\n" + "="*80)
print("TEAM ID ILE MATCH ARAMA:")
print("="*80)

# Olası endpoint'ler
test_urls = [
    # 1. Takımın maçları
    f"https://arsiv.mackolik.com/Team/Matches.aspx?id={{team_id}}",
    f"https://www.mackolik.com/takim/{{team_id}}/fikstür",
    f"https://www.mackolik.com/api/team/{{team_id}}/matches",
    
    # 2. Takım sayfası (HTML parse)
    f"https://arsiv.mackolik.com/Team/Default.aspx?id={{team_id}}",
    
    # 3. Ligin maçları
    f"https://arsiv.mackolik.com/Fixtures/Default.aspx?id={league_id}",
]

for team_id in team_ids[:1]:  # Sadece ilk takımı test et
    print(f"\n--- Team ID: {team_id} ---")
    
    for url_template in test_urls:
        url = url_template.format(team_id=team_id)
        print(f"\n{url}")
        
        try:
            response = requests.get(
                url,
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=10
            )
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                # JSON mi?
                try:
                    json_data = response.json()
                    print(f"  JSON response!")
                    print(f"  Keys: {list(json_data.keys())[:10]}")
                except:
                    # HTML - match linklerini ara
                    import re
                    
                    # Match ID pattern'leri
                    patterns = [
                        r'/mac/(\d+)/',
                        r'Match/Default\.aspx\?id=(\d+)',
                        r'matchId["\s:=]+(\d+)',
                    ]
                    
                    found_ids = []
                    for pattern in patterns:
                        matches = re.findall(pattern, response.text)
                        if matches:
                            found_ids.extend(matches[:5])
                    
                    if found_ids:
                        unique_ids = list(set(found_ids))
                        print(f"  MATCH IDs bulundu: {unique_ids[:5]}")
                        
                        # İlk match ID ile H2H test et
                        if unique_ids:
                            test_match_id = unique_ids[0]
                            h2h_url = f"https://arsiv.mackolik.com/Match/Head2Head.aspx?id={test_match_id}&s=1"
                            print(f"\n  H2H test: {h2h_url}")
                            
                            h2h_response = requests.get(h2h_url, timeout=10)
                            if h2h_response.status_code == 200:
                                if 'Aralarındaki' in h2h_response.text or len(h2h_response.text) > 1000:
                                    print(f"  BASARILI! H2H data var")
                                else:
                                    print(f"  HATALI: H2H data yok")
                    else:
                        print(f"  Match ID bulunamadi (HTML size: {len(response.text)})")
            
        except Exception as e:
            print(f"  ERROR: {type(e).__name__}")

# Ligin tüm maçları endpoint'ini test et
print("\n" + "="*80)
print("LIG FIKSTUR TEST:")
print("="*80)

fixtures_url = f"https://arsiv.mackolik.com/Fixtures/Default.aspx?id={league_id}"
print(f"\n{fixtures_url}")

try:
    response = requests.get(fixtures_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    
    if response.status_code == 200:
        print(f"Status: 200")
        
        # Match ID'leri ara
        import re
        match_ids = re.findall(r'Match/Default\.aspx\?id=(\d+)', response.text)
        
        if match_ids:
            unique_ids = list(set(match_ids))
            print(f"BASARILI! {len(unique_ids)} benzersiz match ID bulundu")
            print(f"Ilk 5: {unique_ids[:5]}")
            
            # İlk maçın H2H'sini test et
            test_id = unique_ids[0]
            h2h_url = f"https://arsiv.mackolik.com/Match/Head2Head.aspx?id={test_id}&s=1"
            print(f"\nH2H test: {h2h_url}")
            
            h2h_response = requests.get(h2h_url, timeout=10)
            if h2h_response.status_code == 200 and len(h2h_response.text) > 1000:
                print(f"BASARILI! H2H data var")
        else:
            print(f"Match ID bulunamadi")
            
except Exception as e:
    print(f"ERROR: {e}")

print("\n" + "="*80)
print("SONUC:")
print("="*80)
print("""
YONTEM 1: Team ID -> Team Fixtures -> Match ID
   • Takım sayfasından maçları çek
   • Match ID'leri parse et

YONTEM 2: League ID -> League Fixtures -> Match ID
   • Lig fikstür sayfasından tüm maçları çek
   • Match ID'leri parse et
   
EN BASIT: Lig fikstür sayfası
   • Tek request ile tüm lig maçları
   • Match ID'ler hazır
   • Takım isimleriyle eşleştir
""")

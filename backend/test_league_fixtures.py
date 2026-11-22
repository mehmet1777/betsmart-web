"""
Lig fixtures sayfasindan match ID'leri cek
"""

import requests
import re

print("="*80)
print("LIG FIXTURES -> MATCH ID TEST")
print("="*80)

# Test için farklı league ID'ler dene
test_leagues = [
    73456,  # Senin buldugun
    73455,  # Senin buldugun
    1,      # Premier League muhtemelen
    2,      # La Liga muhtemelen
]

for league_id in test_leagues:
    print(f"\n--- League ID: {league_id} ---")
    
    url = f"https://arsiv.mackolik.com/Fixtures/Default.aspx?id={league_id}"
    
    try:
        response = requests.get(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://arsiv.mackolik.com/'
            },
            timeout=15
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            html_size = len(response.text)
            print(f"HTML size: {html_size} chars")
            
            if html_size < 1000:
                print("HATALI: Cok kucuk response")
                continue
            
            # Match ID'leri ara
            patterns = [
                r'Match/Default\.aspx\?id=(\d+)',
                r'Head2Head\.aspx\?id=(\d+)',
                r'/mac/(\d+)/',
            ]
            
            all_ids = []
            for pattern in patterns:
                ids = re.findall(pattern, response.text)
                if ids:
                    print(f"Pattern '{pattern}': {len(ids)} match bulundu")
                    all_ids.extend(ids)
            
            if all_ids:
                unique_ids = list(set(all_ids))
                print(f"TOPLAM: {len(unique_ids)} benzersiz match ID")
                print(f"Ilk 5: {unique_ids[:5]}")
                
                # İlk maçın H2H'sini test et
                test_id = unique_ids[0]
                h2h_url = f"https://arsiv.mackolik.com/Match/Head2Head.aspx?id={test_id}&s=1"
                print(f"\nH2H TEST: {test_id}")
                
                h2h_response = requests.get(
                    h2h_url,
                    headers={'User-Agent': 'Mozilla/5.0'},
                    timeout=10
                )
                
                if h2h_response.status_code == 200:
                    # "Aralarındaki Maçlar" var mı kontrol et
                    if 'Aralarındaki' in h2h_response.text:
                        print(f"BASARILI! H2H data var")
                        print(f"H2H Link: {h2h_url}")
                        
                        # Takım isimlerini bul
                        team_pattern = r'<title>([^<]+vs[^<]+)</title>'
                        team_match = re.search(team_pattern, h2h_response.text)
                        if team_match:
                            print(f"Mac: {team_match.group(1)}")
                        
                        break  # Başarılı, diğer league'leri deneme
                    else:
                        print(f"HATALI: H2H data yok")
                else:
                    print(f"H2H request failed: {h2h_response.status_code}")
            else:
                print("Match ID bulunamadi")
        
        elif response.status_code == 403:
            print("403 Forbidden - IP/User-Agent ban olabilir")
        elif response.status_code == 404:
            print("404 - League ID gecersiz")
        
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)[:50]}")

print("\n" + "="*80)
print("SONUC:")
print("="*80)
print("""
BASARILIYSA:
   1. Lig fixtures sayfasinda match ID'ler var
   2. Regex ile parse edilebilir
   3. H2H linkleri olusturulabilir

BASARISIZSA (403):
   • IP ban olabilir
   • Rate limiting
   • Captcha gerekiyor olabilir
   
ALTERNATIF:
   • Mackolik ana iddaa sayfasindan mac linklerini cek
   • /mac/MATCHID/ formatinda linkler var
   • mackolik_api.py zaten bu sayfayi cekiror
""")

"""
SporDB - Mac listesi ve H2H testi
"""

import requests
from bs4 import BeautifulSoup
import re

print("="*80)
print("SPORDB API/SCRAPING TEST")
print("="*80)

# Senin verdiğin lig ID
league_id = "41156"

print(f"\nLig ID: {league_id}")

# Olası endpoint'ler
endpoints = [
    f"https://www.spordb.com/view/scoreboard_table.php?p2=msmain&sezon_altgrup_id={league_id}",
    f"https://www.spordb.com/view/fixture.php?sezon_altgrup_id={league_id}",
    f"https://www.spordb.com/fixture/{league_id}",
    f"https://www.spordb.com/matches/{league_id}",
    f"https://www.spordb.com/api/matches?league={league_id}",
]

for endpoint in endpoints:
    print(f"\n{endpoint}")
    
    try:
        response = requests.get(
            endpoint,
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=15
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            html_size = len(response.text)
            print(f"HTML size: {html_size} chars")
            
            # JSON mi kontrol et
            try:
                data = response.json()
                print(f"JSON response!")
                print(f"Keys: {list(data.keys())[:10]}")
                continue
            except:
                pass
            
            # HTML parse - maç linklerini ara
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Maç pattern'leri
            patterns = [
                r'mac_id=(\d+)',
                r'match_id=(\d+)',
                r'/mac/(\d+)',
                r'msdetail.*?(\d{6,})',
            ]
            
            all_ids = []
            for pattern in patterns:
                ids = re.findall(pattern, response.text)
                if ids:
                    all_ids.extend(ids)
            
            if all_ids:
                unique = list(set(all_ids))
                print(f"MAC IDs bulundu: {len(unique)} adet")
                print(f"Ilk 5: {unique[:5]}")
                
                # İlk maç ID ile detay sayfasını test et
                test_id = unique[0]
                
                # Olası detay sayfası URL'leri
                detail_urls = [
                    f"https://www.spordb.com/view/match_detail.php?mac_id={test_id}",
                    f"https://www.spordb.com/mac/{test_id}",
                    f"https://www.spordb.com/match/{test_id}",
                ]
                
                for detail_url in detail_urls:
                    try:
                        detail_response = requests.get(detail_url, timeout=10)
                        if detail_response.status_code == 200:
                            if len(detail_response.text) > 5000:
                                print(f"\nDetay sayfasi BULUNDU!")
                                print(f"URL: {detail_url}")
                                
                                # H2H data var mı kontrol et
                                if 'karşılaşma' in detail_response.text.lower() or 'h2h' in detail_response.text.lower():
                                    print(f"H2H data var gibi!")
                                
                                break
                    except:
                        pass
                
                break
            else:
                print(f"Mac ID bulunamadi")
                
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {str(e)[:50]}")

# Ana sayfa test - bugünün maçları
print("\n" + "="*80)
print("SPORDB ANA SAYFA - BUGUNUN MACLARI")
print("="*80)

main_urls = [
    "https://www.spordb.com",
    "https://www.spordb.com/today",
    "https://www.spordb.com/canli",
]

for url in main_urls:
    print(f"\n{url}")
    
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            # Maç ID'leri ara
            patterns = [
                r'mac_id=(\d+)',
                r'match.*?(\d{6,})',
            ]
            
            all_ids = []
            for pattern in patterns:
                ids = re.findall(pattern, response.text)
                if ids:
                    all_ids.extend(ids)
            
            if all_ids:
                unique = list(set(all_ids))
                print(f"MAC IDs: {len(unique)} adet")
                print(f"Ilk 5: {unique[:5]}")
                
                # Takım isimlerini de bul
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Takım ismi pattern'i ara
                teams = soup.find_all(text=re.compile(r'vs|gegen|-'))
                if teams:
                    print(f"\nOrnek maclar:")
                    for i, team_text in enumerate(teams[:3], 1):
                        print(f"  {i}. {team_text.strip()[:50]}")
                
                break
                
    except Exception as e:
        print(f"ERROR: {type(e).__name__}")

print("\n" + "="*80)
print("ALTERNATIF: MANUEL LIG ID MAPPING")
print("="*80)

print("""
SporDB lig ID'leri:
  • 41156 = ? (senin verdigin)
  • Premier League = ?
  • La Liga = ?
  • Serie A = ?
  • Bundesliga = ?
  • Turkiye Super Lig = ?

YONTEM:
  1. Her lig icin spordb.com'dan lig sayfasini bul
  2. URL'den sezon_altgrup_id'yi al
  3. Manuel mapping tablosu olustur
  4. Liglere gore mac ID'lerini cek
  
ORNEK:
  LEAGUE_IDS = {
      "TURKIYE Super Lig": "41156",
      "INGILTERE Premier League": "12345",
      ...
  }
""")

print("\n" + "="*80)
print("SONUC:")
print("="*80)
print("""
EGER MAC IDs BULUNURSA:
   MUKEMMEL! SporDB'den H2H data cekebiliriz
   
EGER BULUNAMAZSA:
   • HTML yapisi daha kompleks
   • JavaScript rendering olabilir
   • Manuel lig ID mapping gerekir

ONERIM:
   Sen manuel olarak populer liglerin ID'lerini verirsen:
   1. Lig bazinda mac ID'lerini cekelim
   2. Takim isimleri ile eslestirelim
   3. H2H API'yi kullanalim
   
   Bu yontem:
   ✅ Turk sitesi (engellenme riski az)
   ✅ Yakin bolgede (hizli)
   ✅ Manuel mapping (guvenilir)
""")

"""
Team ID -> Team Page -> Match IDs
"""

import requests
import re

print("="*80)
print("TEAM ID -> MATCH IDs")
print("="*80)

# Senin verdiğin datadan ilk 3 takım ID
team_ids = [120, 119, 137]

print(f"Test edilen takim IDleri: {team_ids}\n")

for team_id in team_ids:
    print(f"\n--- Team ID: {team_id} ---")
    
    # Olası takım sayfası URL'leri
    urls = [
        f"https://arsiv.mackolik.com/Team/Matches.aspx?id={team_id}",
        f"https://www.mackolik.com/takim/{team_id}/fikstür",
    ]
    
    for url in urls:
        print(f"\n{url}")
        
        try:
            response = requests.get(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    'Referer': 'https://arsiv.mackolik.com/'
                },
                timeout=15
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                html_size = len(response.text)
                print(f"HTML size: {html_size} chars")
                
                if html_size < 1000:
                    print("Cok kucuk response, bos sayfa")
                    continue
                
                # Match ID pattern'leri ara
                patterns = [
                    r'Match/Default\.aspx\?id=(\d+)',
                    r'Head2Head\.aspx\?id=(\d+)',
                    r'/mac/(\d+)/',
                ]
                
                all_matches = []
                for pattern in patterns:
                    matches = re.findall(pattern, response.text)
                    if matches:
                        all_matches.extend(matches)
                
                if all_matches:
                    unique = list(set(all_matches))
                    print(f"BASARILI! {len(unique)} benzersiz match ID bulundu")
                    print(f"Ilk 3: {unique[:3]}")
                    
                    # İlk maçın H2H'sini test et
                    test_id = unique[0]
                    h2h_url = f"https://arsiv.mackolik.com/Match/Head2Head.aspx?id={test_id}&s=1"
                    
                    h2h_response = requests.get(h2h_url, timeout=10)
                    if h2h_response.status_code == 200 and len(h2h_response.text) > 5000:
                        print(f"\nH2H TEST BASARILI!")
                        print(f"Link: {h2h_url}")
                        
                        # Başarılı, diğer URL'leri deneme
                        break
                else:
                    print("Match ID bulunamadi")
            
        except Exception as e:
            print(f"ERROR: {type(e).__name__}: {str(e)[:50]}")

print("\n" + "="*80)
print("ALTERNATIF: Takım isminden arama")
print("="*80)

# Takım ID -> Takım ismi (Form Data API'den alınabilir)
# Ama önce Team Info API'si var mı bakalım

team_id = 120
info_url = f"https://www.mackolik.com/api/team/{team_id}"

print(f"\n{info_url}")

try:
    response = requests.get(info_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("JSON response!")
            print(f"Keys: {list(data.keys())[:10]}")
            
            if 'name' in data:
                print(f"Takim adi: {data['name']}")
        except:
            print("JSON parse edilemedi")
            
except Exception as e:
    print(f"ERROR: {type(e).__name__}")

print("\n" + "="*80)
print("SONUC VE ONERILER:")
print("="*80)
print("""
YONTEM 1: Team ID -> Team Matches Page
   • https://arsiv.mackolik.com/Team/Matches.aspx?id=TEAM_ID
   • HTML parse ile match ID'leri cikar
   • SORUN: 403 veya bos sayfa gelebilir

YONTEM 2: Bizim Supabase maçları ile eşleştir
   1. Form Data API'den takım IDlerini al
   2. Bizim future_matches'ten takım isimlerini al
   3. İsim benzerliğine göre eşleştir
   4. Mackolik'te arama yap
   
YONTEM 3: Sahadan UUID yeterli (EN BASIT)
   • Zaten Sahadan'dan %40 başarı var
   • Mackolik fallback çok kompleks
   • Production'a şimdilik Sahadan ile geç
   • Mackolik fallback sonra ekle

ONERIM:
   Mackolik fallback ŞU AN için skip et.
   Sebep:
   • Match ID bulmak çok zor (API yok, HTML parse gerekiyor)
   • Rate limiting / 403 riski
   • %40 başarı yeterli (49 maç için detay var)
   • Frontend'e geç, kullanıcıya göster
   • İleride ihtiyaç olursa Mackolik ekle
""")

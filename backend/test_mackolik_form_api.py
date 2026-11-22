"""
Mackolik Form Data API testi
Format: [team_id, form_string, ?, ?, matches, points, ?, ?, ?, ?, ?]
"""

import requests
import json

print("="*80)
print("MACKOLIK FORM DATA API TEST")
print("="*80)

# Test league IDs
test_leagues = [
    (73456, "Lig 1"),
    (73455, "Lig 2"),
    (73454, "Lig 3?"),  # Tahmin
    (73457, "Lig 4?"),  # Tahmin
]

for league_id, league_name in test_leagues:
    print(f"\n[{league_name}] ID: {league_id}")
    
    try:
        url = f"https://arsiv.mackolik.com/Standings/Data/FormData.aspx?id={league_id}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and len(data) > 0:
                print(f"  OK: {len(data)} takim bulundu")
                
                # İlk takımı parse et
                first_team = data[0]
                print(f"  Ilk takim:")
                print(f"    Team ID: {first_team[0]}")
                print(f"    Form: {first_team[1]}")  # 3=Galibiyet, 1=Beraberlik, 0=Mağlubiyet
                print(f"    Matches: {first_team[4]}")
                print(f"    Points: {first_team[5]}")
                
                # Form string'i decode et (son 5 maç)
                form_str = first_team[1][-5:]  # Son 5 karakter
                form_decoded = []
                for char in form_str:
                    if char == '3':
                        form_decoded.append('W')  # Win
                    elif char == '1':
                        form_decoded.append('D')  # Draw
                    elif char == '0':
                        form_decoded.append('L')  # Loss
                
                print(f"    Form (son 5): {' '.join(form_decoded)}")
            else:
                print(f"  EMPTY")
        else:
            print(f"  ERROR: {response.status_code}")
            
    except Exception as e:
        print(f"  EXCEPTION: {e}")

print("\n" + "="*80)
print("SONUC:")
print("="*80)
print("""
BULGU:
   • https://arsiv.mackolik.com/Standings/Data/FormData.aspx?id=LEAGUE_ID
   • JSON formatinda form data donuyor
   • Format: [team_id, form_string, ?, ?, matches, points, ...]
   • form_string: 3=Galibiyet, 1=Beraberlik, 0=Maglubiyet

SORUN:
   • League ID'yi nereden bulacagiz?
   • 73456, 73455 gibi sayilar rastgele degil
   • Muhtemelen Mackolik'in internal league ID'si

COZUM 1: League ID mapping yapalim
   • Premier League → 73456 (ornek)
   • La Liga → 73455 (ornek)
   • Manuel mapping tablosu

COZUM 2: League ID'yi match'ten cikart
   • Mackolik match page'inde league linki var
   • /Standings/Default.aspx?id=73456 gibi
   • Bu ID'yi parse edip kaydet

COZUM 3: Mackolik API'den league list cek
   • /api/leagues veya benzeri endpoint
   • Tum league ID'leri al
   • Otomatik mapping

ONERILECEK:
   Sahadan match details yeterli, Mackolik fallback olarak kullan.
   Mackolik form data sadece standings icin kullanilabilir (ekstra feature).
""")

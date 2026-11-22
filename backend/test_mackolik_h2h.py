"""
Mackolik H2H API testi
"""

import requests
from bs4 import BeautifulSoup

# Test match ID
match_id = "4481113"

print("="*80)
print("🧪 MACKOLIK H2H TEST")
print("="*80)

# 1. HTML sayfasını test et
print(f"\n1️⃣ HTML Sayfası Test:")
print(f"   URL: https://arsiv.mackolik.com/Match/Head2Head.aspx?id={match_id}&s=1")

try:
    response = requests.get(
        f"https://arsiv.mackolik.com/Match/Head2Head.aspx?id={match_id}&s=1",
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        timeout=10
    )
    
    print(f"   Status: {response.status_code}")
    print(f"   Size: {len(response.text):,} chars")
    
    if response.status_code == 200:
        # HTML parse
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Aralarındaki Maçlar başlığını bul
        h2h_section = soup.find('div', text='Aralarındaki Maçlar')
        if h2h_section:
            print(f"   ✅ 'Aralarındaki Maçlar' bölümü bulundu")
            
            # Maç sonuçlarını ara
            # Genellikle tablo içinde olur
            table = h2h_section.find_next('table')
            if table:
                rows = table.find_all('tr')
                print(f"   ✅ {len(rows)} satır bulundu")
                
                # İlk birkaç satırı göster
                print(f"\n   İlk 5 satır:")
                for i, row in enumerate(rows[:5], 1):
                    cols = row.find_all(['td', 'th'])
                    text = ' | '.join([col.get_text(strip=True) for col in cols[:5]])
                    print(f"   {i}. {text[:100]}")
            else:
                print(f"   ⚠️ Tablo bulunamadı")
        else:
            print(f"   ⚠️ 'Aralarındaki Maçlar' bölümü bulunamadı")
            
            # Alternatif: ID'ye göre bul
            h2h_div = soup.find('div', {'id': lambda x: x and 'h2h' in x.lower()})
            if h2h_div:
                print(f"   💡 H2H div bulundu: {h2h_div.get('id')}")
    
except Exception as e:
    print(f"   ❌ Hata: {e}")

# 2. Mackolik API'yi test et (eğer varsa)
print(f"\n2️⃣ Mackolik API Test:")

# Olası API endpoint'leri
api_endpoints = [
    f"https://www.mackolik.com/api/match/{match_id}/h2h",
    f"https://api.mackolik.com/match/{match_id}/h2h",
    f"https://www.mackolik.com/Match/GetHead2Head?matchId={match_id}",
    f"https://arsiv.mackolik.com/api/match/{match_id}/h2h",
]

for endpoint in api_endpoints:
    try:
        response = requests.get(
            endpoint,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Accept': 'application/json'
            },
            timeout=5
        )
        
        print(f"   {endpoint}")
        print(f"   → Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   → Size: {len(response.text):,} chars")
            
            # JSON mi?
            try:
                data = response.json()
                print(f"   ✅ JSON response!")
                print(f"   → Keys: {list(data.keys())[:5]}")
                break
            except:
                print(f"   → HTML/Text response")
        
    except Exception as e:
        print(f"   → ❌ {type(e).__name__}")

print("\n" + "="*80)

# 3. Network tab'dan gerçek API'yi bul
print("\n💡 SONRAKİ ADIMLAR:")
print("   1. Chrome'da https://arsiv.mackolik.com/Match/Head2Head.aspx?id=4481113&s=1")
print("   2. F12 → Network tab")
print("   3. Sayfayı yenile")
print("   4. XHR/Fetch isteklerini ara (h2h, head2head, match, vb.)")
print("   5. Gerçek API endpoint'i bulun")
print("\n   Alternatif: HTML parse ile devam (BeautifulSoup)")

"""
Mackolik API'nin döndürdüğü HTML'i incele
"""
import requests
from datetime import datetime
from bs4 import BeautifulSoup

date_str = "21.11.2026"  # Yarın
print(f"📅 Test tarihi: {date_str}")

url = (
    f"https://www.mackolik.com/ajax/iddaa/events/soccer"
    f"?byKickOffTime=false"
    f"&competitionId="
    f"&selectedDate={date_str}"
    f"&eventUrlPrefixType=iddaaPage"
    f"&eventUrlSuffixType=iddaaPage"
    f"&googleAnalyticsAction=IddaaOddsClick"
    f"&googleAnalyticsCategory=IddaaOddsClick"
    f"&googleAnalyticsLabel=Iddaa%20Page%20Odds%20Click"
)

print(f"\n🌐 URL: {url}\n")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.mackolik.com/iddaa'
}

print("📡 İstek gönderiliyor...\n")

response = requests.get(url, headers=headers, timeout=30)

print(f"✅ Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"✅ JSON alındı")
    print(f"   Status: {data.get('status')}")
    
    html = data.get('data', {}).get('html', '')
    print(f"   HTML uzunluğu: {len(html)} karakter")
    
    if html:
        # HTML'i parse et
        soup = BeautifulSoup(html, 'html.parser')
        
        # Lig bölümlerini bul
        sections = soup.find_all('section', class_='widget-iddaa-events__competition-section')
        print(f"\n📊 Bulunan lig bölümü: {len(sections)}")
        
        if sections:
            print(f"\n🔍 İlk 3 lig:")
            for i, section in enumerate(sections[:3], 1):
                league_elem = section.find('div', class_='widget-iddaa-events__competition-name')
                if league_elem:
                    league_name = league_elem.get_text(strip=True)
                    rows = section.find_all('tr', class_='widget-iddaa-events__row--markets-summary')
                    print(f"   {i}. {league_name} - {len(rows)} maç")
        else:
            print("\n❌ Lig bölümü bulunamadı!")
            print("\n🔍 HTML içeriği (ilk 500 karakter):")
            print(html[:500])
    else:
        print("\n❌ HTML boş!")
        print(f"\n🔍 Tam JSON response:")
        print(data)
else:
    print(f"❌ Hata: {response.status_code}")
    print(response.text[:500])

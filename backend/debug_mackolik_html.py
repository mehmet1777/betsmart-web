"""Debug Mackolik HTML structure"""
import requests
from datetime import datetime
from bs4 import BeautifulSoup

today = datetime.now()
date_str = today.strftime("%d.%m.%Y")

url = f"https://www.mackolik.com/ajax/iddaa/events/soccer?byKickOffTime=false&competitionId=&selectedDate={date_str}&eventUrlPrefixType=iddaaPage&eventUrlSuffixType=iddaaPage"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.mackolik.com/iddaa'
}

print(f"📅 Tarih: {date_str}\n")

response = requests.get(url, headers=headers, timeout=10)
data = response.json()

html = data.get('data', {}).get('html', '')

# HTML'i dosyaya kaydet
with open('debug_mackolik.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✅ HTML dosyaya kaydedildi: debug_mackolik.html")
print(f"📏 HTML uzunluğu: {len(html)} karakter\n")

# İlk 2000 karakteri göster
print("📄 İlk 2000 karakter:")
print("=" * 80)
print(html[:2000])
print("=" * 80)

# BeautifulSoup ile parse
soup = BeautifulSoup(html, 'html.parser')

# Tüm section'ları bul
sections = soup.find_all('section')
print(f"\n📊 Toplam section sayısı: {len(sections)}")

# İlk section'u incele
if sections:
    print("\n🔍 İlk section:")
    print(sections[0].prettify()[:1000])

# Tüm class isimlerini bul
all_classes = set()
for tag in soup.find_all(True):
    classes = tag.get('class', [])
    for cls in classes:
        all_classes.add(cls)

print(f"\n📋 Bulunan unique class'lar (ilk 20):")
for cls in sorted(list(all_classes))[:20]:
    print(f"  - {cls}")

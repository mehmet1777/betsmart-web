"""
Mackolik Geçmiş Maçlar API'sini bul
"""
import requests
from datetime import datetime, timedelta

# Dünün tarihi
yesterday = (datetime.now() - timedelta(days=1)).strftime("%d.%m.%Y")

print(f"🔍 Geçmiş maçlar API'si aranıyor...")
print(f"📅 Test tarihi: {yesterday}\n")

# Olası endpoint'ler
endpoints = [
    f"https://www.mackolik.com/ajax/iddaa/results/soccer?date={yesterday}",
    f"https://www.mackolik.com/ajax/results/soccer?date={yesterday}",
    f"https://www.mackolik.com/ajax/iddaa/events/soccer?selectedDate={yesterday}&type=results",
    f"https://www.mackolik.com/ajax/data/results/soccer?date={yesterday}",
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.mackolik.com/iddaa'
}

for i, url in enumerate(endpoints, 1):
    print(f"\n{i}. Test ediliyor:")
    print(f"   URL: {url[:80]}...")
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            
            print(f"   ✅ Status: {response.status_code}")
            print(f"   📏 Size: {len(response.text):,} bytes")
            print(f"   📦 Type: {content_type}")
            
            # JSON mi kontrol et
            if 'json' in content_type:
                try:
                    data = response.json()
                    print(f"   ✅ Valid JSON!")
                    print(f"   🔑 Keys: {list(data.keys())[:5]}")
                    
                    # İlk 500 karakter
                    import json
                    print(f"\n   📄 Preview:")
                    print("   " + "=" * 60)
                    print(json.dumps(data, indent=2, ensure_ascii=False)[:500])
                    print("   " + "=" * 60)
                    
                except:
                    print(f"   ⚠️  JSON parse hatası")
            else:
                print(f"   ℹ️  HTML response (JSON değil)")
        else:
            print(f"   ❌ Status: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")

print("\n\n💡 ŞİMDİ SEN YAP:")
print("=" * 70)
print("1. https://www.mackolik.com/iddaa sayfasına git")
print("2. F12 bas → Network tab")
print("3. 'Sonuçlar' veya geçmiş tarih seç")
print("4. XHR/Fetch filtresi aktif et")
print("5. 'ajax' içeren isteklere bak")
print("6. URL'yi buraya yapıştır!")
print("=" * 70)

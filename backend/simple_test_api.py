"""Basit API testi"""
import requests
from datetime import datetime

# Bugünün tarihi
today = datetime.now()
date_str = today.strftime("%d.%m.%Y")

print(f"📅 Test edilen tarih: {date_str}")

# API URL
url = f"https://www.mackolik.com/ajax/iddaa/events/soccer?byKickOffTime=false&competitionId=&selectedDate={date_str}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.mackolik.com/iddaa'
}

print("🌐 API'ye istek gönderiliyor...\n")

try:
    response = requests.get(url, headers=headers, timeout=30)
    
    print(f"✅ Status Code: {response.status_code}")
    print(f"📏 Response Size: {len(response.text):,} bytes\n")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ JSON parse başarılı")
        print(f"📊 Keys: {list(data.keys())}\n")
        
        html = data.get('data', {}).get('html', '')
        print(f"📄 HTML Length: {len(html):,} characters\n")
        
        # İlk 3000 karakteri göster
        print("=" * 80)
        print("İLK 3000 KARAKTER:")
        print("=" * 80)
        print(html[:3000])
        print("=" * 80)
        
        # Maç var mı kontrol et
        if 'widget-iddaa-events__team-name--home' in html:
            print("\n✅ HTML'de maç verileri VAR!")
            
            # Kaç takım ismi var?
            home_count = html.count('widget-iddaa-events__team-name--home')
            print(f"📊 Yaklaşık {home_count} maç bulundu")
        else:
            print("\n⚠️ HTML'de maç verileri YOK - Belki bu tarihte maç yok?")
            
        # HTML'i dosyaya kaydet
        with open('mackolik_response.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("\n💾 HTML 'mackolik_response.html' dosyasına kaydedildi")
        
    else:
        print(f"❌ HTTP Hatası: {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"❌ Hata: {str(e)}")
    import traceback
    traceback.print_exc()

"""
Mackolik bülteninden match ID çekme testi
Sahadan gibi ama Mackolik için
"""

import requests
from datetime import datetime, timedelta

print("="*80)
print("🎯 MACKOLIK BÜLTEN TEST - Match ID Çekme")
print("="*80)

# Mackolik'in olası API endpoint'leri
# Sahadan benzeri: /api/betting-service-bulletin-soccer
endpoints = [
    "https://www.mackolik.com/api/bulletin/matches",
    "https://www.mackolik.com/api/matches/today",
    "https://api.mackolik.com/bulletin",
    "https://www.mackolik.com/canli-sonuclar",  # HTML parse
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json, text/html',
    'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7'
}

print("\n🔍 API Endpoint'leri test ediliyor...")
print("="*80)

for endpoint in endpoints:
    print(f"\n📡 {endpoint}")
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   Size: {len(response.text):,} chars")
            
            # JSON mi?
            try:
                data = response.json()
                print(f"   ✅ JSON response!")
                print(f"   Keys: {list(data.keys())[:10]}")
                
                # Maçları ara
                if isinstance(data, list):
                    print(f"   → Array: {len(data)} items")
                    if len(data) > 0:
                        print(f"   → First item keys: {list(data[0].keys())[:10]}")
                elif isinstance(data, dict):
                    # Nested data ara
                    for key in ['matches', 'data', 'results', 'fixtures']:
                        if key in data:
                            matches = data[key]
                            print(f"   → Found '{key}': {len(matches) if isinstance(matches, list) else 'dict'}")
                            if isinstance(matches, list) and len(matches) > 0:
                                first = matches[0]
                                print(f"   → First match keys: {list(first.keys())[:15]}")
                                print(f"   → Sample: {first}")
                                break
                
            except Exception as json_err:
                # HTML parse
                if 'Match/Default.aspx?id=' in response.text or 'mac/' in response.text:
                    print(f"   ✅ HTML bulundu (match links var)")
                    
                    import re
                    # Match ID'leri bul
                    ids = re.findall(r'Match/Default\.aspx\?id=(\d+)', response.text)
                    if ids:
                        print(f"   → {len(set(ids))} unique match ID bulundu")
                        print(f"   → İlk 5: {ids[:5]}")
                    
                    # Modern URL format: /mac/123456/team-vs-team
                    mac_ids = re.findall(r'/mac/(\d+)/', response.text)
                    if mac_ids:
                        print(f"   → {len(set(mac_ids))} modern format ID bulundu")
                        print(f"   → İlk 5: {mac_ids[:5]}")
                else:
                    print(f"   ⚠️ HTML ama match link yok")
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {type(e).__name__}: {str(e)[:50]}")

print("\n" + "="*80)
print("\n💡 ALTERNATIF YÖNTEM: hybrid_fetch.py'yi incele")
print("="*80)

# hybrid_fetch.py'de Mackolik'ten nasıl çekildiğini kontrol et
try:
    import sys
    import os
    
    # hybrid_fetch'i import et
    from hybrid_fetch import fetch_matches_hybrid
    
    print("\n✅ hybrid_fetch modülü bulundu")
    print("   Bu modül zaten Mackolik'ten veri çekiyor")
    print("   Şimdi: Mackolik match ID'yi ekleyelim!\n")
    
    # hybrid_fetch'in kodunu göster
    print("🔍 hybrid_fetch.py dosyasını kontrol edin:")
    print("   • scrape_mackolik_iddaa() fonksiyonu var mı?")
    print("   • Match ID parse ediliyor mu?")
    print("   • Eğer evet: ID'yi future_matches'e ekle")
    print("   • Eğer hayır: ID'yi parse etmeyi ekle\n")
    
except Exception as e:
    print(f"\n⚠️ hybrid_fetch import edilemedi: {e}")

print("="*80)
print("\n📝 ÖNERİLEN ÇÖZÜM:")
print("="*80)
print("""
1. sahadan_api.py → 'match_uuid' ekle (✅ YAPILDI)
2. hybrid_fetch.py → 'mackolik_match_id' ekle (🔄 YAPALIM)
3. supabase_sync.py → 'mackolik_match_id' kaydet (🔄 YAPALIM)
4. match_details_api.py → Fallback ekle:
   
   def fetch_match_details(match_uuid=None, mackolik_id=None):
       if match_uuid:
           # Sahadan'dan dene
           success, data, error = fetch_from_sahadan(match_uuid)
           if success:
               return data
       
       if mackolik_id:
           # Mackolik'ten dene (fallback)
           success, data, error = fetch_from_mackolik(mackolik_id)
           if success:
               return data
       
       return None, None, "Hiçbir kaynaktan detay çekilemedi"

SONUÇ:
   • Sahadan 502 → Mackolik fallback
   • 49 başarılı + 72 başarısız → ~100+ başarılı olabilir!
""")

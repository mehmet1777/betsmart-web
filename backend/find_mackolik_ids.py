"""
ASIL SORU: Bizim maçlarımızın Mackolik ID'lerini bulabilir miyiz?

Test:
1. Supabase'den bir maç al (home_team, away_team)
2. Mackolik'te bu maçı ara
3. Match ID'yi bul
4. H2H linkini oluştur
"""

import requests
from bs4 import BeautifulSoup
import re
from supabase_sync import get_supabase_client

print("="*80)
print("🎯 MACKOLIK MATCH ID BULMA - OTOMATİK")
print("="*80)

try:
    client = get_supabase_client()
    
    # Popüler bir lig seç (Mackolik'te kesin vardır)
    # Örnek: Premier League, La Liga, Serie A
    test_leagues = [
        'İNGİLTERE Premier League',
        'İSPANYA La Liga',
        'İTALYA Serie A',
        'ALMANYA Bundesliga',
        'TÜRKİYE Süper Lig'
    ]
    
    print(f"\n📊 Popüler liglerden maç arıyoruz...")
    
    matches = client.table('future_matches').select(
        'home_team,away_team,league,datetime'
    ).in_('league', test_leagues).limit(3).execute()
    
    if not matches.data:
        print("⚠️ Popüler ligde maç yok, random alıyoruz...")
        matches = client.table('future_matches').select(
            'home_team,away_team,league,datetime'
        ).limit(3).execute()
    
    print(f"✅ {len(matches.data)} test maçı bulundu")
    print("="*80)
    
    for i, match in enumerate(matches.data, 1):
        home = match['home_team']
        away = match['away_team']
        league = match.get('league', 'N/A')
        
        print(f"\n{i}. {home} vs {away}")
        print(f"   Lig: {league}")
        
        # YÖNTEM 1: Mackolik ana sayfasında bugünün maçlarını çek
        print(f"\n   🔍 Yöntem 1: Mackolik ana sayfasında arıyoruz...")
        
        try:
            # Mackolik iddaa sayfası
            url = "https://www.mackolik.com/iddaa"
            response = requests.get(
                url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                },
                timeout=10
            )
            
            if response.status_code == 200:
                # HTML parse
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Maç linklerini ara
                # Mackolik linkleri genelde: /mac/MATCHID/team-vs-team
                links = soup.find_all('a', href=re.compile(r'/mac/\d+/'))
                
                print(f"      → {len(links)} maç linki bulundu")
                
                # Takım isimlerine göre eşleştir
                found = False
                for link in links:
                    href = link.get('href', '')
                    text = link.get_text().lower()
                    
                    # Basit eşleştirme
                    home_simple = home.lower().replace(' ', '')[:10]
                    away_simple = away.lower().replace(' ', '')[:10]
                    
                    if home_simple in text or away_simple in text:
                        # Match ID'yi çıkar
                        match_id = re.search(r'/mac/(\d+)/', href)
                        if match_id:
                            mackolik_id = match_id.group(1)
                            print(f"      ✅ BULUNDU!")
                            print(f"      → Mackolik ID: {mackolik_id}")
                            print(f"      → Link: https://www.mackolik.com{href}")
                            print(f"      → H2H: https://arsiv.mackolik.com/Match/Head2Head.aspx?id={mackolik_id}&s=1")
                            found = True
                            break
                
                if not found:
                    print(f"      ❌ Bu maç ana sayfada bulunamadı")
                    
        except Exception as e:
            print(f"      ❌ Hata: {e}")
        
        # YÖNTEM 2: Google arama (son çare)
        print(f"\n   🔍 Yöntem 2: Google'da arıyoruz...")
        try:
            # Google: "Mackolik TeamA TeamB"
            query = f"site:mackolik.com {home} {away}"
            google_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            
            response = requests.get(
                google_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                },
                timeout=10
            )
            
            if response.status_code == 200:
                # Mackolik linklerini ara
                mac_links = re.findall(r'mackolik\.com/mac/(\d+)/', response.text)
                
                if mac_links:
                    mackolik_id = mac_links[0]
                    print(f"      ✅ Google'da bulundu!")
                    print(f"      → Mackolik ID: {mackolik_id}")
                    print(f"      → H2H: https://arsiv.mackolik.com/Match/Head2Head.aspx?id={mackolik_id}&s=1")
                else:
                    print(f"      ❌ Google'da bulunamadı")
            
        except Exception as e:
            print(f"      ❌ Hata: {e}")
        
        print("   " + "-"*76)

except Exception as e:
    print(f"\n❌ Genel hata: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("💡 SONUÇ VE ÖNERİLER:")
print("="*80)
print("""
SORUN: 
   • Mackolik match ID'yi bulmak zor
   • API yok, HTML parse gerekiyor
   • Takım isimleri farklı olabilir

ÇÖZÜM 1: hybrid_fetch'e Match ID ekle (EN İYİSİ)
   ✅ /yeniveri çalıştığında hem Sahadan UUID hem Mackolik ID çekilir
   ✅ future_matches tablosuna iki ID de kaydedilir
   ✅ match_details_api.py'de fallback:
      1. Sahadan UUID var mı? → Sahadan'dan çek
      2. Sahadan 502 → Mackolik ID ile Mackolik'ten çek

ÇÖZÜM 2: Manuel mapping (popüler ligler için)
   • Premier League, La Liga gibi popüler ligler için
   • Takım isimlerini manuel map et
   • Sadece popüler liglerde çalışır

ÇÖZÜM 3: Real-time arama (yavaş)
   • Her match details fetch'inde Google'da ara
   • Çok yavaş (1-2 saniye/maç ekstra)
   • Rate limit riski

ÖNERİ: ÇÖZÜM 1 uygulanmalı
   • mackolik_api.py zaten maçları çekiyor
   • Match ID'yi parse edip kaydet
   • 72 başarısız → ~50-60 başarılı olabilir!
""")

"""
Mackolik Match ID'yi nasıl buluruz?
Sahadan UUID'den Mackolik ID'ye dönüşüm var mı?
"""

import requests
from supabase_sync import get_supabase_client

print("="*80)
print("🔍 MACKOLIK MATCH ID BULMA TESTİ")
print("="*80)

# Test için Supabase'den birkaç maç alalım
try:
    client = get_supabase_client()
    
    # Sahadan'dan çekilmiş maçlar (UUID var)
    sahadan_matches = client.table('future_matches').select(
        'match_uuid,home_team,away_team,datetime,league'
    ).not_.is_('match_uuid', 'null').limit(5).execute()
    
    print(f"\n📊 Sahadan'dan çekilmiş {len(sahadan_matches.data)} test maçı:")
    print("="*80)
    
    for i, match in enumerate(sahadan_matches.data, 1):
        print(f"\n{i}. {match['home_team']} vs {match['away_team']}")
        print(f"   Lig: {match.get('league', 'N/A')}")
        print(f"   Tarih: {match.get('datetime', 'N/A')}")
        print(f"   Sahadan UUID: {match['match_uuid']}")
        
        # Mackolik'te arama yap
        # Yöntem 1: Takım isimlerine göre arama
        home = match['home_team'].replace(' ', '+')
        away = match['away_team'].replace(' ', '+')
        
        print(f"\n   🔍 Mackolik'te arıyoruz...")
        
        # Mackolik arama API'si
        search_endpoints = [
            f"https://www.mackolik.com/ara/{home}",
            f"https://arsiv.mackolik.com/ara/{home}",
            f"https://www.mackolik.com/api/search?q={home}",
        ]
        
        found_id = None
        
        for endpoint in search_endpoints:
            try:
                response = requests.get(
                    endpoint,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                        'Accept': 'application/json, text/html'
                    },
                    timeout=5
                )
                
                if response.status_code == 200:
                    # JSON mu?
                    try:
                        data = response.json()
                        print(f"   ✅ JSON bulundu: {endpoint}")
                        print(f"      Keys: {list(data.keys())[:10]}")
                        
                        # Match ID'yi ara
                        # Genellikle 'matches', 'results', 'data' gibi key'lerde
                        if 'matches' in data:
                            print(f"      Matches: {len(data['matches'])} adet")
                            if len(data['matches']) > 0:
                                first_match = data['matches'][0]
                                print(f"      İlk maç: {first_match}")
                                if 'id' in first_match:
                                    found_id = first_match['id']
                        
                        break
                    except:
                        # HTML parse dene
                        if 'Match/Default.aspx?id=' in response.text:
                            import re
                            ids = re.findall(r'Match/Default\.aspx\?id=(\d+)', response.text)
                            if ids:
                                print(f"   ✅ HTML'den ID bulundu: {ids[:3]}")
                                found_id = ids[0]
                                break
                        
            except Exception as e:
                continue
        
        if found_id:
            print(f"\n   🎯 Mackolik ID bulundu: {found_id}")
            print(f"   🔗 H2H URL: https://arsiv.mackolik.com/Match/Head2Head.aspx?id={found_id}&s=1")
        else:
            print(f"\n   ❌ Mackolik ID bulunamadı")
        
        print("   " + "-"*76)
        
except Exception as e:
    print(f"\n❌ Hata: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("💡 SONUÇ:")
print("="*80)
print("""
YÖNTEM 1: Mackolik Arama API
   • Takım isimlerine göre arama yap
   • Match ID'yi response'dan çıkar
   • H2H için kullan

YÖNTEM 2: Manuel Mapping
   • Popüler ligler için manuel ID mapping
   • Örnek: Premier League → mackolik_league_id
   • future_matches'e mackolik_match_id ekle

YÖNTEM 3: Mackolik Scraping (hybrid_fetch gibi)
   • Mackolik bülteninden maç listesi çek
   • Takım isimleri ile eşleştir
   • ID'yi sakla

ÖNERİ: Yöntem 1 + Yöntem 3 kombinasyonu
   • hybrid_fetch'e mackolik_match_id ekle
   • Sahadan UUID yok ise Mackolik ID'yi kullan
   • match_details_api.py'de fallback ekle:
     1. Önce Sahadan dene (UUID ile)
     2. Başarısız ise Mackolik dene (match_id ile)
""")

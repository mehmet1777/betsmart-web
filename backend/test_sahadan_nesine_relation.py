"""
Sahadan UUID ile Nesine Match ID arasinda iliski var mi?
"""

import requests
from supabase_sync import get_supabase_client

print("="*80)
print("SAHADAN UUID <-> NESINE MATCH ID ILISKISI")
print("="*80)

# Supabase'den UUID'li bir maç al
try:
    client = get_supabase_client()
    
    matches = client.table('future_matches').select(
        'match_uuid,home_team,away_team,datetime,league'
    ).not_.is_('match_uuid', 'null').limit(5).execute()
    
    if matches.data:
        print(f"\n{len(matches.data)} test maci bulundu\n")
        
        for i, match in enumerate(matches.data, 1):
            uuid = match['match_uuid']
            home = match['home_team']
            away = match['away_team']
            
            print(f"{i}. {home} vs {away}")
            print(f"   Sahadan UUID: {uuid}")
            print(f"   Tarih: {match.get('datetime')}")
            
            # Sahadan API'den match details cek
            sahadan_url = f"https://www.sahadan.com/api/index/match-detail?match_uuid={uuid}&lang=tr&device=web"
            
            try:
                response = requests.get(sahadan_url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Nesine ID var mi kontrol et
                    import json
                    json_str = json.dumps(data)
                    
                    # Olasi field'ler: nesineId, nesine_id, nid, provider_id
                    patterns = [
                        'nesineId', 'nesine_id', 'nid', 'nesine',
                        'providerId', 'provider_id', 'externalId'
                    ]
                    
                    found = False
                    for pattern in patterns:
                        if pattern in json_str:
                            print(f"   BULUNDU! '{pattern}' field var")
                            found = True
                            
                            # Value'yu bul
                            import re
                            value_pattern = f'"{pattern}"[:\s]+([0-9]+)'
                            matches_val = re.findall(value_pattern, json_str)
                            if matches_val:
                                nesine_id = matches_val[0]
                                print(f"   Nesine ID: {nesine_id}")
                                
                                # Nesine H2H API'yi test et
                                nesine_url = f"https://apistats.nesine.com/api/v3/HeadToHead/{nesine_id}/Summary?competitionHistoryCount=6"
                                nesine_response = requests.get(nesine_url, timeout=10)
                                
                                if nesine_response.status_code == 200:
                                    print(f"   BASARILI! Nesine H2H API calisti")
                                    nesine_data = nesine_response.json()
                                    if nesine_data.get('sc') == 200:
                                        d = nesine_data.get('d', {})
                                        ht = d.get('HT', {}).get('N', 'N/A')
                                        at = d.get('AT', {}).get('N', 'N/A')
                                        print(f"   Takimlar: {ht} vs {at}")
                                else:
                                    print(f"   Nesine H2H failed: {nesine_response.status_code}")
                    
                    if not found:
                        print(f"   Nesine ID bulunamadi")
                        
                        # JSON structure'i goster
                        if isinstance(data, dict):
                            print(f"   Top-level keys: {list(data.keys())[:10]}")
                else:
                    print(f"   Sahadan API error: {response.status_code}")
                    
            except Exception as e:
                print(f"   ERROR: {type(e).__name__}: {str(e)[:50]}")
            
            print()
            
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("="*80)
print("ALTERNATIF: Nesine web sitesinden match ID bul")
print("="*80)

print("""
1. Nesine.com ana sayfasi
2. Mac listesi
3. Bir maca tikla
4. URL'de match ID var mi?
   Ornek: nesine.com/iddaa/mac/3389684/...

Eger varsa:
   • Nesine.com'dan scraping ile match ID'leri cekebiliriz
   • Takim isimleri ile eslestirebiliriz
""")

# Nesine ana sayfa test
print("\n" + "="*80)
print("NESINE ANA SAYFA TEST")
print("="*80)

nesine_home_url = "https://www.nesine.com/iddaa/futbol"

try:
    response = requests.get(
        nesine_home_url,
        headers={'User-Agent': 'Mozilla/5.0'},
        timeout=15
    )
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        import re
        
        # Match ID pattern'leri ara
        patterns = [
            r'/iddaa/mac/(\d+)/',
            r'matchId["\s:=]+(\d+)',
            r'MID["\s:=]+(\d+)',
        ]
        
        all_ids = []
        for pattern in patterns:
            ids = re.findall(pattern, response.text)
            if ids:
                all_ids.extend(ids)
        
        if all_ids:
            unique = list(set(all_ids))
            print(f"BASARILI! {len(unique)} benzersiz match ID bulundu")
            print(f"Ilk 5: {unique[:5]}")
            
            # İlk ID ile H2H test et
            test_id = unique[0]
            h2h_url = f"https://apistats.nesine.com/api/v3/HeadToHead/{test_id}/Summary?competitionHistoryCount=6"
            
            h2h_response = requests.get(h2h_url, timeout=10)
            if h2h_response.status_code == 200:
                h2h_data = h2h_response.json()
                if h2h_data.get('sc') == 200:
                    print(f"\nH2H TEST BASARILI!")
                    d = h2h_data.get('d', {})
                    ht = d.get('HT', {}).get('N', 'N/A')
                    at = d.get('AT', {}).get('N', 'N/A')
                    print(f"Match ID {test_id}: {ht} vs {at}")
        else:
            print("Match ID bulunamadi (HTML size: {len(response.text)})")
            
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {str(e)[:50]}")

print("\n" + "="*80)
print("SONUC:")
print("="*80)
print("""
EGER SAHADAN API'DE NESINE ID VARSA:
   MUKEMMEL! Zaten UUID'den Nesine ID'ye ceviri yapabiliriz
   
EGER NESINE WEB'DEN MATCH ID BULUNURSA:
   • Scraping ile match ID'leri cek
   • Takim isimleri + tarih ile eslestirlm
   • future_matches'e nesine_match_id ekle
   
EGER IKISI DE YOKSA:
   • Manuel mapping (sadece populer ligler)
   • Veya Sahadan ile devam et (%40 basari yeterli)
""")

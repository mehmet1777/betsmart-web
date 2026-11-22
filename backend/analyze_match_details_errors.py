"""
Match details başarısızlık nedenlerini analiz et
"""

from supabase_sync import get_supabase_client
from match_details_api import fetch_match_details
import time

try:
    client = get_supabase_client()
    
    print("="*80)
    print("🔍 MATCH DETAILS BAŞARISIZLIK ANALİZİ")
    print("="*80)
    
    # 1. future_matches'ten UUID'leri al
    all_matches = client.table('future_matches').select('match_uuid,home_team,away_team').execute()
    
    uuids_with_data = []
    uuids_without_data = []
    
    for match in all_matches.data:
        uuid = match.get('match_uuid')
        if uuid and uuid.strip() and uuid != 'None':
            uuids_with_data.append({
                'uuid': uuid,
                'home_team': match['home_team'],
                'away_team': match['away_team']
            })
        else:
            uuids_without_data.append({
                'home_team': match['home_team'],
                'away_team': match['away_team']
            })
    
    print(f"\n📊 GENEL İSTATİSTİK:")
    print(f"   Toplam maç: {len(all_matches.data)}")
    print(f"   UUID var: {len(uuids_with_data)}")
    print(f"   UUID yok: {len(uuids_without_data)}")
    
    # 2. match_details'ten başarılı olanları al
    saved_details = client.table('match_details').select('match_uuid').execute()
    saved_uuids = set(d['match_uuid'] for d in saved_details.data)
    
    print(f"\n✅ BAŞARILI:")
    print(f"   Supabase'de kayıtlı: {len(saved_uuids)}")
    
    # 3. Başarısız olanları bul
    failed_matches = [m for m in uuids_with_data if m['uuid'] not in saved_uuids]
    
    print(f"\n❌ BAŞARISIZ:")
    print(f"   Kayıt yok: {len(failed_matches)}")
    
    if len(failed_matches) > 0:
        print(f"\n🔬 İLK 5 BAŞARISIZ MAÇI TEST EDELİM:")
        print("="*80)
        
        for i, match in enumerate(failed_matches[:5], 1):
            print(f"\n{i}. {match['home_team']} vs {match['away_team']}")
            print(f"   UUID: {match['uuid']}")
            
            # API test
            success, data, error = fetch_match_details(match['uuid'])
            
            if success:
                print(f"   ✅ API yanıt verdi")
                print(f"   H2H: {len(data.get('h2h_data', {}).get('matches', []))} maç")
                print(f"   Form Home: {len(data.get('form_home', {}).get('matches', []))} maç")
                print(f"   Form Away: {len(data.get('form_away', {}).get('matches', []))} maç")
            else:
                print(f"   ❌ API hatası: {error}")
            
            time.sleep(1)  # Rate limit
        
        print("\n" + "="*80)
        print(f"\n💡 SONUÇ:")
        print(f"   • Eğer 'API yanıt verdi' görüyorsanız: Sync hatası var")
        print(f"   • Eğer 'API hatası' görüyorsanız: Sahadan'da detay yok")
    
    # 4. UUID yok olanları göster
    if len(uuids_without_data) > 0:
        print(f"\n⚠️ UUID YOK ({len(uuids_without_data)} maç):")
        print(f"   İlk 5:")
        for i, match in enumerate(uuids_without_data[:5], 1):
            print(f"   {i}. {match['home_team']} vs {match['away_team']}")
        print(f"\n   💡 Sebep: Muhtemelen Mackolik fallback kullanılmış")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()

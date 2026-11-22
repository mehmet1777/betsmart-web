"""
Supabase'de UUID kontrolü
"""

from supabase_sync import get_supabase_client

try:
    client = get_supabase_client()
    
    # UUID'li maçları say
    result = client.table('future_matches').select('match_uuid, home_team, away_team, league').not_.is_('match_uuid', 'null').execute()
    
    print(f"📊 UUID'li maç sayısı: {len(result.data)}\n")
    
    if result.data:
        print("İlk 5 maç:")
        for i, match in enumerate(result.data[:5], 1):
            print(f"{i}. {match['home_team']} vs {match['away_team']}")
            print(f"   UUID: {match['match_uuid']}")
            print(f"   Lig: {match.get('league', 'N/A')}\n")
    else:
        print("⚠️ Hiç UUID yok. Sebepleri:")
        print("1. /yeniveri henüz çalıştırılmadı")
        print("2. Sahadan API'den UUID gelmiyor")
        print("3. supabase_sync.py UUID'yi kaydetmiyor")
        
        print("\n🔍 Test için bir maç çekelim:")
        
        # Rastgele bir maç çek
        all_matches = client.table('future_matches').select('*').limit(1).execute()
        
        if all_matches.data:
            match = all_matches.data[0]
            print(f"\n📋 Örnek maç:")
            print(f"   ID: {match.get('id')}")
            print(f"   Maç: {match.get('home_team')} vs {match.get('away_team')}")
            print(f"   UUID: {match.get('match_uuid', 'YOK ❌')}")
            print(f"   Tarih: {match.get('datetime')}")
        else:
            print("\n⚠️ Hiç maç yok!")
            
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()

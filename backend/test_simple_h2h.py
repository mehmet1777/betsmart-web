"""
Basit H2H test - Galatasaray vs Fenerbahce
"""

from supabase_sync import get_supabase_client

try:
    client = get_supabase_client()
    
    print("="*80)
    print("GALATASARAY vs FENERBAHCE - H2H TEST")
    print("="*80)
    
    # Basit sorgu - home_team'de Galatasaray, away_team'de Fenerbahce
    print("\n1. Galatasaray (EV) vs Fenerbahce (DEP):")
    result1 = client.table('matches').select('*').ilike(
        'home_team', '%Galatasaray%'
    ).ilike('away_team', '%Fenerbahce%').limit(10).execute()
    
    print(f"   Bulundu: {len(result1.data)} mac")
    for match in result1.data[:5]:
        print(f"   - {match['home_team']} {match['score']} {match['away_team']}")
    
    # Ters - Fenerbahce ev sahibi
    print("\n2. Fenerbahce (EV) vs Galatasaray (DEP):")
    result2 = client.table('matches').select('*').ilike(
        'home_team', '%Fenerbahce%'
    ).ilike('away_team', '%Galatasaray%').limit(10).execute()
    
    print(f"   Bulundu: {len(result2.data)} mac")
    for match in result2.data[:5]:
        print(f"   - {match['home_team']} {match['score']} {match['away_team']}")
    
    # Toplam
    total = len(result1.data) + len(result2.data)
    print(f"\nTOPLAM H2H: {total} mac")
    
    if total > 0:
        print("\n✅ BASARILI! Kendi datamizda H2H var!")
    else:
        print("\n❌ H2H bulunamadi")
    
except Exception as e:
    print(f"\nHATA: {e}")
    import traceback
    traceback.print_exc()

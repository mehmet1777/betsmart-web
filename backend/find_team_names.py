"""
Database'de Galatasaray ve Fenerbahce hangi isimlerle yazilmis?
"""

from supabase_sync import get_supabase_client

try:
    client = get_supabase_client()
    
    print("="*80)
    print("TAKIM ISMI ARAMA - 393k MAC")
    print("="*80)
    
    # 1. Galatasaray benzeri isimler
    print("\n1. 'Galatasaray' iceren takimlar:")
    
    # Unique team names - home_team
    result = client.rpc('get_unique_teams_like', {'pattern': '%Galata%'}).execute()
    
    # RPC yoksa manuel yap
    if not result.data:
        # Alternatif: DISTINCT ile
        # Ancak bu da yavas olabilir, sadece ilk 20 mac
        matches = client.table('matches').select('home_team,away_team').limit(1000).execute()
        
        teams = set()
        for match in matches.data:
            home = match.get('home_team', '')
            away = match.get('away_team', '')
            
            if 'galata' in home.lower():
                teams.add(home)
            if 'galata' in away.lower():
                teams.add(away)
        
        if teams:
            print(f"   Bulundu: {len(teams)} farkli isim")
            for team in sorted(teams):
                print(f"   - {team}")
        else:
            print("   Bulunamadi")
    
    # 2. Fenerbahce benzeri isimler
    print("\n2. 'Fenerbahce' iceren takimlar:")
    
    matches2 = client.table('matches').select('home_team,away_team').limit(1000).execute()
    
    teams2 = set()
    for match in matches2.data:
        home = match.get('home_team', '')
        away = match.get('away_team', '')
        
        if 'fener' in home.lower():
            teams2.add(home)
        if 'fener' in away.lower():
            teams2.add(away)
    
    if teams2:
        print(f"   Bulundu: {len(teams2)} farkli isim")
        for team in sorted(teams2):
            print(f"   - {team}")
    else:
        print("   Bulunamadi")
    
    # 3. Turkiye ligleri ornekleri
    print("\n3. Turkiye liglerinden ornek takimlar:")
    
    turkish_matches = client.table('matches').select(
        'home_team,away_team,league'
    ).ilike('league', '%Turkiye%').limit(10).execute()
    
    if turkish_matches.data:
        print(f"   Bulundu: {len(turkish_matches.data)} Turkiye maci")
        for match in turkish_matches.data[:5]:
            print(f"   {match['home_team']} vs {match['away_team']}")
            print(f"   Lig: {match['league']}")
    
except Exception as e:
    print(f"\nHATA: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("COZUM:")
print("="*80)
print("""
EGER TAKIM ISIMLERI FARKLI ISE:
   • Fuzzy matching kullan
   • Ornek: "Galatasaray" == "Galatasaray SK"
   • Python: fuzzywuzzy, rapidfuzz
   
VEYA:
   • Team name normalization tablosu olustur
   • Mapping: "Galatasaray SK" -> "Galatasaray"
   • Her sorguda normalize et
""")

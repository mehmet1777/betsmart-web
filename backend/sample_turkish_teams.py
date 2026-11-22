"""
Sadece 100 mactan Turk takimlarini bul
"""

from supabase_sync import get_supabase_client

try:
    client = get_supabase_client()
    
    print("="*80)
    print("SON 100 MACTAN TURK TAKIMLARI")
    print("="*80)
    
    # Son 100 maç
    matches = client.table('matches').select('home_team,away_team,league').order('id', desc=True).limit(100).execute()
    
    print(f"\nToplam: {len(matches.data)} mac\n")
    
    # Turkiye, Galatasaray, Fenerbahce icerenleri filtrele
    turkish_teams = set()
    
    for match in matches.data:
        home = match.get('home_team', '')
        away = match.get('away_team', '')
        league = match.get('league', '')
        
        # Turkiye ligi veya Turk takimi
        if 'türk' in league.lower() or 'turk' in league.lower():
            turkish_teams.add(home)
            turkish_teams.add(away)
        
        if any(keyword in home.lower() for keyword in ['galata', 'fener', 'besiktas', 'trabzon']):
            turkish_teams.add(home)
        
        if any(keyword in away.lower() for keyword in ['galata', 'fener', 'besiktas', 'trabzon']):
            turkish_teams.add(away)
    
    if turkish_teams:
        print(f"Turk takimlari ({len(turkish_teams)} adet):")
        for team in sorted(turkish_teams):
            print(f"  - {team}")
    else:
        print("Son 100 macta Turk takimi yok")
        print("\nOrnek maclar:")
        for i, match in enumerate(matches.data[:10], 1):
            print(f"{i}. {match['home_team']} vs {match['away_team']}")
            print(f"   Lig: {match['league']}")
    
except Exception as e:
    print(f"HATA: {e}")
    import traceback
    traceback.print_exc()

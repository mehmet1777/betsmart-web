from supabase_sync import get_supabase_client

c = get_supabase_client()

# Turkiye ligi
r = c.table('matches').select('home_team,away_team,score,league').eq('league', 'Türkiye').limit(5).execute()
print(f'Turkiye ligi: {len(r.data)} mac')
for m in r.data:
    print(f"{m['home_team']} {m['score']} {m['away_team']}")

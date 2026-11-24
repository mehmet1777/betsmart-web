import os
os.environ['SUPABASE_URL'] = 'https://rrphsslkjnjzbqlbeyyn.supabase.co'
os.environ['SUPABASE_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJycGhzc2xram5qemJxbGJleXluIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzUwNDgwMzUsImV4cCI6MjA1MDYyNDAzNX0.qGEJ0EuMUNxK5Hs5Mg0EXGxs4s4i7WFKblmzPR-B9zk'

from supabase import create_client
import json

supabase = create_client(os.environ['SUPABASE_URL'], os.environ['SUPABASE_KEY'])

# İlk match_details kaydını al
result = supabase.table('match_details').select('*').limit(1).execute()

if result.data:
    match = result.data[0]
    print('=== Match Details Sample ===')
    print(f"Match UUID: {match.get('match_uuid')}")
    print(f"Home: {match.get('home_team')}")
    print(f"Away: {match.get('away_team')}")
    
    # H2H data yapısı
    print('\n=== H2H Data Structure ===')
    h2h = match.get('h2h_data', {})
    if h2h and 'matches' in h2h and len(h2h['matches']) > 0:
        first_h2h = h2h['matches'][0]
        print('Keys:', list(first_h2h.keys()))
        print('Sample:', json.dumps(first_h2h, indent=2, ensure_ascii=False))
    
    # Form data yapısı
    print('\n=== Form Data Structure ===')
    form_home = match.get('form_home', {})
    if form_home and 'matches' in form_home and len(form_home['matches']) > 0:
        first_form = form_home['matches'][0]
        print('Keys:', list(first_form.keys()))
        print('Sample:', json.dumps(first_form, indent=2, ensure_ascii=False))

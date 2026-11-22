"""
SofaScore ve FotMob H2H API test
"""

import requests
import json

print("="*80)
print("SOFASCORE & FOTMOB H2H API TEST")
print("="*80)

# Test match IDs (tahmin)
test_ids = {
    'sofascore': ['11467528', '11467529', '12345678'],  # Rastgele
    'fotmob': ['4172309', '4172310', '4172311']  # Rastgele
}

# 1. SOFASCORE TEST
print("\n" + "="*80)
print("1. SOFASCORE API TEST")
print("="*80)

sofascore_endpoints = [
    "https://api.sofascore.com/api/v1/event/{event_id}/h2h",
    "https://api.sofascore.com/api/v1/event/{event_id}/statistics",
    "https://www.sofascore.com/api/v1/event/{event_id}/h2h",
]

for event_id in test_ids['sofascore'][:1]:
    print(f"\nTest Event ID: {event_id}")
    
    for endpoint_template in sofascore_endpoints:
        endpoint = endpoint_template.format(event_id=event_id)
        print(f"\n{endpoint}")
        
        try:
            response = requests.get(
                endpoint,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    'Accept': 'application/json'
                },
                timeout=10
            )
            
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  JSON OK!")
                    print(f"  Keys: {list(data.keys())[:10]}")
                    
                    # H2H data var mi?
                    if 'events' in data or 'h2h' in data or 'matches' in data:
                        print(f"  BASARILI! H2H data var gibi")
                        break
                except:
                    print(f"  JSON parse edilemedi")
            elif response.status_code == 404:
                print(f"  404 - Event ID gecersiz")
            
        except Exception as e:
            print(f"  ERROR: {type(e).__name__}")

# SofaScore today's matches endpoint
print("\n" + "-"*80)
print("SofaScore - Today's Matches")
print("-"*80)

today_endpoints = [
    "https://api.sofascore.com/api/v1/sport/football/scheduled-events/2024-11-23",
    "https://api.sofascore.com/api/v1/sport/football/events/live",
]

for endpoint in today_endpoints:
    print(f"\n{endpoint}")
    
    try:
        response = requests.get(
            endpoint,
            headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON OK!")
                print(f"Keys: {list(data.keys())[:10]}")
                
                # Event ID'leri ara
                json_str = json.dumps(data)
                if 'id' in json_str:
                    print(f"Event IDs var gibi!")
                    
                    # İlk event'i bul
                    if 'events' in data:
                        events = data['events']
                        if events and len(events) > 0:
                            first_event = events[0]
                            event_id = first_event.get('id')
                            print(f"\nIlk event ID: {event_id}")
                            
                            if event_id:
                                # H2H test et
                                h2h_url = f"https://api.sofascore.com/api/v1/event/{event_id}/h2h"
                                h2h_response = requests.get(h2h_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                                
                                if h2h_response.status_code == 200:
                                    h2h_data = h2h_response.json()
                                    print(f"H2H API BASARILI!")
                                    print(f"H2H Keys: {list(h2h_data.keys())[:10]}")
                                    break
            except:
                pass
                
    except Exception as e:
        print(f"ERROR: {type(e).__name__}")

# 2. FOTMOB TEST
print("\n" + "="*80)
print("2. FOTMOB API TEST")
print("="*80)

fotmob_endpoints = [
    "https://www.fotmob.com/api/matchDetails?matchId={match_id}",
    "https://www.fotmob.com/api/matches?date={date}",
]

for match_id in test_ids['fotmob'][:1]:
    endpoint = fotmob_endpoints[0].format(match_id=match_id)
    print(f"\n{endpoint}")
    
    try:
        response = requests.get(
            endpoint,
            headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'},
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON OK!")
                print(f"Keys: {list(data.keys())[:10]}")
                
                # H2H data var mi?
                if 'h2h' in data or 'headToHead' in data:
                    print(f"BASARILI! H2H data var")
            except:
                print(f"JSON parse edilemedi")
                
    except Exception as e:
        print(f"ERROR: {type(e).__name__}")

# FotMob today's matches
from datetime import datetime
today = datetime.now().strftime("%Y%m%d")

matches_endpoint = f"https://www.fotmob.com/api/matches?date={today}"
print(f"\n{matches_endpoint}")

try:
    response = requests.get(
        matches_endpoint,
        headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'},
        timeout=10
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"JSON OK!")
            print(f"Keys: {list(data.keys())[:10]}")
            
            # Match ID'leri ara
            if 'leagues' in data:
                leagues = data['leagues']
                print(f"{len(leagues)} lig bulundu")
                
                # İlk ligi al
                if leagues and len(leagues) > 0:
                    first_league = leagues[0]
                    if 'matches' in first_league:
                        matches = first_league['matches']
                        if matches and len(matches) > 0:
                            first_match = matches[0]
                            match_id = first_match.get('id')
                            print(f"\nIlk match ID: {match_id}")
                            
                            if match_id:
                                # Match details test et
                                details_url = f"https://www.fotmob.com/api/matchDetails?matchId={match_id}"
                                details_response = requests.get(details_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
                                
                                if details_response.status_code == 200:
                                    details_data = details_response.json()
                                    print(f"Match Details BASARILI!")
                                    print(f"Keys: {list(details_data.keys())[:15]}")
        except:
            pass
            
except Exception as e:
    print(f"ERROR: {type(e).__name__}")

print("\n" + "="*80)
print("SONUC:")
print("="*80)
print("""
BASARILIYSA:
   • API endpoint'leri calisiyor
   • Match ID'leri bulunabilir
   • Fallback olarak kullanilabilir

BASARISIZSA:
   • Rate limiting olabilir
   • API degismis olabilir
   • Alternatif sitelere gec
""")

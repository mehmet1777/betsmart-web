"""
Sahadan Match Details API
Takım karşılaştırmaları, form durumu, H2H verileri
"""
import requests
from datetime import datetime

def fetch_match_details(match_uuid):
    """
    Sahadan'dan maç detaylarını çek
    
    Args:
        match_uuid: Maçın unique ID'si
        
    Returns:
        (success: bool, data: dict, error: str)
    """
    try:
        url = f"https://www.sahadan.com/api/index/match-detail"
        params = {
            'application': 'com.kokteyl.mackolik',
            'language': 'tr',
            'country': 'tr',
            'e': 'sam',
            'match_uuid': match_uuid,
            'a': 'bs'
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Referer': 'https://www.sahadan.com/'
        }
        
        print(f"📡 Match details çekiliyor: {match_uuid[:8]}...")
        
        response = requests.get(url, params=params, headers=headers, timeout=30)
        
        if response.status_code != 200:
            return (False, None, f"API error: {response.status_code}")
        
        data = response.json()
        match_data = data.get('data', {})
        
        if not match_data:
            return (False, None, "No data returned")
        
        # Parse et
        parsed = parse_match_details(match_data)
        
        return (True, parsed, None)
        
    except Exception as e:
        print(f"❌ Match details error: {e}")
        import traceback
        traceback.print_exc()
        return (False, None, str(e))


def parse_match_details(match_data):
    """
    API response'unu parse et, sadece önemli verileri çıkar
    
    Returns:
        dict with h2h_data, form_home, form_away
    """
    result = {
        'match_uuid': match_data.get('match', {}).get('uuid'),
        'home_team': match_data.get('match', {}).get('team_A', {}).get('name'),
        'away_team': match_data.get('match', {}).get('team_B', {}).get('name'),
        'match_datetime': match_data.get('match', {}).get('date_time_utc'),
        'h2h_data': parse_h2h(match_data.get('h2h', {}), 
                               match_data.get('match', {}).get('team_A', {}).get('name'),
                               match_data.get('match', {}).get('team_B', {}).get('name')),
        'form_home': parse_form(match_data.get('forms', {}).get('team_A', {})),
        'form_away': parse_form(match_data.get('forms', {}).get('team_B', {}))
    }
    
    return result


def parse_h2h(h2h_data, home_team, away_team):
    """
    H2H (Aralarındaki Maçlar) verisini parse et
    """
    if not h2h_data:
        return None
    
    matches = h2h_data.get('matches', [])
    
    # İstatistikleri hesapla
    home_wins = 0
    draws = 0
    away_wins = 0
    total_goals = 0
    
    parsed_matches = []
    
    for match in matches[:10]:  # Son 10 maç
        try:
            match_home = match.get('team_A', {}).get('name', '')
            match_away = match.get('team_B', {}).get('name', '')
            score_home = match.get('fts_A', 0)
            score_away = match.get('fts_B', 0)
            half_score_home = match.get('hts_A')  # İlk yarı skoru
            half_score_away = match.get('hts_B')  # İlk yarı skoru
            match_date = match.get('date_time_utc', '')[:10]
            
            # Kim kazandı?
            if match_home == home_team:
                # Ev sahibi bizim ev sahibimiz
                if score_home > score_away:
                    home_wins += 1
                    winner = 'home'
                elif score_home < score_away:
                    away_wins += 1
                    winner = 'away'
                else:
                    draws += 1
                    winner = 'draw'
            else:
                # Ev sahibi bizim deplasman takımımız
                if score_home < score_away:
                    home_wins += 1
                    winner = 'home'
                elif score_home > score_away:
                    away_wins += 1
                    winner = 'away'
                else:
                    draws += 1
                    winner = 'draw'
            
            total_goals += score_home + score_away
            
            parsed_matches.append({
                'date': match_date,
                'home': match_home,
                'away': match_away,
                'score_home': score_home,
                'score_away': score_away,
                'half_score_home': half_score_home,
                'half_score_away': half_score_away,
                'winner': winner
            })
            
        except Exception as e:
            print(f"⚠️ H2H match parse error: {e}")
            continue
    
    return {
        'total_matches': len(parsed_matches),
        'home_wins': home_wins,
        'draws': draws,
        'away_wins': away_wins,
        'avg_goals': round(total_goals / len(parsed_matches), 2) if parsed_matches else 0,
        'matches': parsed_matches
    }


def parse_form(form_data):
    """
    Form durumunu parse et (son 5 maç)
    """
    if not form_data:
        return None
    
    all_comps = form_data.get('all_competitions', {})
    
    if not all_comps:
        return None
    
    # Son maçları parse et
    matches_raw = all_comps.get('matches', [])
    parsed_matches = []
    
    for match in matches_raw[:5]:
        try:
            match_home = match.get('team_A', {}).get('name', '')
            match_away = match.get('team_B', {}).get('name', '')
            score_home = match.get('fts_A', 0)
            score_away = match.get('fts_B', 0)
            half_score_home = match.get('hts_A')  # İlk yarı skoru
            half_score_away = match.get('hts_B')  # İlk yarı skoru
            match_date = match.get('date_time_utc', '')[:10]
            
            parsed_matches.append({
                'date': match_date,
                'home': match_home,
                'away': match_away,
                'score_home': score_home,
                'score_away': score_away,
                'half_score_home': half_score_home,
                'half_score_away': half_score_away
            })
        except:
            continue
    
    return {
        'serie': all_comps.get('serie', ''),  # "WWDLL"
        'goals_for': all_comps.get('goal_pro', 0),
        'goals_against': all_comps.get('goal_against', 0),
        'over_25': all_comps.get('over_2_goals', 0),  # 0-5
        'btts': all_comps.get('two_teams_scored', 0),  # Karşılıklı gol 0-5
        'matches': parsed_matches
    }


# Test
if __name__ == '__main__':
    # Test UUID (Monza vs Fiorentina)
    test_uuid = "7tto7hbwd8o4wifwovvhbk1zo"
    
    print("MATCH DETAILS API TEST")
    print("="*80)
    
    success, data, error = fetch_match_details(test_uuid)
    
    if success:
        print("✅ Başarılı!\n")
        
        import json
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        print("\n" + "="*80)
        print("H2H Özet:")
        h2h = data.get('h2h_data', {})
        if h2h:
            print(f"  Toplam maç: {h2h.get('total_matches')}")
            print(f"  {data['home_team']}: {h2h.get('home_wins')} galibiyet")
            print(f"  Beraberlik: {h2h.get('draws')}")
            print(f"  {data['away_team']}: {h2h.get('away_wins')} galibiyet")
            print(f"  Ortalama gol: {h2h.get('avg_goals')}")
        
        print("\nForm Özet:")
        form_home = data.get('form_home', {})
        form_away = data.get('form_away', {})
        
        if form_home:
            print(f"  {data['home_team']}:")
            print(f"    Serie: {form_home.get('serie')}")
            print(f"    Goller: {form_home.get('goals_for')} atılan, {form_home.get('goals_against')} yenilen")
            print(f"    2.5 Üst: {form_home.get('over_25')}/5")
            print(f"    KG: {form_home.get('btts')}/5")
        
        if form_away:
            print(f"  {data['away_team']}:")
            print(f"    Serie: {form_away.get('serie')}")
            print(f"    Goller: {form_away.get('goals_for')} atılan, {form_away.get('goals_against')} yenilen")
            print(f"    2.5 Üst: {form_away.get('over_25')}/5")
            print(f"    KG: {form_away.get('btts')}/5")
    else:
        print(f"❌ Hata: {error}")

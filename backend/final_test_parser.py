"""Final Test - Parse with ODDS!"""
import json

with open('livedata_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

matches = data.get('m', [])

print("🎯 GEÇMIŞ MAÇLAR - ORANLARLA\n")
print("=" * 80)

parsed = []

for i, match in enumerate(matches[:5]):
    try:
        home_team = match[2]
        away_team = match[4]
        score = match[7]
        match_time = match[16]
        odd_1 = match[18]
        odd_x = match[19]
        odd_2 = match[20]
        under_25 = match[21]
        over_25 = match[22]
        match_date = match[35]
        
        # Lig bilgisi
        league_data = match[36]
        league_name = league_data[1] if league_data and len(league_data) > 1 else "Unknown"
        
        result = {
            'date': match_date,
            'time': match_time,
            'league': league_name,
            'home_team': home_team,
            'away_team': away_team,
            'score': score,
            'odd_1': odd_1,
            'odd_x': odd_x,
            'odd_2': odd_2,
            'under_25': under_25,
            'over_25': over_25
        }
        
        parsed.append(result)
        
        print(f"{i+1}. {league_name}")
        print(f"   📅 {match_date} {match_time}")
        print(f"   ⚽ {home_team} {score} {away_team}")
        print(f"   💰 Oranlar: 1:{odd_1} X:{odd_x} 2:{odd_2}")
        print(f"   📊 Alt/Üst: {under_25}/{over_25}")
        print()
        
    except Exception as e:
        print(f"❌ Hata: {e}")

print("=" * 80)
print(f"✅ {len(parsed)} maç başarıyla parse edildi!")
print("\n🎉 SONUÇ: TÜM VERİLER VAR - ORANLARIYLA!")

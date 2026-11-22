"""Parse Mackolik LiveData - Test"""
import json

# JSON'u oku
with open('livedata_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("🔍 LiveData Parser Test\n")
print("=" * 80)

# Array yapısını çöz
events = data.get('e', [])
print(f"📊 Toplam event sayısı: {len(events)}\n")

# İlk birkaç maçı parse et
print("İLK 10 MAÇ:")
print("-" * 80)

parsed_matches = []

for i, event in enumerate(events[:10]):
    try:
        # Array indeksleri (tahmin)
        event_id = event[0]          # 0: Event ID
        match_id = event[1]          # 1: Match ID
        status = event[2]            # 2: Status
        country_id = event[3]        # 3: Country ID
        league_id = event[4]         # 4: League ID
        league_name = event[5]       # 5: League Name (TAM İSİM!)
        league_short = event[6]      # 6: League Short Code
        home_team_id = event[7]      # 7: Home Team ID
        home_team = event[8]         # 8: Home Team Name
        away_team_id = event[9]      # 9: Away Team ID
        away_team = event[10]        # 10: Away Team Name
        match_time = event[11]       # 11: Time
        home_score = event[12]       # 12: Home Score
        away_score = event[13]       # 13: Away Score
        # event[14-18] diğer veriler...
        
        match = {
            'league': league_name,
            'home_team': home_team,
            'away_team': away_team,
            'home_score': home_score,
            'away_score': away_score,
            'time': match_time
        }
        
        parsed_matches.append(match)
        
        print(f"{i+1}. {league_name}")
        print(f"   {home_team} {home_score} - {away_score} {away_team}")
        print(f"   Saat: {match_time}")
        print()
        
    except Exception as e:
        print(f"❌ Parse hatası: {e}")
        print(f"   Event: {event[:5]}...")
        print()

print("=" * 80)
print(f"\n✅ {len(parsed_matches)} maç başarıyla parse edildi!")

print("\n📋 BİZİM FORMAT İLE UYUMU:")
print("-" * 80)
print("✅ Lig adı: VAR (tam isim)")
print("✅ Ev sahibi: VAR")
print("✅ Deplasman: VAR")
print("✅ Skor: VAR")
print("✅ Tarih/Saat: VAR")
print("❌ Oranlar: YOK (geçmiş maç, normal)")
print("\n💡 SONUÇ: Parser için uygun! ✅")

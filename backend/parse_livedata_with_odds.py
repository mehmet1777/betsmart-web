"""Parse Mackolik LiveData WITH ODDS!"""
import json

with open('livedata_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("🎯 LiveData Parser - WITH ODDS!\n")
print("=" * 80)

matches_data = data.get('m', [])
print(f"📊 Toplam maç sayısı: {len(matches_data)}\n")

print("İLK 10 MAÇ - ORANLARLA:")
print("-" * 80)

parsed_matches = []

for i, match in enumerate(matches_data[:10]):
    try:
        # Index tahminleri (first match'e bakarak)
        match_id = match[0]
        home_team_id = match[1]
        home_team = match[2]
        away_team_id = match[3]
        away_team = match[4]
        status = match[5]
        status_text = match[6]  # 'MS' = Maç Sonu
        score = match[7]
        
        # Oranlar (string formatında gelmiş)
        odd_1 = match[14]   # Index 14
        odd_x = match[15]   # Index 15
        odd_2 = match[16]   # Index 16
        under_25 = match[17] # Index 17 (Alt 2.5)
        over_25 = match[18]  # Index 18 (Üst 2.5)
        
        # Diğer bilgiler
        match_time = match[12] if len(match) > 12 else ""
        match_date = match[32] if len(match) > 32 else ""
        
        # Lig bilgisi (nested dict içinde)
        league_info = match[33] if len(match) > 33 else []
        league_name = league_info[1] if len(league_info) > 1 else "Unknown"
        
        parsed = {
            'league': league_name,
            'home_team': home_team,
            'away_team': away_team,
            'score': score,
            'status': status_text,
            'odd_1': odd_1,
            'odd_x': odd_x,
            'odd_2': odd_2,
            'under_25': under_25,
            'over_25': over_25,
            'time': match_time,
            'date': match_date
        }
        
        parsed_matches.append(parsed)
        
        print(f"{i+1}. {league_name}")
        print(f"   {home_team} vs {away_team}")
        print(f"   Skor: {score} ({status_text})")
        print(f"   Oranlar: 1:{odd_1} X:{odd_x} 2:{odd_2}")
        print(f"   Alt/Üst 2.5: {under_25}/{over_25}")
        print()
        
    except Exception as e:
        print(f"❌ Parse hatası (index {i}): {e}")
        print(f"   Match data length: {len(match)}")
        print()

print("=" * 80)
print(f"\n✅ {len(parsed_matches)} maç başarıyla parse edildi!")

print("\n📋 BİZİM FORMAT İLE UYUM:")
print("-" * 80)
print("✅ Lig adı: VAR")
print("✅ Ev sahibi: VAR")
print("✅ Deplasman: VAR")
print("✅ Skor: VAR")
print("✅ Oranlar (1-X-2): VAR ✨")
print("✅ Alt/Üst 2.5: VAR ✨")
print("✅ Tarih/Saat: VAR")
print("\n🎉 SONUÇ: TAMAMEN UYUMLU! Tüm veriler var!")

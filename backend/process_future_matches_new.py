# YENİ MACKOLIK FORMAT PARSER - LİG KODU BAZLI
# Aynı saatte birden fazla maç desteği

def parse_new_mackolik_format(all_data):
    """
    Yeni Mackolik formatını parse et - Lig kodu bazlı
    
    Aynı saatte birden fazla maç olabilir:
    13:00  1  X  2...
    J-C
    2
    Kawasaki Frontale
    Kashiwa Reysol
    (8 oran)
    J-C              ← Yeni maç, aynı saat!
    2
    Vissel Kobe
    Machida Zelvia
    (8 oran)
    """
    
    lines = [line.strip() for line in all_data.split('\n') if line.strip()]
    
    print(f"📊 Toplam {len(lines)} satır")
    print("\n📋 İLK 100 SATIR:")
    for idx, line in enumerate(lines[:100]):
        print(f"[{idx:2d}] '{line}'")
    print("-" * 50)
    
    future_matches = []
    current_date = ""
    current_time = ""  # Son görülen saat
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Tarih satırı (örn: "11.11.2026")
        if '.' in line and len(line) >= 8 and len(line) <= 12:
            parts = line.split('.')
            if len(parts) == 3 and all(p.isdigit() for p in parts):
                current_date = f"{parts[0]}/{parts[1]}/{parts[2]}"
                print(f"\n📅 Tarih bulundu: {current_date}")
                i += 1
                continue
        
        # Saat satırı mı?
        if ':' in line and len(line) >= 5:
            first_part = line.split()[0] if ' ' in line or '\t' in line else line[:5]
            
            if ':' in first_part and len(first_part) == 5:
                try:
                    hours, mins = first_part.split(':')
                    if hours.isdigit() and mins.isdigit():
                        current_time = first_part
                        print(f"🕐 Saat bulundu: {current_time}")
                        i += 1
                        continue
                except:
                    pass
        
        # Lig kodu satırı mı? (kısa, büyük harfli veya tire içeren)
        # Bu bir maçın başlangıcı demektir
        if len(line) >= 2 and len(line) <= 6:
            # Lig kodu olma ihtimali yüksek
            league_code = line
            
            # Kategori sayısı
            category_idx = i + 1
            if category_idx < len(lines) and lines[category_idx].isdigit():
                team_start = category_idx + 1
            else:
                team_start = category_idx
            
            # Takım isimleri
            if team_start + 1 >= len(lines):
                i += 1
                continue
                
            home_team = lines[team_start].strip()
            away_team = lines[team_start + 1].strip()
            
            # Takım ismi olma kontrolü (çok kısa değil, sayı değil)
            if len(home_team) < 3 or len(away_team) < 3:
                i += 1
                continue
            
            if home_team.isdigit() or away_team.isdigit():
                i += 1
                continue
            
            # Oranlar
            odds_start = team_start + 2
            
            if odds_start + 2 >= len(lines):
                i += 1
                continue
            
            try:
                odd_1_str = lines[odds_start].strip()
                odd_x_str = lines[odds_start + 1].strip()
                odd_2_str = lines[odds_start + 2].strip()
                
                # Oran formatı kontrolü
                def is_valid_odd(s):
                    if s == '-':
                        return True
                    try:
                        val = float(s.replace(',', '.'))
                        return 1.0 <= val <= 100.0
                    except:
                        return False
                
                if not (is_valid_odd(odd_1_str) and is_valid_odd(odd_x_str) and is_valid_odd(odd_2_str)):
                    i += 1
                    continue
                
                # "-" ise 1.01 yap
                odd_1 = 1.01 if odd_1_str == '-' else float(odd_1_str.replace(',', '.'))
                odd_x = 1.01 if odd_x_str == '-' else float(odd_x_str.replace(',', '.'))
                odd_2 = 1.01 if odd_2_str == '-' else float(odd_2_str.replace(',', '.'))
                
                # Tarih + saat
                if current_date and current_time:
                    match_datetime = f"{current_date} {current_time}"
                else:
                    match_datetime = f"11/11/2026 {current_time if current_time else '00:00'}"
                
                # Maçı ekle
                match = {
                    'datetime': match_datetime,
                    'league': league_code,
                    'home_team': home_team,
                    'away_team': away_team,
                    'odd_1': odd_1,
                    'odd_x': odd_x,
                    'odd_2': odd_2,
                    'over_25': 1.01,
                    'under_25': 1.01
                }
                future_matches.append(match)
                
                print(f"✅ Maç: {home_team} vs {away_team}")
                print(f"   Lig: {league_code} | Saat: {match_datetime}")
                print(f"   Oranlar: {odd_1:.2f} / {odd_x:.2f} / {odd_2:.2f}")
                
                # Kalan oranları atla (1-X, 1-2, X-2, Alt, Üst = 5 oran daha)
                i = odds_start + 8
                continue
                
            except (ValueError, IndexError) as e:
                print(f"⚠️ Oran parse hatası satır {i}: {e}")
        
        i += 1
    
    return future_matches


if __name__ == "__main__":
    # Test
    test_data = """
11.11.2026
13:00	1	X	2	1-X	1-2	X-2	Alt	Üst
J-C
2
Kawasaki Frontale
Kashiwa Reysol
2.47
3.24
1.92
1.38
1.10
1.21
2.17
1.29
J-C
2
Vissel Kobe
Machida Zelvia
2.07
2.87
2.48
1.21
1.15
1.32
1.55
1.70
"""
    
    matches = parse_new_mackolik_format(test_data)
    print(f"\n✅ Toplam {len(matches)} maç parse edildi")
    for m in matches:
        print(f"{m['home_team']} vs {m['away_team']}: {m['odd_1']}/{m['odd_x']}/{m['odd_2']}")

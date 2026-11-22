"""
Mackolik LİG görünümünden gelecek maçları parse et
Format: Lig başlıkları ile gruplandırılmış maçlar
"""

import re
from typing import List, Dict

def parse_league_view_format(clipboard_data: str) -> List[Dict]:
    """
    Mackolik LİG sekmesinden kopyalanan veriyi parse et
    
    Mantık:
    1. Lig başlığını bul
    2. Tarih satırını bul
    3. Saat varsa al, yoksa son saati kullan
    4. NAT/2RF/etc lig kodunu atla
    5. Takım isimlerini al (ardışık 2 satır)
    6. Oranları al (sonraki sayısal satırlar)
    """
    
    matches = []
    lines = [l.strip() for l in clipboard_data.strip().split('\n')]
    
    current_league = None
    current_date = None
    current_time = None
    i = 0
    
    print(f"\n🔍 Parsing {len(lines)} lines...")
    
    while i < len(lines):
        line = lines[i]
        
        # Boş satırları atla
        if not line:
            i += 1
            continue
        
        # Header satırlarını atla
        if any(keyword in line.lower() for keyword in ['maç sonucu', 'çifte şans', 'altı/üstü', 'saat\t', 'lig\t']):
            i += 1
            continue
        
        # Lig başlığını yakala (örn: "Avrupa - UEFA Uluslar Ligi")
        if ' - ' in line and len(line) > 10:
            # Kısa kodları (PRD, NAT) atla
            if not (len(line) <= 5 and line.isupper()):
                current_league = line
                print(f"\n📂 Lig: {current_league}")
                i += 1
                continue
        
        # Tarih satırını yakala (örn: "12.11.2026")
        if re.match(r'^\d{2}\.\d{2}\.\d{4}$', line):
            current_date = line
            print(f"📅 Tarih: {current_date}")
            i += 1
            continue
        
        # Saat satırını yakala (örn: "20:00" veya "20:00     1       X...")
        time_match = re.match(r'^(\d{2}:\d{2})', line)
        if time_match:
            current_time = time_match.group(1)
            i += 1
            continue
        
        # Lig kodu satırı (NAT, 2RF, PRD, etc.) - bu takımların başlangıcı demek
        if len(line) <= 5 and line.isupper() and current_date and current_time:
            # Sonraki satır: sayı (maç sayısı) - atla
            i += 1
            if i < len(lines) and lines[i].isdigit():
                i += 1
            
            # Şimdi ardışık 2 takım ismi gelecek
            if i >= len(lines) - 1:
                break
            
            home_team = lines[i].strip()
            i += 1
            away_team = lines[i].strip()
            i += 1
            
            # Takım isimlerinin geçerli olduğunu kontrol et
            if not home_team or not away_team:
                continue
            
            # Oranları topla
            odds = []
            while i < len(lines) and len(odds) < 8:
                try:
                    # Sayı veya tire
                    if lines[i] == '-' or re.match(r'^\d+\.?\d*$', lines[i]):
                        val = lines[i]
                        if val == '-':
                            odds.append(0.0)
                        else:
                            odds.append(float(val))
                        i += 1
                    else:
                        break
                except ValueError:
                    break
            
            # En az 3 oran olmalı (1, X, 2)
            if len(odds) >= 3 and current_league and current_date and current_time:
                match = {
                    'datetime': f"{current_date} {current_time}",
                    'home_team': home_team,
                    'away_team': away_team,
                    'league': current_league,
                    'odd_1': odds[0] if len(odds) > 0 else 0.0,
                    'odd_x': odds[1] if len(odds) > 1 else 0.0,
                    'odd_2': odds[2] if len(odds) > 2 else 0.0,
                    'over_25': odds[7] if len(odds) > 7 else 0.0,
                    'under_25': odds[6] if len(odds) > 6 else 0.0
                }
                matches.append(match)
                print(f"  ✅ {home_team} vs {away_team} - {match['odd_1']}/{match['odd_x']}/{match['odd_2']}")
            
            continue
        
        i += 1
    
    return matches


if __name__ == "__main__":
    # Test
    test_data = """Avrupa - UEFA Uluslar Ligi
12.11.2026
20:00
NAT
1
Ermenistan
Güney Kıbrıs
2.08
2.92
2.74
1.21
1.19
1.41
1.54
1.85
NAT
1
Türkiye
Belçika
3.50
3.62
1.60
1.74
1.11
1.11
2.31
1.33"""
    
    matches = parse_league_view_format(test_data)
    print(f"\n✅ {len(matches)} maç parse edildi")
    for match in matches:
        print(f"  {match['league']}: {match['home_team']} vs {match['away_team']} @ {match['datetime']}")

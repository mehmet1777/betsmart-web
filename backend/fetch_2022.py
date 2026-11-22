"""Mackolik 2022 Maçları"""
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import time

def fetch_past_matches(date_str):
    try:
        dt = datetime.strptime(date_str, "%d.%m.%Y")
        api_date = dt.strftime("%d/%m/%Y")
        url = f"https://vd.mackolik.com/livedata?date={api_date}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Referer': 'https://www.mackolik.com/'
        }
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return []
        data = response.json()
        matches_data = data.get('m', [])
        parsed_matches = []
        for match in matches_data:
            try:
                home_team = match[2]
                away_team = match[4]
                halftime_score = match[7]
                home_score = match[12]
                away_score = match[13]
                fulltime_score = f"{home_score}-{away_score}"
                match_time = match[16]
                odd_1 = match[18]
                odd_x = match[19]
                odd_2 = match[20]
                under_25 = match[21]
                over_25 = match[22]
                match_date = match[35]
                league_data = match[36]
                league_name = league_data[1] if league_data and len(league_data) > 1 else "Unknown"
                if odd_1 == 0 or odd_1 == "0" or odd_1 == "0.00":
                    continue
                parsed_matches.append({
                    'Tarih': match_date,
                    'Saat': match_time,
                    'Lig': league_name,
                    'Ev Sahibi': home_team,
                    'Deplasman': away_team,
                    'IY': halftime_score,
                    'MS': fulltime_score,
                    'MS 1': odd_1,
                    'MS X': odd_x,
                    'MS 2': odd_2,
                    'Alt 2.5': under_25,
                    'Üst 2.5': over_25
                })
            except:
                continue
        return parsed_matches
    except:
        return []

def save_to_excel(all_matches, filename):
    try:
        excel_data = []
        for match in all_matches:
            def safe_odd(value):
                try:
                    val = float(value)
                    return val if val > 0 else 1.01
                except:
                    return 1.01
            row = {
                'Saat': match['Saat'],
                'BOŞ_B': '',
                'Lig': match['Lig'],
                'Mbs': 3,
                'Ev Sahibi': match['Ev Sahibi'],
                'MS': match['MS'],
                'Deplasman': match['Deplasman'],
                'İY': match['IY'],
                '1': safe_odd(match['MS 1']),
                'X': safe_odd(match['MS X']),
                '2': safe_odd(match['MS 2']),
                'Alt 2.5': safe_odd(match['Alt 2.5']),
                'Üst 2.5': safe_odd(match['Üst 2.5'])
            }
            excel_data.append(row)
        df = pd.DataFrame(excel_data)
        columns = ['Saat', 'BOŞ_B', 'Lig', 'Mbs', 'Ev Sahibi', 'MS', 'Deplasman', 'İY', '1', 'X', '2', 'Alt 2.5', 'Üst 2.5']
        df = df[columns]
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        filepath = os.path.join(desktop, filename)
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Maçlar')
            worksheet = writer.sheets['Maçlar']
            worksheet.column_dimensions['A'].width = 10
            worksheet.column_dimensions['B'].width = 0.1
            worksheet.column_dimensions['C'].width = 40
            worksheet.column_dimensions['D'].width = 10
            worksheet.column_dimensions['E'].width = 50
            worksheet.column_dimensions['F'].width = 10
            worksheet.column_dimensions['G'].width = 50
            worksheet.column_dimensions['H'].width = 15
            worksheet.column_dimensions['I'].width = 15
            worksheet.column_dimensions['J'].width = 15
            worksheet.column_dimensions['K'].width = 15
            worksheet.column_dimensions['L'].width = 15
            worksheet.column_dimensions['M'].width = 15
        print(f"✅ 2022 TAMAMLANDI: {len(all_matches)} maç")
        return filepath
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

print("=" * 50)
print("📅 2022 BAŞLIYOR...")
print("=" * 50)
all_matches = []
start_date = datetime(2022, 1, 1)
end_date = datetime(2022, 12, 31)
current_date = start_date
day_count = 0
while current_date <= end_date:
    day_count += 1
    date_str = current_date.strftime("%d.%m.%Y")
    matches = fetch_past_matches(date_str)
    if matches:
        all_matches.extend(matches)
        print(f"[{day_count:3d}] {date_str} ✅ {len(matches)} maç")
    current_date += timedelta(days=1)
    time.sleep(0.3)
print(f"\n🏁 TOPLAM: {len(all_matches)} MAÇ")
if all_matches:
    save_to_excel(all_matches, "mackolik_2022.xlsx")

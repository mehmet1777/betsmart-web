"""
Mackolik LiveData API - Tarih Aralığındaki Tüm Maçları Excel'e Kaydet
01.01.2026 - 10.11.2026
"""
import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import time

def fetch_past_matches(date_str):
    """
    Belirtilen tarihteki maçları çek
    
    Args:
        date_str: Tarih (DD.MM.YYYY formatında)
    
    Returns:
        list: Maç listesi
    """
    try:
        # Tarihi DD/MM/YYYY formatına çevir
        dt = datetime.strptime(date_str, "%d.%m.%Y")
        api_date = dt.strftime("%d/%m/%Y")  # DD/MM/YYYY formatı
        
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
        
        # Parse et
        parsed_matches = []
        
        for match in matches_data:
            try:
                # Temel bilgiler
                home_team = match[2]
                away_team = match[4]
                
                # SKORLAR
                halftime_score = match[7]  # İlk yarı: "1-0"
                home_score = match[12]     # Ev sahibi maç sonucu: 1
                away_score = match[13]     # Deplasman maç sonucu: 1
                fulltime_score = f"{home_score}-{away_score}"  # Maç sonucu: "1-1"
                
                match_time = match[16]
                
                # Oranlar
                odd_1 = match[18]
                odd_x = match[19]
                odd_2 = match[20]
                under_25 = match[21]
                over_25 = match[22]
                
                match_date = match[35]
                
                # Lig bilgisi
                league_data = match[36]
                league_name = league_data[1] if league_data and len(league_data) > 1 else "Unknown"
                
                # 0.00 oranlı maçları filtrele (iddaa'da yok)
                if odd_1 == 0 or odd_1 == "0" or odd_1 == "0.00":
                    continue
                
                parsed_matches.append({
                    'Tarih': match_date,
                    'Saat': match_time,
                    'Lig': league_name,
                    'Ev Sahibi': home_team,
                    'Deplasman': away_team,
                    'IY': halftime_score,      # İlk Yarı
                    'MS': fulltime_score,      # Maç Sonucu
                    'MS 1': odd_1,
                    'MS X': odd_x,
                    'MS 2': odd_2,
                    'Alt 2.5': under_25,
                    'Üst 2.5': over_25
                })
                
            except Exception as e:
                continue
        
        return parsed_matches
        
    except Exception as e:
        return []

def save_to_excel(all_matches, filename):
    """Tüm maçları Excel'e kaydet"""
    try:
        # DataFrame oluştur
        excel_data = []
        
        for match in all_matches:
            # Oranları float'a çevir, yoksa 1.01
            def safe_odd(value):
                try:
                    val = float(value)
                    return val if val > 0 else 1.01
                except:
                    return 1.01
            
            row = {
                'Saat': match['Saat'],
                'BOŞ_B': '',  # B sütunu boş
                'Lig': match['Lig'],
                'Mbs': 3,  # Sabit değer
                'Ev Sahibi': match['Ev Sahibi'],  # E sütunu (başlık yok)
                'MS': match['MS'],  # F sütunu (Maç Sonucu)
                'Deplasman': match['Deplasman'],  # G sütunu (başlık yok)
                'İY': match['IY'],  # H sütunu (İlk Yarı)
                '1': safe_odd(match['MS 1']),
                'X': safe_odd(match['MS X']),
                '2': safe_odd(match['MS 2']),
                'Alt 2.5': safe_odd(match['Alt 2.5']),
                'Üst 2.5': safe_odd(match['Üst 2.5'])
            }
            excel_data.append(row)
        
        df = pd.DataFrame(excel_data)
        
        # Sütun sırası (RESİMDEKİ GİBİ TAM)
        columns = ['Saat', 'BOŞ_B', 'Lig', 'Mbs', 'Ev Sahibi', 'MS', 'Deplasman', 'İY',
                   '1', 'X', '2', 'Alt 2.5', 'Üst 2.5']
        df = df[columns]
        
        # Desktop'a kaydet
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
        filepath = os.path.join(desktop, filename)
        
        # Excel'e yaz
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Maçlar')
            
            # Worksheet al
            worksheet = writer.sheets['Maçlar']
            
            # Sütun genişliklerini ayarla (kullanıcı ayarları)
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
        
        print(f"\n✅ Excel dosyası oluşturuldu!")
        print(f"📂 Konum: {filepath}")
        print(f"📊 TOPLAM {len(all_matches)} maç kaydedildi")
        
        return filepath
        
    except Exception as e:
        print(f"❌ Excel kayıt hatası: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Tarih aralığı
    start_date = datetime.strptime("01.01.2026", "%d.%m.%Y")
    end_date = datetime.strptime("10.11.2026", "%d.%m.%Y")
    
    print("=" * 80)
    print(f"🎯 TOPLU GEÇMIŞ MAÇLAR - EXCEL EXPORT")
    print("=" * 80)
    print(f"📅 Başlangıç: {start_date.strftime('%d.%m.%Y')}")
    print(f"📅 Bitiş: {end_date.strftime('%d.%m.%Y')}")
    print(f"📆 Toplam Gün: {(end_date - start_date).days + 1}")
    print("=" * 80)
    print()
    
    all_matches = []
    current_date = start_date
    day_count = 0
    
    while current_date <= end_date:
        day_count += 1
        date_str = current_date.strftime("%d.%m.%Y")
        
        print(f"[{day_count:3d}] {date_str} çekiliyor...", end=" ", flush=True)
        
        matches = fetch_past_matches(date_str)
        
        if matches:
            all_matches.extend(matches)
            print(f"✅ {len(matches)} maç")
        else:
            print(f"⚪ 0 maç")
        
        # Sonraki güne geç
        current_date += timedelta(days=1)
        
        # API'yi yormamak için bekleme (her istekte 0.5 saniye)
        time.sleep(0.5)
    
    print()
    print("=" * 80)
    print(f"🏁 TOPLAM {len(all_matches)} MAÇ BULUNDU")
    print("=" * 80)
    print()
    
    if all_matches:
        # İlk 5 maç önizleme
        print(f"📋 İLK 5 MAÇ ÖNİZLEME:")
        print("-" * 80)
        for i, match in enumerate(all_matches[:5], 1):
            print(f"{i}. {match['Lig']}")
            print(f"   {match['Ev Sahibi']} vs {match['Deplasman']}")
            print(f"   İY: {match['IY']} → MS: {match['MS']}")
            print(f"   Oranlar: {match['MS 1']} - {match['MS X']} - {match['MS 2']}")
            print()
        
        # Excel'e kaydet
        filename = f"mackolik_2026_temp.xlsx"
        save_to_excel(all_matches, filename)
        
        print()
        print("=" * 80)
        print("🎉 İŞLEM TAMAMLANDI!")
        
    else:
        print("\n❌ Maç bulunamadı veya hata oluştu")

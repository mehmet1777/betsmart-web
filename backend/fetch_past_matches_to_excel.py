"""
Mackolik LiveData API - Geçmiş Maçları Excel'e Kaydet
"""
import requests
import pandas as pd
from datetime import datetime
import os

def fetch_past_matches(date_str):
    """
    Belirtilen tarihteki maçları çek
    
    Args:
        date_str: Tarih (DD.MM.YYYY formatında)
    
    Returns:
        list: Maç listesi
    """
    try:
        # Tarihi MM/DD/YYYY formatına çevir
        dt = datetime.strptime(date_str, "%d.%m.%Y")
        api_date = dt.strftime("%m/%d/%Y")
        
        url = f"https://vd.mackolik.com/livedata?date={api_date}"
        
        print(f"🌐 API'ye istek gönderiliyor...")
        print(f"📅 Tarih: {date_str} → {api_date}")
        print(f"🔗 URL: {url}\n")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Referer': 'https://www.mackolik.com/'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ HTTP Hatası: {response.status_code}")
            return []
        
        data = response.json()
        matches_data = data.get('m', [])
        
        print(f"✅ API yanıtı alındı: {len(matches_data)} maç\n")
        
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
                print(f"⚠️  Parse hatası: {e}")
                continue
        
        return parsed_matches
        
    except Exception as e:
        print(f"❌ Genel hata: {e}")
        import traceback
        traceback.print_exc()
        return []

def save_to_excel(matches, filename):
    """Maçları Excel'e kaydet - Eski format"""
    try:
        # DataFrame oluştur - ESKİ FORMAT
        excel_data = []
        
        for match in matches:
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
        print(f"📊 {len(matches)} maç kaydedildi")
        print(f"💡 Bulunamayan oranlar → 1.01")
        
        return filepath
        
    except Exception as e:
        print(f"❌ Excel kayıt hatası: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    # Test: 01.01.2026
    target_date = "01.01.2026"
    
    print("=" * 80)
    print(f"🎯 GEÇMIŞ MAÇLAR - EXCEL EXPORT")
    print("=" * 80)
    print()
    
    # Maçları çek
    matches = fetch_past_matches(target_date)
    
    if matches:
        print(f"\n📋 İLK 5 MAÇ ÖNİZLEME:")
        print("-" * 80)
        for i, match in enumerate(matches[:5], 1):
            print(f"{i}. {match['Lig']}")
            print(f"   {match['Ev Sahibi']} vs {match['Deplasman']}")
            print(f"   İY: {match['IY']} → MS: {match['MS']}")
            print(f"   Oranlar: {match['MS 1']} - {match['MS X']} - {match['MS 2']}")
            print()
        
        # Excel'e kaydet
        filename = f"mackolik_gecmis_maclar_{target_date.replace('.', '_')}.xlsx"
        save_to_excel(matches, filename)
        
        print("\n" + "=" * 80)
        print("🎉 İŞLEM TAMAMLANDI!")
        
    else:
        print("\n❌ Maç bulunamadı veya hata oluştu")

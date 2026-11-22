"""
Tüm yıl Excel dosyalarını birleştir
"""
import pandas as pd
import os
from openpyxl import load_workbook

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

print("=" * 80)
print("📊 EXCEL DOSYALARI BİRLEŞTİRİLİYOR")
print("=" * 80)
print()

# Dosyaları oku
years = [2020, 2021, 2022, 2023, 2024, 2025]
all_data = []

for year in years:
    filepath = os.path.join(desktop, f"mackolik_{year}.xlsx")
    
    if os.path.exists(filepath):
        print(f"📂 {year} okunuyor...", end=" ", flush=True)
        
        try:
            df = pd.read_excel(filepath, sheet_name='Maçlar')
            row_count = len(df)
            all_data.append(df)
            print(f"✅ {row_count} satır")
        except Exception as e:
            print(f"❌ Hata: {e}")
    else:
        print(f"⚠️  {year} dosyası bulunamadı: {filepath}")

print()
print("=" * 80)

if all_data:
    # Tüm dataframe'leri birleştir
    print("🔄 Birleştiriliyor...")
    combined_df = pd.concat(all_data, ignore_index=True)
    
    total_rows = len(combined_df)
    print(f"✅ Toplam {total_rows} satır birleştirildi")
    
    # Yeni Excel'e kaydet
    output_file = os.path.join(desktop, "mackolik_2020_2025_TÜM.xlsx")
    
    print(f"\n💾 Kaydediliyor: mackolik_2020_2025_TÜM.xlsx")
    print("⏳ Lütfen bekleyin, bu biraz zaman alabilir...")
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        combined_df.to_excel(writer, index=False, sheet_name='Maçlar')
        
        # Sütun genişliklerini ayarla
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
    
    print()
    print("=" * 80)
    print("🎉 BİRLEŞTİRME TAMAMLANDI!")
    print("=" * 80)
    print(f"📂 Dosya: {output_file}")
    print(f"📊 Toplam Satır: {total_rows:,}")
    print()
    
    # Dosya boyutu
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
    print(f"💾 Dosya Boyutu: {file_size:.2f} MB")
    
else:
    print("❌ Birleştirilecek dosya bulunamadı")

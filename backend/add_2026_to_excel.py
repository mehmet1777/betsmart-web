"""
2026 verilerini toplu Excel'e ekle
"""
import pandas as pd
import os

desktop = os.path.join(os.path.expanduser('~'), 'Desktop')

print("=" * 80)
print("📊 2026 VERİLERİ TOPLU EXCEL'E EKLENİYOR")
print("=" * 80)
print()

try:
    # Mevcut toplu Excel'i oku
    main_file = os.path.join(desktop, "mackolik_2020_2025_TÜM.xlsx")
    print(f"📂 Ana dosya okunuyor: mackolik_2020_2025_TÜM.xlsx")
    df_main = pd.read_excel(main_file, sheet_name='Maçlar')
    main_count = len(df_main)
    print(f"✅ {main_count:,} kayıt okundu\n")
    
    # 2026 dosyasını oku
    temp_file = os.path.join(desktop, "mackolik_2026_temp.xlsx")
    print(f"📂 2026 dosyası okunuyor: mackolik_2026_temp.xlsx")
    df_2026 = pd.read_excel(temp_file, sheet_name='Maçlar')
    new_count = len(df_2026)
    print(f"✅ {new_count:,} kayıt okundu\n")
    
    # Birleştir
    print("🔄 Birleştiriliyor...")
    combined_df = pd.concat([df_main, df_2026], ignore_index=True)
    total_count = len(combined_df)
    print(f"✅ Toplam {total_count:,} kayıt\n")
    
    # Yeni dosya adı
    output_file = os.path.join(desktop, "mackolik_2020_2026_TÜM.xlsx")
    
    print(f"💾 Kaydediliyor: mackolik_2020_2026_TÜM.xlsx")
    print("⏳ Lütfen bekleyin...")
    
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
    print(f"📂 Dosya: mackolik_2020_2026_TÜM.xlsx")
    print(f"📊 2020-2025: {main_count:,} maç")
    print(f"📊 2026: {new_count:,} maç")
    print(f"📊 TOPLAM: {total_count:,} maç")
    
    # Dosya boyutu
    file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
    print(f"💾 Dosya Boyutu: {file_size:.2f} MB")
    
    # Geçici dosyayı sil
    print(f"\n🗑️  Geçici dosya siliniyor...")
    os.remove(temp_file)
    print(f"✅ mackolik_2026_temp.xlsx silindi")
    
except Exception as e:
    print(f"❌ Hata: {e}")
    import traceback
    traceback.print_exc()

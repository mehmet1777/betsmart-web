"""
Excel'deki maçları veritabanına aktar
"""
import sqlite3
import pandas as pd
import os
from datetime import datetime

db_path = 'c:/Users/worda/Desktop/BetSmart/betsmart.db'
excel_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'mackolik_2020_2025_TÜM.xlsx')

print("=" * 80)
print("📊 EXCEL → VERİTABANI AKTARIM")
print("=" * 80)
print()

try:
    # Veritabanına bağlan
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Eski kayıtları sil
    print("🗑️  Eski veriler siliniyor...")
    cursor.execute("DELETE FROM matches")
    deleted_count = cursor.rowcount
    print(f"✅ {deleted_count:,} eski kayıt silindi\n")
    
    # Excel'i oku
    print("📂 Excel okunuyor...")
    df = pd.read_excel(excel_path, sheet_name='Maçlar')
    total_rows = len(df)
    print(f"✅ {total_rows:,} satır okundu\n")
    
    # Veritabanı yapısını kontrol et
    cursor.execute("PRAGMA table_info(matches)")
    columns_info = cursor.fetchall()
    
    print("📋 Veritabanı sütunları:")
    for col in columns_info:
        print(f"   - {col[1]} ({col[2]})")
    print()
    
    # Veri aktarımı
    print("💾 Veriler aktarılıyor...")
    imported_count = 0
    error_count = 0
    
    for index, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO matches (
                    time, home_team, away_team, 
                    half_score, score,
                    odd_1, odd_x, odd_2,
                    under, over, league,
                    mbs, is_played
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['Saat'],  # time
                row['Ev Sahibi'],
                row['Deplasman'],
                row['İY'],  # half_score (İlk Yarı)
                row['MS'],  # score (Maç Sonucu)
                float(row['1']) if row['1'] != 1.01 else None,
                float(row['X']) if row['X'] != 1.01 else None,
                float(row['2']) if row['2'] != 1.01 else None,
                float(row['Alt 2.5']) if row['Alt 2.5'] != 1.01 else None,  # under
                float(row['Üst 2.5']) if row['Üst 2.5'] != 1.01 else None,  # over
                row['Lig'],
                3,  # mbs (sabit değer)
                1   # is_played (geçmiş maç, oynanmış)
            ))
            
            imported_count += 1
            
            # İlerleme göster (her 10000 kayıtta)
            if imported_count % 10000 == 0:
                print(f"   ✅ {imported_count:,} kayıt aktarıldı...")
                conn.commit()  # Ara commit
                
        except Exception as e:
            error_count += 1
            if error_count < 5:  # İlk 5 hatayı göster
                print(f"   ⚠️  Hata (satır {index+1}): {e}")
    
    # Son commit
    conn.commit()
    
    print()
    print("=" * 80)
    print("🎉 AKTARIM TAMAMLANDI!")
    print("=" * 80)
    print(f"✅ Aktarılan: {imported_count:,} kayıt")
    print(f"❌ Hata: {error_count:,} kayıt")
    
    # Doğrulama
    cursor.execute("SELECT COUNT(*) FROM matches")
    final_count = cursor.fetchone()[0]
    print(f"📊 Veritabanındaki toplam: {final_count:,} kayıt")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Genel Hata: {e}")
    import traceback
    traceback.print_exc()

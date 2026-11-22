import pandas as pd

# App.py'deki AYNI şekilde yükle
df = pd.read_excel('uploads/bulten.xlsx')
df = df.fillna("")

print("Excel yapısı:")
print(f"Toplam sütun: {len(df.columns)}")
print(f"Toplam satır: {len(df)}\n")

# İlk 3 satırı göster
print("İlk 3 satır (df.values.tolist() ile - app.py'nin kullandığı):")
for i, row in enumerate(df.values.tolist()[:3]):
    print(f"\nSatır {i}:")
    for j in range(min(12, len(row))):
        print(f"  index {j}: {row[j]}")

# Şimdi gerçek veriyi bul
print("\n" + "="*50)
print("GERÇEK VERİ NEREDE?")
print("="*50)

# Her satırda '2-1' gibi skor formatını ve '1.43' gibi oran formatını ara
for row_idx, row in enumerate(df.values.tolist()[:10]):
    for col_idx, val in enumerate(row):
        val_str = str(val)
        # Skor formatı: "2-1", "1-0", vb.
        if '-' in val_str and len(val_str) <= 5:
            print(f"Satır {row_idx}, Sütun {col_idx}: '{val}' (SKOR formatı)")
        # Oran formatı: "1.43", "4.1", vb.
        elif '.' in val_str and val_str.replace('.','').isdigit() and 1.0 <= float(val) <= 50.0:
            print(f"Satır {row_idx}, Sütun {col_idx}: '{val}' (ORAN formatı)")
        # Takım ismi: En az 3 karakter, harf içeriyor
        elif isinstance(val, str) and len(val) >= 3 and any(c.isalpha() for c in val):
            print(f"Satır {row_idx}, Sütun {col_idx}: '{val}' (TAKIM formatı)")

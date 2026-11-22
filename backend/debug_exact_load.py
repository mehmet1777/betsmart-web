import pandas as pd

# App.py'deki ile aynı şekilde yükle
df = pd.read_excel('uploads/bulten.xlsx')
df = df.fillna("")

print(f"Toplam sütun: {len(df.columns)}")
print(f"Toplam satır: {len(df)}")

print("\nİlk 12 sütun başlıkları:")
for i in range(min(12, len(df.columns))):
    print(f"  index {i}: '{df.columns[i]}'")

print("\n2. satır (iloc[1]) - İlk gerçek veri:")
if len(df) > 1:
    row = df.iloc[1]
    for i in range(min(12, len(row))):
        val = row.iloc[i]
        print(f"  index {i}: {val}")

print("\nBu veriler veritabanına şöyle kaydedilecek:")
if len(df) > 1:
    row_data = df.iloc[1].tolist()
    print(f"  home_team (index 5): {row_data[5] if len(row_data) > 5 else 'YOK'}")
    print(f"  score (index 6): {row_data[6] if len(row_data) > 6 else 'YOK'}")
    print(f"  away_team (index 7): {row_data[7] if len(row_data) > 7 else 'YOK'}")
    print(f"  odd_1 (index 9): {row_data[9] if len(row_data) > 9 else 'YOK'}")
    print(f"  odd_x (index 10): {row_data[10] if len(row_data) > 10 else 'YOK'}")
    print(f"  odd_2 (index 11): {row_data[11] if len(row_data) > 11 else 'YOK'}")

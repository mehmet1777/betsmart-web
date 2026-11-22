"""
Excel dosyasındaki sütun genişliklerini oku
"""
from openpyxl import load_workbook
import os

# Excel dosyası
desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
filepath = os.path.join(desktop, 'mackolik_gecmis_01_01_2026_to_10_11_2026.xlsx')

print(f"📂 Dosya: {filepath}\n")

# Workbook aç
wb = load_workbook(filepath)
ws = wb['Maçlar']

print("=" * 80)
print("SÜTUN GENİŞLİKLERİ")
print("=" * 80)

# Sütun harfleri
columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P']

widths = {}
for col in columns:
    width = ws.column_dimensions[col].width
    if width:
        widths[col] = width
        print(f"worksheet.column_dimensions['{col}'].width = {width:.1f}")

print()
print("=" * 80)
print("PYTHON KODU İÇİN:")
print("=" * 80)
print()

for col, width in widths.items():
    print(f"            worksheet.column_dimensions['{col}'].width = {width:.1f}")

wb.close()

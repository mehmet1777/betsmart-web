"""Show first match raw data"""
import json

with open('livedata_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

matches = data.get('m', [])
first_match = matches[0]

print("İLK MAÇ - RAW DATA:")
print("=" * 80)

for i, field in enumerate(first_match):
    value_str = str(field)[:100]  # İlk 100 karakter
    print(f"[{i:2d}] {type(field).__name__:10s} = {value_str}")

print("\n" + "=" * 80)
print(f"Toplam field: {len(first_match)}")

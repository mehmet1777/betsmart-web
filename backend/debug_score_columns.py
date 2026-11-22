"""
Mackolik API - Skor sütunlarını bul
"""
import requests
import json

url = "https://vd.mackolik.com/livedata?date=01/01/2026"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': '*/*',
    'Referer': 'https://www.mackolik.com/'
}

response = requests.get(url, headers=headers, timeout=15)
data = response.json()

# İlk maçı al
first_match = data['m'][0]

print("=" * 80)
print("İLK MAÇ VERİLERİ - TÜM İNDEKSLER")
print("=" * 80)
print()

for i, value in enumerate(first_match):
    print(f"[{i:3d}] = {value}")

print()
print("=" * 80)
print("İLK 5 MAÇ - İLGİLİ ALANLAR")
print("=" * 80)

for idx, match in enumerate(data['m'][:5], 1):
    print(f"\n{idx}. {match[2]} vs {match[4]}")
    print(f"   [7]  = {match[7]}")  # Bildiğimiz skor
    print(f"   [8]  = {match[8]}")  
    print(f"   [9]  = {match[9]}")  
    print(f"   [10] = {match[10]}")
    print(f"   [11] = {match[11]}")
    print(f"   [12] = {match[12]}")
    print(f"   [13] = {match[13]}")
    print(f"   [14] = {match[14]}")
    print(f"   [15] = {match[15]}")

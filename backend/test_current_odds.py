"""
Şu anda sistemde hangi oranlar var test et
"""
from supabase_sync import get_supabase_client

client = get_supabase_client()

# future_matches tablosundan ilk 5 maçı al
result = client.table('future_matches').select('*').limit(5).execute()

print("SUPABASE'DEKİ MEVCUT ORANLAR:")
print("="*80)

if result.data:
    for match in result.data:
        home = match.get('home_team', '')
        away = match.get('away_team', '')
        odd_1 = match.get('odd_1', '-')
        odd_x = match.get('odd_x', '-')
        odd_2 = match.get('odd_2', '-')
        
        print(f"\nMac: {home} vs {away}")
        print(f"  Oranlar: 1={odd_1}, X={odd_x}, 2={odd_2}")
else:
    print("Veritabaninda mac yok")

print("\n" + "="*80)
print("\nSAHADAN API'DEN AYNI MACLARI ÇEK VE KARSILASTIR:")
print("="*80)

from sahadan_api import fetch_sahadan_matches

success, matches, error = fetch_sahadan_matches(days_ahead=1)

if success and matches:
    # İlk 3 maçı göster
    for match in matches[:3]:
        home = match.get('home_team', '')
        away = match.get('away_team', '')
        odd_1 = match.get('odd_1', '-')
        odd_x = match.get('odd_x', '-')
        odd_2 = match.get('odd_2', '-')
        
        print(f"\nMac: {home} vs {away}")
        print(f"  options[0] Oranlar: 1={odd_1}, X={odd_x}, 2={odd_2}")

print("\n" + "="*80)
print("KARSILASTIRMA:")
print("  Eger Supabase'deki oranlar daha YUKSEK ise -> OLEY cekiyor")
print("  Eger Supabase'deki oranlar daha DUSUK ise -> NESINE cekiyor")

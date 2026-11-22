"""
Sahadan'dan Nesine oranlarını çek, Supabase'e yaz, doğrula
"""
from sahadan_api import fetch_sahadan_matches
from supabase_sync import sync_matches_to_supabase, get_supabase_client

print("NESINE ORANLARI TEST - SAHADAN -> SUPABASE")
print("="*80)

# 1. Sahadan'dan çek
print("\n1. Sahadan API'den cekiliyor (options[0] = Nesine)...")
success, matches, error = fetch_sahadan_matches(days_ahead=1)

if not success or not matches:
    print(f"HATA: {error}")
    exit(1)

print(f"   {len(matches)} mac bulundu")

# İlk maçı göster
first_match = matches[0]
print(f"\nOrnek mac:")
print(f"  {first_match['home_team']} vs {first_match['away_team']}")
print(f"  Nesine oranlari: 1={first_match['odd_1']}, X={first_match['odd_x']}, 2={first_match['odd_2']}")

# 2. Supabase'e kaydet
print("\n2. Supabase'e kaydediliyor...")
success_count, errors = sync_matches_to_supabase(matches[:10])  # Sadece ilk 10'u test için

print(f"   {success_count} mac kaydedildi")

# 3. Supabase'den oku ve doğrula
print("\n3. Supabase'den kontrol ediliyor...")
client = get_supabase_client()

home_team = first_match['home_team']
away_team = first_match['away_team']

result = client.table('future_matches').select('*').eq(
    'home_team', home_team
).eq('away_team', away_team).execute()

if result.data and len(result.data) > 0:
    db_match = result.data[0]
    
    print(f"\nSupabase'deki oranlar:")
    print(f"  1={db_match['odd_1']}, X={db_match['odd_x']}, 2={db_match['odd_2']}")
    
    # Karşılaştır
    if (abs(float(db_match['odd_1']) - float(first_match['odd_1'])) < 0.01 and
        abs(float(db_match['odd_x']) - float(first_match['odd_x'])) < 0.01 and
        abs(float(db_match['odd_2']) - float(first_match['odd_2'])) < 0.01):
        print("\n✅ BASARILI: Supabase'e NESINE oranlari kaydedildi!")
    else:
        print("\n⚠️  UYARI: Oranlar farkli!")
        print("   Sahadan'dan gelen:", first_match['odd_1'], first_match['odd_x'], first_match['odd_2'])
        print("   Supabase'deki:", db_match['odd_1'], db_match['odd_x'], db_match['odd_2'])
else:
    print("Mac Supabase'de bulunamadi")

print("\n" + "="*80)
print("SONUC: Sahadan API options[0] kullanarak NESINE oranlarini cekiyor.")
print("       Telegram /yeniveri komutunu calistirinca NESINE oranlari gelir.")

"""
Basit test - Supabase vs Sahadan oran karşılaştırması
"""
from sahadan_api import fetch_sahadan_matches
from supabase_sync import get_supabase_client

print("ORAN KARSILASTIRMA - SUPABASE vs SAHADAN")
print("="*80)

# Sahadan'dan bugünkü maçları çek
print("\n1. Sahadan'dan bugunku maclari cekiyor (options[0] = Nesine)...")
success, sahadan_matches, error = fetch_sahadan_matches(days_ahead=2)

if not success:
    print(f"Hata: {error}")
    exit(1)

print(f"   {len(sahadan_matches)} mac bulundu")

# İlk 3 maçı göster
print("\nSAHADAN'DAN GELEN ORANLAR (Nesine - options[0]):")
print("-"*80)
for i, match in enumerate(sahadan_matches[:3], 1):
    print(f"{i}. {match['home_team']} vs {match['away_team']}")
    print(f"   1={match['odd_1']:.2f}, X={match['odd_x']:.2f}, 2={match['odd_2']:.2f}")

# Supabase'den aynı maçları al
print("\n2. Supabase'den ayni maclari cekiyor...")
client = get_supabase_client()

print("\nSUPABASE'DEKİ ORANLAR:")
print("-"*80)

for i, sahadan_match in enumerate(sahadan_matches[:3], 1):
    result = client.table('future_matches').select('*').eq(
        'home_team', sahadan_match['home_team']
    ).eq('away_team', sahadan_match['away_team']).execute()
    
    if result.data and len(result.data) > 0:
        db_match = result.data[0]
        print(f"{i}. {db_match['home_team']} vs {db_match['away_team']}")
        print(f"   1={db_match['odd_1']:.2f}, X={db_match['odd_x']:.2f}, 2={db_match['odd_2']:.2f}")
        
        # Fark hesapla
        diff_1 = db_match['odd_1'] - sahadan_match['odd_1']
        diff_x = db_match['odd_x'] - sahadan_match['odd_x']
        diff_2 = db_match['odd_2'] - sahadan_match['odd_2']
        
        print(f"   FARK: 1={diff_1:+.2f}, X={diff_x:+.2f}, 2={diff_2:+.2f}")
        
        # Yorum
        if abs(diff_1) > 0.15 and diff_1 > 0:
            print(f"   >> Supabase DAHA YUKSEK - OLEY oranlari var!")
        elif abs(diff_1) < 0.05:
            print(f"   >> Ayni - NESINE kullaniliyor")
    else:
        print(f"{i}. Supabase'de bulunamadi")
    print()

print("="*80)
print("SONUC:")
print("  - Eger Supabase oranlari ~0.20 daha yuksekse -> OLEY")
print("  - Eger Supabase ile Sahadan ayni ise -> NESINE")
print("  - Oran takipci her 10dk Sahadan options[0] cekiyor (Nesine)")

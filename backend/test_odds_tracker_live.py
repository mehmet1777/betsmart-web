"""
Oran takipçiyi manuel çalıştır, hangi oranları çektiğini gör
"""
from sahadan_api import fetch_sahadan_matches
from supabase_sync import get_supabase_client

print("ORAN TAKIPCI TEST - CANLI CEKIM")
print("="*80)

# 1. Supabase'den mevcut bir maçı al
client = get_supabase_client()
existing_matches = client.table('future_matches').select('*').limit(5).execute()

if not existing_matches.data:
    print("Supabase'de mac yok")
    exit(1)

first_match = existing_matches.data[0]

print("\nSupabase'deki bir mac:")
print(f"  {first_match['home_team']} vs {first_match['away_team']}")
print(f"  Mevcut oranlar: 1={first_match['odd_1']}, X={first_match['odd_x']}, 2={first_match['odd_2']}")

# 2. Sahadan'dan aynı günün maçlarını çek
print("\nSahadan'dan ayni gun maclari cekiliyor...")
success, new_matches, error = fetch_sahadan_matches(days_ahead=1)

if not success:
    print(f"Hata: {error}")
    exit(1)

print(f"  {len(new_matches)} mac bulundu")

# 3. Aynı maçı bul
target_match = None
for match in new_matches:
    if (match['home_team'] == first_match['home_team'] and 
        match['away_team'] == first_match['away_team']):
        target_match = match
        break

if target_match:
    print(f"\nAyni mac Sahadan'da bulundu:")
    print(f"  {target_match['home_team']} vs {target_match['away_team']}")
    print(f"  Yeni oranlar (options[0]): 1={target_match['odd_1']}, X={target_match['odd_x']}, 2={target_match['odd_2']}")
    
    # Karşılaştır
    print(f"\nKARSILASTIRMA:")
    print(f"  Supabase: 1={first_match['odd_1']:.2f}, X={first_match['odd_x']:.2f}, 2={first_match['odd_2']:.2f}")
    print(f"  Sahadan:  1={target_match['odd_1']:.2f}, X={target_match['odd_x']:.2f}, 2={target_match['odd_2']:.2f}")
    
    # Farkları hesapla
    diff_1 = target_match['odd_1'] - first_match['odd_1']
    diff_x = target_match['odd_x'] - first_match['odd_x']
    diff_2 = target_match['odd_2'] - first_match['odd_2']
    
    print(f"  Fark:     1={diff_1:+.2f}, X={diff_x:+.2f}, 2={diff_2:+.2f}")
    
    # Analiz
    if abs(diff_1) < 0.01 and abs(diff_x) < 0.01 and abs(diff_2) < 0.01:
        print(f"\n  SONUC: Oranlar ayni - Nesine kullaniliyor ✅")
    elif diff_1 > 0.15 and diff_x > 0.15 and diff_2 > 0.15:
        print(f"\n  SONUC: Supabase'deki oranlar DAHA YUKSEK")
        print(f"         Supabase'de OLEY, Sahadan NESINE cekiyor")
        print(f"         Yani oran takipci guncelledikce Nesine'ye donecek")
    elif diff_1 < -0.15 and diff_x < -0.15 and diff_2 < -0.15:
        print(f"\n  SONUC: Sahadan'dan gelen oranlar DAHA YUKSEK")
        print(f"         Bu normal degil, options[1] kullaniliyor olabilir")
    else:
        print(f"\n  SONUC: Kucuk degisiklikler, oran guncellenmis olabilir")
else:
    print(f"\nAyni mac Sahadan'da bulunamadi")
    print(f"(Tarih veya takim isimleri farkli olabilir)")

print("\n" + "="*80)
print("NOT: Oran takipci her 10 dakikada Sahadan options[0] (Nesine) cekiyor.")
print("     Supabase'deki Oley oranlari sonraki guncellemede Nesine'ye donecek.")

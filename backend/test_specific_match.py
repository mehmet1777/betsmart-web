"""
Belirli bir maçı bul ve oranlarını karşılaştır
Atl Goianiense vs Vila Nova
"""
from sahadan_api import fetch_sahadan_matches
from supabase_sync import get_supabase_client

print("BELIRLI MAC TEST - Atl Goianiense vs Vila Nova")
print("="*80)

# 1. Supabase'de bu maçı ara
print("\n1. Supabase'de araniyor...")
client = get_supabase_client()

# Takım isimlerinde varyasyonlar olabilir
search_terms = [
    ('Atl Goianiense', 'Vila Nova'),
    ('Atletico Goianiense', 'Vila Nova'),
    ('Goianiense', 'Vila Nova'),
    ('Atl GO', 'Vila Nova'),
]

db_match = None
for home_search, away_search in search_terms:
    result = client.table('future_matches').select('*').ilike(
        'home_team', f'%{home_search}%'
    ).ilike('away_team', f'%{away_search}%').execute()
    
    if result.data and len(result.data) > 0:
        db_match = result.data[0]
        print(f"   Bulundu: {db_match['home_team']} vs {db_match['away_team']}")
        break

if db_match:
    print(f"\nSUPABASE'DEKİ ORANLAR:")
    print(f"  1={db_match['odd_1']}, X={db_match['odd_x']}, 2={db_match['odd_2']}")
    print(f"  Tarih: {db_match['datetime']}")
else:
    print("   Supabase'de bulunamadi")

# 2. Sahadan'dan çek
print("\n2. Sahadan'dan tum maclari cekiyor...")
success, sahadan_matches, error = fetch_sahadan_matches(days_ahead=3)

if not success:
    print(f"Hata: {error}")
    exit(1)

print(f"   {len(sahadan_matches)} mac bulundu")

# 3. Bu maçı Sahadan'da bul
print("\n3. Sahadan'da araniyor...")
sahadan_match = None

for match in sahadan_matches:
    home = match['home_team'].lower()
    away = match['away_team'].lower()
    
    # Esnek arama
    if (('goianiense' in home or 'goian' in home or 'atl' in home) and 
        ('vila' in away or 'nova' in away)):
        sahadan_match = match
        print(f"   Bulundu: {match['home_team']} vs {match['away_team']}")
        break

if sahadan_match:
    print(f"\nSAHADAN'DAN GELEN ORANLAR (options[0]):")
    print(f"  1={sahadan_match['odd_1']}, X={sahadan_match['odd_x']}, 2={sahadan_match['odd_2']}")
    print(f"  Tarih: {sahadan_match['datetime']}")
    
    # Resimde görünen oranlar
    print(f"\nRESİMDEKİ ORANLAR:")
    print(f"  1=1.75, X=2.79, 2=3.27")
    
    # Karşılaştırma
    print("\n" + "="*80)
    print("KARSILASTIRMA:")
    print("="*80)
    
    if db_match:
        print(f"\nSupabase:  1={db_match['odd_1']:.2f}, X={db_match['odd_x']:.2f}, 2={db_match['odd_2']:.2f}")
    
    print(f"Sahadan:   1={sahadan_match['odd_1']:.2f}, X={sahadan_match['odd_x']:.2f}, 2={sahadan_match['odd_2']:.2f}")
    print(f"Resim:     1=1.75, X=2.79, 2=3.27")
    
    # Analiz
    print("\n" + "-"*80)
    
    # Sahadan ile resmi karşılaştır
    if abs(sahadan_match['odd_1'] - 1.75) < 0.05:
        print("✅ Sahadan options[0] = Resimdeki oranlar")
        print("   options[0] = Nesine veya ayni kaynak")
    elif abs(sahadan_match['odd_1'] - 1.75) > 0.15:
        print("❌ Sahadan options[0] != Resimdeki oranlar")
        print(f"   Fark: {abs(sahadan_match['odd_1'] - 1.75):.2f}")
        
        # options[1] kontrol et
        print("\n   options[1] kontrolu yapiliyor...")
        print("   (Sahadan API'den ayni mac icin options[1] gerekiyor)")
    
    if db_match:
        print("\n" + "-"*80)
        
        # Supabase ile resmi karşılaştır  
        if abs(db_match['odd_1'] - 1.75) < 0.05:
            print("✅ Supabase = Resimdeki oranlar (Nesine)")
        elif abs(db_match['odd_1'] - 1.75) > 0.15:
            diff = db_match['odd_1'] - 1.75
            print(f"❌ Supabase != Resimdeki oranlar")
            print(f"   Fark: {diff:+.2f}")
            
            if diff > 0.15:
                print("   Supabase'de DAHA YUKSEK oranlar var")
                print("   Supabase'de OLEY, resimde NESINE")
            elif diff < -0.15:
                print("   Supabase'de DAHA DUSUK oranlar var")
                print("   Bu normal degil, kontrol et!")

else:
    print("   Sahadan'da bulunamadi")

print("\n" + "="*80)

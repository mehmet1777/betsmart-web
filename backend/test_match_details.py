"""
Match Details sistemini hızlı test et
"""
from match_details_api import fetch_match_details
from match_details_sync import sync_match_details_to_supabase

print("MATCH DETAILS - HIZLI TEST")
print("="*80)

# Test UUID (Monza vs Fiorentina)
test_uuid = "7tto7hbwd8o4wifwovvhbk1zo"

print("\n1. API Test...")
success, data, error = fetch_match_details(test_uuid)

if success:
    print("   ✅ API çalışıyor")
    print(f"   Maç: {data['home_team']} vs {data['away_team']}")
    
    h2h = data.get('h2h_data', {})
    print(f"   H2H: {h2h.get('total_matches')} maç bulundu")
    
    form_home = data.get('form_home', {})
    print(f"   Form: {form_home.get('serie') if form_home else 'N/A'}")
else:
    print(f"   ❌ API hatası: {error}")
    exit(1)

print("\n2. Supabase Test...")
success, error = sync_match_details_to_supabase(test_uuid, force_update=True)

if success:
    print("   ✅ Supabase'e kaydedildi")
    print("\n3. Kontrol Et:")
    print("   https://supabase.com → Table Editor → match_details")
else:
    print(f"   ❌ Supabase hatası: {error}")

print("\n" + "="*80)
print("TEST TAMAMLANDI")
print("\nŞimdi ne yapmalısın?")
print("  1. Supabase'de match_details tablosunu aç")
print("  2. match_uuid: 7tto7hbwd8o4wifwovvhbk1zo aramasını yap")
print("  3. h2h_data ve form_home kolonlarına bak (JSON)")

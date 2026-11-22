"""
matches tablosunu incele - geçmiş maçlar burada mı?
"""
from supabase_sync import get_supabase_client

client = get_supabase_client()

print("=" * 70)
print("MATCHES TABLOSU ANALİZİ")
print("=" * 70)
print()

# Tablo yapısı
print("[1] Tablo Yapısı")
result = client.table('matches').select('*').limit(1).execute()
if result.data:
    print(f"  Columns: {list(result.data[0].keys())}")
print()

# Örnek kayıt
print("[2] Örnek Kayıtlar")
result = client.table('matches').select('*').limit(5).execute()
for i, match in enumerate(result.data):
    print(f"{i+1}. {match.get('date')} - {match.get('home_team')} vs {match.get('away_team')}")
    print(f"   Skor: {match.get('score')}, Lig: {match.get('league')}")
print()

# Skorlu maçlar var mı? (bitmiş maçlar)
print("[3] Skorlu Maçlar (Bitmiş)")
result = client.table('matches').select('*').not_.is_('score', 'null').limit(10).execute()
print(f"  Skorlu maç sayısı (sample): {len(result.data)}")
if result.data:
    for i, match in enumerate(result.data[:3]):
        print(f"  {i+1}. {match.get('date')} - {match.get('home_team')} vs {match.get('away_team')}")
        print(f"     Skor: {match.get('score')}")
print()

# Hannover araması
print("[4] Hannover 96 Araması")
result = client.table('matches').select('*').or_(
    'home_team.ilike.%Hannover%,away_team.ilike.%Hannover%'
).limit(10).execute()
print(f"  Bulunan: {len(result.data)} maç")
if result.data:
    for i, match in enumerate(result.data[:5]):
        print(f"  {i+1}. {match.get('date')} - {match.get('home_team')} vs {match.get('away_team')}")
        print(f"     Skor: {match.get('score')}, Lig: {match.get('league')}")
else:
    print("  ❌ HANNOVER BULUNAMADI!")
print()

print("=" * 70)

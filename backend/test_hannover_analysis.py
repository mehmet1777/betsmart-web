"""
Hannover - Greuther Fürth maçı için analiz testi
Oranlar: 1.71 - 3.82 - 4.04
"""
from supabase_sync import get_supabase_client

client = get_supabase_client()

odd_1 = 1.71
odd_x = 3.82
odd_2 = 4.04

print("=" * 70)
print("HANNOVER 96 vs GREUTHER FÜRTH - ANALİZ TESTİ")
print("=" * 70)
print(f"Oranlar: {odd_1} - {odd_x} - {odd_2}")
print()

# Test 1: ±0.01 tolerans (mevcut kod)
print("[1] ±0.01 tolerans (mevcut)")
result = client.table('matches').select('*').filter('odd_1', 'gte', odd_1 - 0.01).filter('odd_1', 'lte', odd_1 + 0.01).filter('odd_x', 'gte', odd_x - 0.01).filter('odd_x', 'lte', odd_x + 0.01).filter('odd_2', 'gte', odd_2 - 0.01).filter('odd_2', 'lte', odd_2 + 0.01).not_.is_('score', 'null').limit(100).execute()
print(f"  Bulunan: {len(result.data)} maç")
print()

# Test 2: ±0.05 tolerans
print("[2] ±0.05 tolerans")
result = client.table('matches').select('*').filter('odd_1', 'gte', odd_1 - 0.05).filter('odd_1', 'lte', odd_1 + 0.05).filter('odd_x', 'gte', odd_x - 0.05).filter('odd_x', 'lte', odd_x + 0.05).filter('odd_2', 'gte', odd_2 - 0.05).filter('odd_2', 'lte', odd_2 + 0.05).not_.is_('score', 'null').limit(100).execute()
print(f"  Bulunan: {len(result.data)} maç")
if result.data:
    for i, match in enumerate(result.data[:5]):
        print(f"  {i+1}. {match.get('home_team')} vs {match.get('away_team')}")
        print(f"     Oranlar: {match.get('odd_1')} - {match.get('odd_x')} - {match.get('odd_2')}")
        print(f"     Skor: {match.get('score')}")
print()

# Test 3: ±0.10 tolerans
print("[3] ±0.10 tolerans")
result = client.table('matches').select('*').filter('odd_1', 'gte', odd_1 - 0.10).filter('odd_1', 'lte', odd_1 + 0.10).filter('odd_x', 'gte', odd_x - 0.10).filter('odd_x', 'lte', odd_x + 0.10).filter('odd_2', 'gte', odd_2 - 0.10).filter('odd_2', 'lte', odd_2 + 0.10).not_.is_('score', 'null').limit(100).execute()
print(f"  Bulunan: {len(result.data)} maç")
if result.data:
    for i, match in enumerate(result.data[:5]):
        print(f"  {i+1}. {match.get('home_team')} vs {match.get('away_team')}")
        print(f"     Oranlar: {match.get('odd_1')} - {match.get('odd_x')} - {match.get('odd_2')}")
        print(f"     Skor: {match.get('score')}")
print()

# Test 4: ±0.20 tolerans
print("[4] ±0.20 tolerans")
result = client.table('matches').select('*').filter('odd_1', 'gte', odd_1 - 0.20).filter('odd_1', 'lte', odd_1 + 0.20).filter('odd_x', 'gte', odd_x - 0.20).filter('odd_x', 'lte', odd_x + 0.20).filter('odd_2', 'gte', odd_2 - 0.20).filter('odd_2', 'lte', odd_2 + 0.20).not_.is_('score', 'null').limit(100).execute()
print(f"  Bulunan: {len(result.data)} maç")
if result.data:
    for i, match in enumerate(result.data[:5]):
        print(f"  {i+1}. {match.get('home_team')} vs {match.get('away_team')}")
        print(f"     Oranlar: {match.get('odd_1')} - {match.get('odd_x')} - {match.get('odd_2')}")
        print(f"     Skor: {match.get('score')}")
print()

print("=" * 70)
print("ÖNERİ:")
print("  ±0.01-0.02 çok dar → hiç sonuç yok")
print("  ±0.10-0.20 ideal → yeterli sonuç bulunur")
print("=" * 70)

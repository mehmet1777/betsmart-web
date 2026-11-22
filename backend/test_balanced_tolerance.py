"""
Dengeli tolerans testi: ±0.05 ve ±0.15
"""
from supabase_sync import get_supabase_client

client = get_supabase_client()

odd_1 = 1.71
odd_x = 3.82
odd_2 = 4.04

print("=" * 70)
print("DENGELİ TOLERANS TESTİ")
print("=" * 70)
print(f"Oranlar: {odd_1} - {odd_x} - {odd_2}")
print()

# Exact: ±0.05
print("[1] AYNI ORANLAR (±0.05)")
exact = client.table('matches').select('*').filter('odd_1', 'gte', odd_1 - 0.05).filter('odd_1', 'lte', odd_1 + 0.05).filter('odd_x', 'gte', odd_x - 0.05).filter('odd_x', 'lte', odd_x + 0.05).filter('odd_2', 'gte', odd_2 - 0.05).filter('odd_2', 'lte', odd_2 + 0.05).not_.is_('score', 'null').limit(100).execute()

print(f"  Bulunan: {len(exact.data)} maç")
if exact.data:
    for i, m in enumerate(exact.data[:3]):
        print(f"  {i+1}. {m['home_team']} vs {m['away_team']}")
        print(f"     {m['odd_1']} - {m['odd_x']} - {m['odd_2']} → {m['score']}")
print()

# Similar: ±0.15
print("[2] BENZER ORANLAR (±0.15)")
similar = client.table('matches').select('*').filter('odd_1', 'gte', odd_1 - 0.15).filter('odd_1', 'lte', odd_1 + 0.15).filter('odd_x', 'gte', odd_x - 0.15).filter('odd_x', 'lte', odd_x + 0.15).filter('odd_2', 'gte', odd_2 - 0.15).filter('odd_2', 'lte', odd_2 + 0.15).not_.is_('score', 'null').limit(100).execute()

exact_ids = [m['id'] for m in exact.data]
similar_only = [m for m in similar.data if m['id'] not in exact_ids]

print(f"  Bulunan (exact hariç): {len(similar_only)} maç")
if similar_only:
    for i, m in enumerate(similar_only[:3]):
        print(f"  {i+1}. {m['home_team']} vs {m['away_team']}")
        print(f"     {m['odd_1']} - {m['odd_x']} - {m['odd_2']} → {m['score']}")
print()

total = len(exact.data) + len(similar_only)
print(f"TOPLAM: {total} maç ({len(exact.data)} aynı + {len(similar_only)} benzer)")

if total >= 20:
    print("✅ YETERLİ SONUÇ - Analiz çalışacak")
elif total >= 10:
    print("⚠️  ORTA SEVİYE - Çalışır ama daha fazla olabilir")
else:
    print("❌ YETERSİZ - Tolerans daha artırılmalı")
print("=" * 70)

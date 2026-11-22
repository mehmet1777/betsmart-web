"""
Yeni tolerans değerleriyle test - ±0.10 ve ±0.20
"""
from supabase_sync import get_supabase_client

client = get_supabase_client()

# Hannover maçı oranları
odd_1 = 1.71
odd_x = 3.82
odd_2 = 4.04

print("=" * 70)
print("YENİ TOLERANS TESTİ")
print("=" * 70)
print(f"Maç: Hannover 96 vs Greuther Fürth")
print(f"Oranlar: {odd_1} - {odd_x} - {odd_2}")
print()

# Exact: ±0.10
print("[1] Exact Match (±0.10)")
exact = client.table('matches').select('*').filter('odd_1', 'gte', odd_1 - 0.10).filter('odd_1', 'lte', odd_1 + 0.10).filter('odd_x', 'gte', odd_x - 0.10).filter('odd_x', 'lte', odd_x + 0.10).filter('odd_2', 'gte', odd_2 - 0.10).filter('odd_2', 'lte', odd_2 + 0.10).not_.is_('score', 'null').limit(100).execute()

print(f"  Bulunan: {len(exact.data)} maç")

if exact.data:
    print(f"\n  İlk 5 sonuç:")
    for i, match in enumerate(exact.data[:5]):
        print(f"  {i+1}. {match.get('home_team')} vs {match.get('away_team')}")
        print(f"     Oranlar: {match.get('odd_1')} - {match.get('odd_x')} - {match.get('odd_2')}")
        print(f"     Skor: {match.get('score')}")
    
    # İstatistik hesapla
    stats = {'1': 0, 'X': 0, '2': 0, 'total': 0}
    for match in exact.data:
        score = match.get('score', '').strip()
        if '-' in score:
            parts = score.split('-')
            if len(parts) == 2:
                try:
                    home = int(parts[0].strip())
                    away = int(parts[1].strip())
                    stats['total'] += 1
                    if home > away:
                        stats['1'] += 1
                    elif home == away:
                        stats['X'] += 1
                    else:
                        stats['2'] += 1
                except:
                    pass
    
    if stats['total'] > 0:
        print(f"\n  İstatistikler ({stats['total']} geçerli maç):")
        print(f"    Ev sahibi galibiyet: {stats['1']} (%{stats['1']/stats['total']*100:.1f})")
        print(f"    Beraberlik: {stats['X']} (%{stats['X']/stats['total']*100:.1f})")
        print(f"    Deplasman galibiyet: {stats['2']} (%{stats['2']/stats['total']*100:.1f})")
else:
    print("  ❌ Sonuç yok")

print()

# Similar: ±0.20
print("[2] Similar Match (±0.20)")
similar = client.table('matches').select('*').filter('odd_1', 'gte', odd_1 - 0.20).filter('odd_1', 'lte', odd_1 + 0.20).filter('odd_x', 'gte', odd_x - 0.20).filter('odd_x', 'lte', odd_x + 0.20).filter('odd_2', 'gte', odd_2 - 0.20).filter('odd_2', 'lte', odd_2 + 0.20).not_.is_('score', 'null').limit(100).execute()

# Exact'te olmayanları filtrele
exact_ids = [m['id'] for m in exact.data]
similar_only = [m for m in similar.data if m['id'] not in exact_ids]

print(f"  Bulunan (exact hariç): {len(similar_only)} maç")
print(f"  Toplam: {len(exact.data)} exact + {len(similar_only)} similar = {len(exact.data) + len(similar_only)} maç")

print()
print("=" * 70)
print("SONUÇ:")
if len(exact.data) + len(similar_only) > 10:
    print("  ✅ Yeterli sonuç bulundu! Analiz çalışacak.")
else:
    print("  ⚠️  Az sonuç bulundu. Tolerans daha da artırılabilir.")
print("=" * 70)

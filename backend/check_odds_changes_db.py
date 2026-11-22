"""
Supabase'deki oran değişikliklerini kontrol et
"""
from supabase_sync import get_supabase_client

client = get_supabase_client()

print("=" * 70)
print("SUPABASE - ORAN DEGISIKLIKLERI")
print("=" * 70)
print()

# Toplam kayıt
result = client.table('odds_changes').select('*').execute()
print(f"Toplam kayit: {len(result.data)}")
print()

# En son 5 değişiklik
print("En son 5 degisiklik:")
recent = client.table('odds_changes').select('*').order('detected_at', desc=True).limit(5).execute()

for i, change in enumerate(recent.data):
    print(f"\n{i+1}. {change['home_team']} vs {change['away_team']}")
    print(f"   Tarih: {change['match_datetime']}")
    print(f"   MS1: {change['old_odd_1']:.2f} -> {change['new_odd_1']:.2f} ({change['change_1']:+.1f}%)")
    print(f"   MSX: {change['old_odd_x']:.2f} -> {change['new_odd_x']:.2f} ({change['change_x']:+.1f}%)")
    print(f"   MS2: {change['old_odd_2']:.2f} -> {change['new_odd_2']:.2f} ({change['change_2']:+.1f}%)")
    print(f"   Toplam degisim: {change['total_change']:.1f}%")
    print(f"   Tespit: {change['detected_at']}")

print()

# En büyük değişimler
print("En buyuk 5 degisim:")
biggest = client.table('odds_changes').select('*').order('total_change', desc=True).limit(5).execute()

for i, change in enumerate(biggest.data):
    print(f"\n{i+1}. {change['home_team']} vs {change['away_team']}")
    print(f"   Toplam degisim: {change['total_change']:.1f}%")
    print(f"   MS1: {change['change_1']:+.1f}% | MSX: {change['change_x']:+.1f}% | MS2: {change['change_2']:+.1f}%")

print()
print("=" * 70)

"""
Garip oran değişikliklerini kontrol et
"""
from supabase_sync import get_supabase_client

client = get_supabase_client()

print("=" * 70)
print("GARAİP ORAN DEĞİŞİMLERİ ANALİZİ")
print("=" * 70)
print()

# En büyük değişimleri detaylı incele
result = client.table('odds_changes').select('*').order('total_change', desc=True).limit(10).execute()

print("🔍 En büyük 10 değişim (detaylı):")
print()

for i, change in enumerate(result.data):
    print(f"{i+1}. {change['home_team']} vs {change['away_team']}")
    print(f"   📅 Tarih: {change['match_datetime']}")
    print(f"   🏆 Lig: {change.get('league', 'N/A')}")
    print(f"   📊 Eski oranlar: {change['old_odd_1']:.2f} - {change['old_odd_x']:.2f} - {change['old_odd_2']:.2f}")
    print(f"   📊 Yeni oranlar: {change['new_odd_1']:.2f} - {change['new_odd_x']:.2f} - {change['new_odd_2']:.2f}")
    print(f"   💥 Değişimler: {change['change_1']:+.1f}% | {change['change_x']:+.1f}% | {change['change_2']:+.1f}%")
    print(f"   ⚡ Toplam: {change['total_change']:.1f}%")
    
    # Anomali kontrol
    anomalies = []
    if change['old_odd_1'] > 20 or change['new_odd_1'] > 20:
        anomalies.append("MS1 çok yüksek (>20)")
    if change['old_odd_x'] > 20 or change['new_odd_x'] > 20:
        anomalies.append("MSX çok yüksek (>20)")
    if change['old_odd_2'] > 20 or change['new_odd_2'] > 20:
        anomalies.append("MS2 çok yüksek (>20)")
    if change['old_odd_1'] == 0 or change['new_odd_1'] == 0:
        anomalies.append("MS1 sıfır")
    if change['old_odd_x'] == 0 or change['new_odd_x'] == 0:
        anomalies.append("MSX sıfır")
    if change['old_odd_2'] == 0 or change['new_odd_2'] == 0:
        anomalies.append("MS2 sıfır")
    if abs(change['change_1']) > 200:
        anomalies.append("MS1 aşırı değişim (>200%)")
    if abs(change['change_x']) > 200:
        anomalies.append("MSX aşırı değişim (>200%)")
    if abs(change['change_2']) > 200:
        anomalies.append("MS2 aşırı değişim (>200%)")
    
    if anomalies:
        print(f"   ⚠️  ANOMALİLER: {', '.join(anomalies)}")
    
    print()

print("=" * 70)
print("\n💡 Öneriler:")
print("1. 20'den büyük oranları filtrele (placeholder olabilir)")
print("2. 0 olan oranları atla (eksik veri)")
print("3. %100'den fazla değişimi uyarı olarak işaretle")
print("4. Makul aralık: Oran değişimi ±50% içinde olmalı")
print("=" * 70)

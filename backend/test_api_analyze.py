"""
Analyze API endpoint'ini test et - gerçek bir HTTP çağrısı simüle et
"""
import requests
import json

# Test verisi - Hannover maçı
test_data = {
    "odd_1": "1.71",
    "odd_x": "3.82", 
    "odd_2": "4.04",
    "home_team": "Hannover 96",
    "away_team": "Greuther Fürth"
}

# Local test için
api_url = "http://localhost:3000/api/analyze"

print("=" * 70)
print("ANALYZE API TEST")
print("=" * 70)
print(f"Test Data: {test_data}")
print()

# Manuel Supabase sorgusu - API'deki mantığı taklit et
print("[1] Manuel Supabase Query (API mantığını taklit)")
from supabase_sync import get_supabase_client

client = get_supabase_client()

odd_1 = float(test_data['odd_1'])
odd_x = float(test_data['odd_x'])
odd_2 = float(test_data['odd_2'])

print(f"   Oranlar: {odd_1}, {odd_x}, {odd_2}")
print(f"   Arama aralığı: ±0.01")
print()

# Exact match query (API'deki gibi)
try:
    result = client.table('matches').select('*').filter('odd_1', 'gte', odd_1 - 0.01).filter('odd_1', 'lte', odd_1 + 0.01).filter('odd_x', 'gte', odd_x - 0.01).filter('odd_x', 'lte', odd_x + 0.01).filter('odd_2', 'gte', odd_2 - 0.01).filter('odd_2', 'lte', odd_2 + 0.01).not_.is_('score', 'null').limit(100).execute()
    
    print(f"   ✓ Query başarılı")
    print(f"   Bulunan maç: {len(result.data)}")
    
    if result.data:
        print(f"\n   İlk 3 sonuç:")
        for i, match in enumerate(result.data[:3]):
            print(f"   {i+1}. {match.get('home_team')} vs {match.get('away_team')}")
            print(f"      Oranlar: {match.get('odd_1')} - {match.get('odd_x')} - {match.get('odd_2')}")
            print(f"      Skor: {match.get('score')}")
    else:
        print(f"\n   ❌ HİÇ SONUÇ YOK!")
        
except Exception as e:
    print(f"   ❌ Query hatası: {e}")

print()

# Veri kalitesi kontrolü
print("[2] Veri Kalitesi Kontrolü")

# Oranlı ve skorlu maç var mı?
try:
    with_odds_and_score = client.table('matches').select('id, home_team, away_team, odd_1, odd_x, odd_2, score').not_.is_('odd_1', 'null').not_.is_('odd_x', 'null').not_.is_('odd_2', 'null').not_.is_('score', 'null').limit(10).execute()
    
    print(f"   Oranlı VE skorlu maç sayısı (ilk 10): {len(with_odds_and_score.data)}")
    
    if with_odds_and_score.data:
        print(f"\n   Örnek maçlar:")
        for i, match in enumerate(with_odds_and_score.data[:3]):
            print(f"   {i+1}. {match.get('home_team')} vs {match.get('away_team')}")
            print(f"      Oranlar: {match.get('odd_1')} - {match.get('odd_x')} - {match.get('odd_2')}")
            print(f"      Skor: {match.get('score')}")
    else:
        print(f"\n   ❌ ORAN VE SKORLU MAÇ YOK!")
        print(f"   SORUN: Veritabanında oranlar ve skorlar aynı kayıtta değil!")
        
except Exception as e:
    print(f"   ❌ Hata: {e}")

print()

# Oran aralığı test - geniş arama
print("[3] Geniş Oran Aralığı Testi (±1.0)")
try:
    wide_search = client.table('matches').select('id, home_team, away_team, odd_1, odd_x, odd_2, score').filter('odd_1', 'gte', odd_1 - 1.0).filter('odd_1', 'lte', odd_1 + 1.0).filter('odd_x', 'gte', odd_x - 1.0).filter('odd_x', 'lte', odd_x + 1.0).filter('odd_2', 'gte', odd_2 - 1.0).filter('odd_2', 'lte', odd_2 + 1.0).not_.is_('score', 'null').limit(100).execute()
    
    print(f"   Geniş arama: {len(wide_search.data)} maç bulundu")
    
    if wide_search.data:
        print(f"\n   İlk 5 sonuç:")
        for i, match in enumerate(wide_search.data[:5]):
            print(f"   {i+1}. {match.get('home_team')} vs {match.get('away_team')}")
            print(f"      Oranlar: {match.get('odd_1')} - {match.get('odd_x')} - {match.get('odd_2')}")
            print(f"      Skor: {match.get('score')}")
    else:
        print(f"\n   ❌ Geniş aramada bile sonuç yok!")
        print(f"   SORUN: Oranlar NULL veya skorlar NULL!")
        
except Exception as e:
    print(f"   ❌ Hata: {e}")

print()

# NULL analizi
print("[4] NULL Değer Analizi")
try:
    total = client.table('matches').select('id').execute()
    with_score = client.table('matches').select('id').not_.is_('score', 'null').execute()
    with_odd1 = client.table('matches').select('id').not_.is_('odd_1', 'null').execute()
    with_odd1_and_score = client.table('matches').select('id').not_.is_('odd_1', 'null').not_.is_('score', 'null').execute()
    
    print(f"   Toplam maç: {len(total.data)}")
    print(f"   Skorlu maç: {len(with_score.data)} (%{len(with_score.data)/len(total.data)*100:.1f})")
    print(f"   Oranlı maç (odd_1): {len(with_odd1.data)} (%{len(with_odd1.data)/len(total.data)*100:.1f})")
    print(f"   ORAN VE SKORLU: {len(with_odd1_and_score.data)} (%{len(with_odd1_and_score.data)/len(total.data)*100:.1f})")
    
    if len(with_odd1_and_score.data) < 1000:
        print(f"\n   ❌ SORUN BULUNDU!")
        print(f"   Oran VE skor birlikte olan maç çok az!")
        print(f"   Analiz için yeterli veri yok!")
    
except Exception as e:
    print(f"   ❌ Hata: {e}")

print()
print("=" * 70)

"""
Analiz sistemini kontrol et - geçmiş maç verisi var mı?
"""
from supabase_sync import get_supabase_client

client = get_supabase_client()

print("=" * 70)
print("ANALİZ SİSTEMİ VERİ KONTROLÜ")
print("=" * 70)
print()

# 1. Past matches tablosunu kontrol et
print("[1] Past Matches Tablosu")
try:
    result = client.table('past_matches').select('*').limit(5).execute()
    print(f"  Kayıt sayısı (sample): {len(result.data)}")
    
    if result.data:
        print(f"  İlk kayıt:")
        first = result.data[0]
        print(f"    - datetime: {first.get('datetime', 'N/A')}")
        print(f"    - home_team: {first.get('home_team', 'N/A')}")
        print(f"    - away_team: {first.get('away_team', 'N/A')}")
        print(f"    - league: {first.get('league', 'N/A')}")
        print(f"    - fulltime_score: {first.get('fulltime_score', 'N/A')}")
    else:
        print("  ❌ TABLO BOŞ!")
except Exception as e:
    print(f"  ❌ HATA: {e}")

print()

# 2. Hannover 96 için geçmiş maçları ara
print("[2] Hannover 96 Geçmiş Maçları")
try:
    result = client.table('past_matches').select('*').or_(
        'home_team.ilike.%Hannover%,away_team.ilike.%Hannover%'
    ).limit(10).execute()
    
    print(f"  Bulunan maç: {len(result.data)}")
    
    if result.data:
        for i, match in enumerate(result.data[:5]):
            print(f"  {i+1}. {match.get('datetime')} - {match.get('home_team')} vs {match.get('away_team')}")
            print(f"     Skor: {match.get('fulltime_score')}, Lig: {match.get('league')}")
    else:
        print("  ❌ HANNOVER İÇİN GEÇMİŞ MAÇ YOK!")
except Exception as e:
    print(f"  ❌ HATA: {e}")

print()

# 3. Greuther Fürth için geçmiş maçları ara
print("[3] Greuther Fürth Geçmiş Maçları")
try:
    result = client.table('past_matches').select('*').or_(
        'home_team.ilike.%Fürth%,away_team.ilike.%Fürth%,home_team.ilike.%Furth%,away_team.ilike.%Furth%'
    ).limit(10).execute()
    
    print(f"  Bulunan maç: {len(result.data)}")
    
    if result.data:
        for i, match in enumerate(result.data[:5]):
            print(f"  {i+1}. {match.get('datetime')} - {match.get('home_team')} vs {match.get('away_team')}")
            print(f"     Skor: {match.get('fulltime_score')}, Lig: {match.get('league')}")
    else:
        print("  ❌ FÜRTH İÇİN GEÇMİŞ MAÇ YOK!")
except Exception as e:
    print(f"  ❌ HATA: {e}")

print()

# 4. Toplam geçmiş maç sayısı
print("[4] Toplam Geçmiş Maç Sayısı")
try:
    # Son 30 gün
    from datetime import datetime, timedelta
    cutoff = datetime.now() - timedelta(days=30)
    cutoff_str = cutoff.strftime('%d.%m.%Y')
    
    result = client.table('past_matches').select('id', count='exact').execute()
    print(f"  Toplam kayıt: {result.count if hasattr(result, 'count') else 'N/A'}")
    
    # Başka bir yöntem - tüm kayıtları çek
    all_matches = client.table('past_matches').select('id').execute()
    print(f"  Toplam kayıt (query): {len(all_matches.data)}")
    
except Exception as e:
    print(f"  ❌ HATA: {e}")

print()
print("=" * 70)

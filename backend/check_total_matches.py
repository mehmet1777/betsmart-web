"""
Supabase'deki toplam maç sayısını kontrol et
"""
from supabase_sync import get_supabase_client

client = get_supabase_client()

print("=" * 70)
print("SUPABASE TOPLAM MAÇ SAYISI")
print("=" * 70)
print()

# matches tablosu - geçmiş maçlar
print("[1] matches tablosu (geçmiş maçlar)")
try:
    # Tüm kayıtları çek (pagination ile)
    all_matches = []
    offset = 0
    batch_size = 1000
    
    while True:
        result = client.table('matches').select('id').range(offset, offset + batch_size - 1).execute()
        if not result.data:
            break
        all_matches.extend(result.data)
        offset += batch_size
        print(f"  Çekiliyor... {len(all_matches)} kayıt")
        
        if len(result.data) < batch_size:
            break
    
    print(f"\n  ✅ TOPLAM: {len(all_matches)} maç")
    
    # Skorlu maçlar
    scored = client.table('matches').select('id').not_.is_('score', 'null').limit(10000).execute()
    print(f"  Skorlu (bitmiş): {len(scored.data)} maç (ilk 10000)")
    
    # Oranlı maçlar
    with_odds = client.table('matches').select('id').not_.is_('odd_1', 'null').limit(10000).execute()
    print(f"  Oranlı: {len(with_odds.data)} maç (ilk 10000)")
    
except Exception as e:
    print(f"  ❌ HATA: {e}")

print()

# future_matches tablosu - gelecek maçlar
print("[2] future_matches tablosu (gelecek maçlar)")
try:
    all_future = []
    offset = 0
    batch_size = 1000
    
    while True:
        result = client.table('future_matches').select('id').range(offset, offset + batch_size - 1).execute()
        if not result.data:
            break
        all_future.extend(result.data)
        offset += batch_size
        print(f"  Çekiliyor... {len(all_future)} kayıt")
        
        if len(result.data) < batch_size:
            break
    
    print(f"\n  ✅ TOPLAM: {len(all_future)} maç")
    
except Exception as e:
    print(f"  ❌ HATA: {e}")

print()
print("=" * 70)
print("ÖZET")
print("=" * 70)
print(f"Geçmiş maçlar (matches): {len(all_matches) if 'all_matches' in locals() else 'HATA'}")
print(f"Gelecek maçlar (future_matches): {len(all_future) if 'all_future' in locals() else 'HATA'}")
print(f"GENEL TOPLAM: {len(all_matches) + len(all_future) if 'all_matches' in locals() and 'all_future' in locals() else 'HATA'}")

if 'all_matches' in locals() and len(all_matches) < 100000:
    print()
    print("⚠️  UYARI: Geçmiş maç sayısı çok az!")
    print("   Normalde ~393,000 maç olmalı")
    print("   Veriler silinmiş olabilir!")
print("=" * 70)

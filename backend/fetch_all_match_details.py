"""
Tüm maçların detaylarını çek
/yeniveri komutundan sonra çalışır
"""
from match_details_sync import sync_multiple_matches
from supabase_sync import get_supabase_client

def fetch_all_match_details_for_future_matches():
    """
    future_matches tablosundaki tüm maçların detaylarını çek
    
    Returns:
        (success_count: int, error_count: int, skipped: int)
    """
    try:
        client = get_supabase_client()
        
        print("\n" + "="*80)
        print("📊 MATCH DETAILS CEKILIYOR")
        print("="*80)
        
        # future_matches'ten UUID'leri çek
        result = client.table('future_matches').select('match_uuid,home_team,away_team').execute()
        
        if not result.data:
            print("⚠️  future_matches tablosunda maç yok")
            return (0, 0, 0)
        
        # UUID'leri topla (None olanları atla)
        uuids = []
        no_uuid_count = 0
        
        for match in result.data:
            uuid = match.get('match_uuid')
            if uuid and uuid != 'None' and uuid.strip():
                uuids.append(uuid)
            else:
                no_uuid_count += 1
        
        print(f"✅ Toplam maç: {len(result.data)}")
        print(f"   UUID var: {len(uuids)}")
        print(f"   UUID yok: {no_uuid_count}")
        
        if len(uuids) == 0:
            print("⚠️  Hiçbir maçta UUID yok (Mackolik fallback kullanılmış olabilir)")
            return (0, 0, no_uuid_count)
        
        # Paralel çek (3 thread)
        success_count, error_count = sync_multiple_matches(uuids, max_workers=3)
        
        print("\n" + "="*80)
        print("📊 MATCH DETAILS OZET")
        print("="*80)
        print(f"✅ Basarili: {success_count}")
        print(f"❌ Hatali: {error_count}")
        print(f"⏭️  Atlanan: {no_uuid_count} (UUID yok)")
        print("="*80)
        
        return (success_count, error_count, no_uuid_count)
        
    except Exception as e:
        print(f"❌ Genel hata: {e}")
        import traceback
        traceback.print_exc()
        return (0, 0, 0)


# CLI kullanımı için
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--force':
        print("⚠️  FORCE MODE: Mevcut kayitlar tekrar cekilecek")
        # TODO: force_update=True parametresi ekle
    
    fetch_all_match_details_for_future_matches()

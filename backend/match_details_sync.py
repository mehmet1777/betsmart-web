"""
Match Details'i Supabase'e kaydet
"""
from supabase_sync import get_supabase_client
from match_details_api import fetch_match_details
from datetime import datetime

def sync_match_details_to_supabase(match_uuid, force_update=False):
    """
    Tek bir maçın detaylarını Supabase'e kaydet
    
    Args:
        match_uuid: Maçın UUID'si
        force_update: True ise mevcut kayıt varsa güncelle
        
    Returns:
        (success: bool, error: str or "skipped")
    """
    try:
        client = get_supabase_client()
        
        # Önce kontrol et: Bu maç daha önce çekilmiş mi?
        if not force_update:
            existing = client.table('match_details').select('id').eq(
                'match_uuid', match_uuid
            ).execute()
            
            if existing.data and len(existing.data) > 0:
                return (True, "skipped")  # Skipped flag
        
        # API'den çek
        success, data, error = fetch_match_details(match_uuid)
        
        if not success:
            return (False, error)
        
        # Supabase'e kaydet
        record = {
            'match_uuid': data['match_uuid'],
            'home_team': data['home_team'],
            'away_team': data['away_team'],
            'match_datetime': data['match_datetime'],
            'h2h_data': data['h2h_data'],
            'form_home': data['form_home'],
            'form_away': data['form_away'],
            'fetched_at': datetime.now().isoformat()
        }
        
        # Upsert (insert or update)
        result = client.table('match_details').upsert(
            record,
            on_conflict='match_uuid'
        ).execute()
        
        return (True, None)  # Success
        
    except Exception as e:
        return (False, str(e))


def sync_multiple_matches(match_uuids, max_workers=3):
    """
    Birden fazla maçın detaylarını çek (paralel)
    
    Args:
        match_uuids: UUID listesi
        max_workers: Paralel thread sayısı
        
    Returns:
        (success_count: int, error_count: int)
    """
    import concurrent.futures
    
    total = len(match_uuids)
    print(f"\n📊 {total} maçın detayları çekiliyor...")
    print(f"⚡ {max_workers} thread paralel çalışacak")
    print("="*80)
    
    success_count = 0
    error_count = 0
    skipped_count = 0
    completed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(sync_match_details_to_supabase, uuid): uuid 
            for uuid in match_uuids
        }
        
        for future in concurrent.futures.as_completed(futures):
            uuid = futures[future]
            completed += 1
            progress = (completed / total) * 100
            
            try:
                success, error = future.result()
                if success:
                    if error == "skipped":  # Zaten var
                        skipped_count += 1
                    else:
                        success_count += 1
                else:
                    error_count += 1
                    
                # Progress göster
                print(f"[{completed}/{total}] %{progress:.1f} | ✅ {success_count} | ⏭️ {skipped_count} | ❌ {error_count}")
                
            except Exception as e:
                error_count += 1
                print(f"[{completed}/{total}] %{progress:.1f} | ❌ Thread hatası: {str(e)[:50]}")
    
    print("="*80)
    print(f"✅ Yeni eklenen: {success_count}")
    print(f"⏭️  Zaten vardı: {skipped_count}")
    print(f"❌ Hatalı: {error_count}")
    
    return (success_count, error_count)


# Test
if __name__ == '__main__':
    # Test UUID
    test_uuid = "7tto7hbwd8o4wifwovvhbk1zo"
    
    print("MATCH DETAILS SYNC TEST")
    print("="*80)
    
    success, error = sync_match_details_to_supabase(test_uuid, force_update=True)
    
    if success:
        print("\n✅ Test başarılı! Supabase'de kontrol edin:")
        print("   https://supabase.com/dashboard/project/.../editor")
    else:
        print(f"\n❌ Test başarısız: {error}")

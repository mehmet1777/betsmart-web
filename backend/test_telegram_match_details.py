"""
Test: /yeniveri komutu sonrası match details otomatik çekilir mi?
"""

import sys
import os

# fetch_all_match_details import kontrolü
try:
    from fetch_all_match_details import fetch_all_match_details_for_future_matches
    print("✅ fetch_all_match_details modülü import edildi")
except Exception as e:
    print(f"❌ Import hatası: {e}")
    sys.exit(1)

# Supabase bağlantı kontrolü
try:
    from supabase_sync import get_supabase_client
    client = get_supabase_client()
    
    # Test: future_matches'ten UUID'li maç çek
    result = client.table('future_matches').select('match_uuid, home_team, away_team').not_.is_('match_uuid', 'null').limit(1).execute()
    
    if result.data and len(result.data) > 0:
        test_match = result.data[0]
        print(f"\n✅ Test maçı bulundu:")
        print(f"   UUID: {test_match['match_uuid']}")
        print(f"   Maç: {test_match['home_team']} vs {test_match['away_team']}")
    else:
        print("\n⚠️ UUID'li maç bulunamadı (henüz /yeniveri çalıştırılmamış)")
        
except Exception as e:
    print(f"❌ Supabase hatası: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("🧪 SİMÜLASYON: /yeniveri akışı")
print("="*50)

print("\n1️⃣ Maçlar Sahadan'dan çekildi")
print("2️⃣ Supabase'e kaydedildi (UUID'ler dahil)")
print("3️⃣ İlk oranlar odds_changes'e eklendi")
print("\n4️⃣ Match details fetch başlıyor...\n")

try:
    # Simüle et
    print("📊 fetch_all_match_details_for_future_matches() çağrılıyor...")
    print("   (Bu işlem 1-2 dakika sürebilir, UUID başına ~1 saniye)\n")
    
    # Gerçek fetch (eğer UUID'ler varsa)
    if result.data and len(result.data) > 0:
        print("⚠️ DİKKAT: Gerçek API çağrısı yapacağız. Devam etmek istiyor musunuz?")
        print("   - UUID'li tüm maçlar için match details çekilecek")
        print("   - Her maç için ~1 saniye sürer")
        print("   - Sahadan API'ye request gidecek")
        
        response = input("\n✅ Devam (E/H)? ").strip().upper()
        
        if response == 'E':
            print("\n🚀 Başlatılıyor...\n")
            result = fetch_all_match_details_for_future_matches()
            
            print("\n" + "="*50)
            print("SONUÇ:")
            print("="*50)
            
            if result['success']:
                print(f"✅ Başarılı: {result['success_count']} maç")
                print(f"❌ Başarısız: {result['failed_count']} maç")
                print(f"⏭️ Atlanan (UUID yok): {result['skipped_count']} maç")
                print(f"⏱️ Toplam süre: {result['elapsed_time']:.1f} saniye")
                
                if result['success_count'] > 0:
                    print("\n🎉 Telegram mesajında şu görünür:")
                    print(f"   📊 {result['success_count']} maç detayı eklendi")
                    if result['failed_count'] > 0:
                        print(f"   ⚠️ {result['failed_count']} maç detayı alınamadı")
            else:
                print(f"❌ Hata: {result.get('error', 'Bilinmeyen hata')}")
        else:
            print("\n❌ İptal edildi")
    else:
        print("⚠️ UUID'li maç yok, önce /yeniveri çalıştırın")
        
except KeyboardInterrupt:
    print("\n\n⚠️ Kullanıcı tarafından iptal edildi")
except Exception as e:
    print(f"\n❌ Hata: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Test tamamlandı\n")

"""
API yanıt veren ama kaydedilmeyen maçları test et
"""

from match_details_sync import sync_match_details_to_supabase

# Test edilecek UUID'ler (API yanıt veren ama kaydedilmeyenler)
test_uuids = [
    ("avzv2to75kgvcl7bvs9sykx04", "Gymnasia vs Newells OB"),
    ("6p5ug920hdwebzrkkytnv7cic", "Parceiro (K) vs Urawa Reds (K)")
]

print("="*80)
print("🧪 SYNC TEST - API yanıt veren ama kaydedilmeyenler")
print("="*80)

for uuid, match_name in test_uuids:
    print(f"\n📋 {match_name}")
    print(f"   UUID: {uuid}")
    
    try:
        success, error = sync_match_details_to_supabase(uuid, force_update=True)
        
        if success:
            print(f"   ✅ Şimdi kaydedildi!")
        else:
            print(f"   ❌ Hala hata: {error}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "="*80)
print("💡 SONUÇ:")
print("   Eğer 'Şimdi kaydedildi' görüyorsanız:")
print("   → Önceki çalıştırmada race condition veya timeout vardı")
print("   → Paralel thread sayısını azaltmayı deneyin (max_workers=1)")

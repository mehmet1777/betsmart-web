"""
Hybrid Fetch - Sahadan + Mackolik
Önce Sahadan dener, bulamazsa Mackolik'e geçer
"""
from sahadan_api import fetch_sahadan_matches
from mackolik_api import fetch_mackolik_matches

def fetch_matches_hybrid(days_ahead=2, status_callback=None):
    """
    Hybrid fetch: Sahadan → Mackolik
    
    Args:
        days_ahead: Kaç gün sonrasına kadar
        status_callback: İlerleme callback
        
    Returns:
        (success: bool, matches: list, error: str, source: str)
    """
    
    print("🔄 Hybrid Fetch başlatılıyor...")
    print("━" * 50)
    
    # 1️⃣ Önce Sahadan'ı dene
    print("1️⃣ Sahadan.com deneniyor (tarih filtreli)...")
    
    if status_callback:
        status_callback("trying_sahadan")
    
    success, matches, error = fetch_sahadan_matches(days_ahead, status_callback)
    
    if success and len(matches) >= 10:
        print(f"✅ Sahadan başarılı: {len(matches)} geçerli maç bulundu")
        print("━" * 50)
        return (True, matches, None, "sahadan")
    
    # Sahadan başarısız veya yeterli maç yok
    print(f"⚠️  Sahadan'da yeterli geçerli maç yok (bulundu: {len(matches)})")
    print(f"   Hata: {error}")
    print("━" * 50)
    
    # 2️⃣ Mackolik'e geç
    print("2️⃣ Mackolik.com'a geçiliyor...")
    
    if status_callback:
        status_callback("falling_back_to_mackolik")
    
    success, matches, error = fetch_mackolik_matches(days_ahead, status_callback)
    
    if success:
        print(f"✅ Mackolik başarılı: {len(matches)} maç bulundu")
        print("━" * 50)
        return (True, matches, None, "mackolik")
    
    # Her ikisi de başarısız
    print("❌ Hem Sahadan hem Mackolik başarısız!")
    print("━" * 50)
    return (False, [], "Her iki kaynaktan da veri çekilemedi", None)


if __name__ == "__main__":
    # Test
    def status_print(msg):
        print(f"   📊 Status: {msg}")
    
    success, matches, error, source = fetch_matches_hybrid(days_ahead=2, status_callback=status_print)
    
    if success:
        print(f"\n🎉 BAŞARILI!")
        print(f"   Kaynak: {source}")
        print(f"   Maç sayısı: {len(matches)}")
        if matches:
            print(f"\n   İlk 3 maç:")
            for i, m in enumerate(matches[:3], 1):
                print(f"   {i}. {m.get('home_team')} vs {m.get('away_team')}")
    else:
        print(f"\n❌ BAŞARISIZ: {error}")

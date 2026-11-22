"""
Galatasaray vs Fenerbahce H2H - Exact match ile
"""

from supabase_sync import get_supabase_client

try:
    client = get_supabase_client()
    
    print("="*80)
    print("GALATASARAY vs FENERBAHCE H2H - 393k MAC")
    print("="*80)
    
    # 1. Galatasaray (EV) vs Fenerbahce (DEP)
    print("\n1. Galatasaray (EV) vs Fenerbahce (DEP):")
    
    result1 = client.table('matches').select('*').eq(
        'home_team', 'Galatasaray'
    ).eq('away_team', 'Fenerbahce').execute()
    
    print(f"   Bulundu: {len(result1.data)} mac\n")
    for match in result1.data:
        print(f"   {match['home_team']} {match['score']} {match['away_team']}")
        print(f"   IY: {match['half_score']} | Oranlar: {match['odd_1']}-{match['odd_x']}-{match['odd_2']}")
        print()
    
    # 2. Fenerbahce (EV) vs Galatasaray (DEP)
    print("\n2. Fenerbahce (EV) vs Galatasaray (DEP):")
    
    result2 = client.table('matches').select('*').eq(
        'home_team', 'Fenerbahce'
    ).eq('away_team', 'Galatasaray').execute()
    
    print(f"   Bulundu: {len(result2.data)} mac\n")
    for match in result2.data:
        print(f"   {match['home_team']} {match['score']} {match['away_team']}")
        print(f"   IY: {match['half_score']} | Oranlar: {match['odd_1']}-{match['odd_x']}-{match['odd_2']}")
        print()
    
    # TOPLAM
    all_h2h = result1.data + result2.data
    total = len(all_h2h)
    
    print("="*80)
    print(f"TOPLAM H2H: {total} MAC")
    print("="*80)
    
    if total > 0:
        print("\n✅ BASARILI! Kendi datamizda H2H var!")
        
        # İstatistikler
        gala_wins = 0
        fener_wins = 0
        draws = 0
        
        for match in all_h2h:
            home = match['home_team']
            score = match.get('score', '')
            
            if score and '-' in score:
                try:
                    h, a = map(int, score.split('-'))
                    
                    if home == 'Galatasaray':
                        if h > a: gala_wins += 1
                        elif h < a: fener_wins += 1
                        else: draws += 1
                    else:
                        if h > a: fener_wins += 1
                        elif h < a: gala_wins += 1
                        else: draws += 1
                except:
                    pass
        
        print(f"\nISTATISTIKLER (Son {total} mac):")
        print(f"  Galatasaray: {gala_wins} galibiyet")
        print(f"  Fenerbahce: {fener_wins} galibiyet")
        print(f"  Beraberlik: {draws}")
        
        print("\n" + "="*80)
        print("SAHADAN FALLBACK STRATEJISI:")
        print("="*80)
        print("""
1. Sahadan API'den H2H cek
   ✅ BASARILI -> Kullan
   ❌ 502 ERROR -> 2. adima gec
   
2. Kendi database'den H2H cek
   • future_matches'ten home_team ve away_team al
   • matches'te exact match yap
   • H2H data olustur
   
3. Eger hala yoksa
   • "Detay bulunamadi" goster
   
AVANTAJLAR:
   ✅ 393k gecmis mac datasi var!
   ✅ Hizli (exact match)
   ✅ Guvenilir
   ✅ API limit yok
   
COVERAGE TAHMINI:
   • Sahadan: %40 (49/121)
   • Kendi DB: +%35-40 (populer takimlar)
   • TOPLAM: %75-80 basari!
        """)
    else:
        print("\n❌ H2H bulunamadi")
        print("\nSEBEPLER:")
        print("  • Takim ismi farkli yazilmis olabilir")
        print("  • Ornek: 'Galatasaray' vs 'Galatasaray SK'")
        print("  • Fuzzy matching gerekebilir")
    
except Exception as e:
    print(f"\nHATA: {e}")
    import traceback
    traceback.print_exc()

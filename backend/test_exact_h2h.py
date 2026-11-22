"""
Exact match ile H2H test - ILIKE yerine eq kullan
"""

from supabase_sync import get_supabase_client

try:
    client = get_supabase_client()
    
    print("="*80)
    print("EXACT MATCH H2H TEST - 393k mac arasinda")
    print("="*80)
    
    # Exact team names (database'deki tam isimler)
    # Önce bir maç çekip takım isimlerinin tam halini görelim
    
    print("\n1. Database'de 'Galatasaray' iceren ilk 3 mac:")
    sample = client.table('matches').select('home_team,away_team,score').ilike(
        'home_team', '%Galata%'
    ).limit(3).execute()
    
    if sample.data:
        for match in sample.data:
            print(f"   {match['home_team']} vs {match['away_team']}")
            
        # İlk maçın tam ismini al
        exact_home = sample.data[0]['home_team']
        print(f"\n2. Exact match test: '{exact_home}'")
        
        # Exact match sorgusu (çok daha hızlı)
        exact_result = client.table('matches').select('*').eq(
            'home_team', exact_home
        ).limit(5).execute()
        
        print(f"   Bulundu: {len(exact_result.data)} mac")
        for match in exact_result.data:
            print(f"   - {match['home_team']} {match['score']} {match['away_team']}")
    else:
        print("   Galatasaray bulunamadi!")
        
        # Alternatif: Fenerbahce dene
        print("\n   Fenerbahce deneniyor...")
        sample2 = client.table('matches').select('home_team,away_team,score').ilike(
            'home_team', '%Fener%'
        ).limit(3).execute()
        
        if sample2.data:
            for match in sample2.data:
                print(f"   {match['home_team']} vs {match['away_team']}")
    
    print("\n" + "="*80)
    print("COZUM ONERILERI:")
    print("="*80)
    print("""
SORUN: 393k mac, ILIKE cok yavas, timeout oluyor

COZUM 1: Index ekle (ONERILIR)
   SQL: create_h2h_indexes.sql
   • pg_trgm extension
   • GIN index home_team ve away_team
   • Sorgu sureleri: 10sn -> 0.1sn
   
COZUM 2: Exact match kullan
   • ILIKE yerine eq()
   • Ancak takim ismi tam olmali
   • "Galatasaray" != "Galatasaray SK"
   
COZUM 3: Ayri H2H tablosu olustur
   CREATE TABLE h2h_cache (
       team1 TEXT,
       team2 TEXT,
       matches JSONB,
       updated_at TIMESTAMP
   )
   • Pre-calculate edilmis H2H
   • Hizli sorgular
   • Ancak ekstra maintenance
   
COZUM 4: Python'da filtrele (YAVAS ama calisir)
   • Tum maclari cek (batch'ler halinde)
   • Python'da takım ismi eslestir
   • 393k mac icin ~30-60 saniye
   
ONERIM: COZUM 1 (Index ekle)
   • En hizli ve guvenilir
   • Bir kere ekle, surekli kullan
   • Supabase dashboard'dan SQL calistir
""")
    
except Exception as e:
    print(f"\nHATA: {e}")
    import traceback
    traceback.print_exc()

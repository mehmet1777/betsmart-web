"""
Kendi datamizdan H2H cek - Galatasaray vs Fenerbahce TEST
"""

from supabase_sync import get_supabase_client
from datetime import datetime

print("="*80)
print("KENDI DATAMIZDAN H2H TEST")
print("="*80)

# Test takımları
home_team = "Galatasaray"
away_team = "Fenerbahce"

print(f"\nTest: {home_team} vs {away_team}")
print("-"*80)

try:
    client = get_supabase_client()
    
    # 1. ARALANDAKI MACLAR (H2H)
    print(f"\n1. ARALANDAKI MACLAR:")
    print("-"*80)
    
    # Galatasaray vs Fenerbahce VEYA Fenerbahce vs Galatasaray
    h2h_query = client.table('matches').select('*').or_(
        f"and(home_team.ilike.%{home_team}%,away_team.ilike.%{away_team}%),"
        f"and(home_team.ilike.%{away_team}%,away_team.ilike.%{home_team}%)"
    ).order('id', desc=True).limit(10).execute()
    
    h2h_matches = h2h_query.data
    
    if h2h_matches:
        print(f"✅ {len(h2h_matches)} mac bulundu (son 10):\n")
        
        for i, match in enumerate(h2h_matches, 1):
            date = match.get('date', 'N/A')
            home = match.get('home_team', 'N/A')
            away = match.get('away_team', 'N/A')
            score = match.get('score', 'N/A')
            half_score = match.get('half_score', 'N/A')
            league = match.get('league', 'N/A')
            
            print(f"{i:2d}. {home} {score} {away} (IY: {half_score})")
            print(f"    Lig: {league}")
    else:
        print(f"❌ Hic mac bulunamadi")
    
    # 2. GALATASARAY SON 5 MAC (Form)
    print(f"\n2. {home_team.upper()} - SON 5 MAC:")
    print("-"*80)
    
    gala_form = client.table('matches').select('*').or_(
        f"home_team.ilike.%{home_team}%,away_team.ilike.%{home_team}%"
    ).order('id', desc=True).limit(5).execute()
    
    if gala_form.data:
        print(f"✅ {len(gala_form.data)} mac bulundu:\n")
        
        for i, match in enumerate(gala_form.data, 1):
            home = match.get('home_team', 'N/A')
            away = match.get('away_team', 'N/A')
            score = match.get('score', 'N/A')
            
            # Galatasaray ev sahibi mi deplasman mi?
            if home_team.lower() in home.lower():
                print(f"{i}. {home} {score} {away} (EV)")
            else:
                print(f"{i}. {home} {score} {away} (DEP)")
    
    # 3. FENERBAHCE SON 5 MAC (Form)
    print(f"\n3. {away_team.upper()} - SON 5 MAC:")
    print("-"*80)
    
    fener_form = client.table('matches').select('*').or_(
        f"home_team.ilike.%{away_team}%,away_team.ilike.%{away_team}%"
    ).order('id', desc=True).limit(5).execute()
    
    if fener_form.data:
        print(f"✅ {len(fener_form.data)} mac bulundu:\n")
        
        for i, match in enumerate(fener_form.data, 1):
            home = match.get('home_team', 'N/A')
            away = match.get('away_team', 'N/A')
            score = match.get('score', 'N/A')
            
            # Fenerbahce ev sahibi mi deplasman mi?
            if away_team.lower() in home.lower():
                print(f"{i}. {home} {score} {away} (EV)")
            else:
                print(f"{i}. {home} {score} {away} (DEP)")
    
    # 4. ISTATISTIKLER
    print(f"\n4. ISTATISTIKLER:")
    print("-"*80)
    
    if h2h_matches:
        # Galibiyet sayıları
        gala_wins = 0
        fener_wins = 0
        draws = 0
        
        for match in h2h_matches:
            home = match.get('home_team', '')
            score = match.get('score', '')
            
            if score and '-' in score:
                try:
                    home_score, away_score = map(int, score.split('-'))
                    
                    if home_team.lower() in home.lower():
                        # Galatasaray ev sahibi
                        if home_score > away_score:
                            gala_wins += 1
                        elif home_score < away_score:
                            fener_wins += 1
                        else:
                            draws += 1
                    else:
                        # Fenerbahce ev sahibi
                        if home_score > away_score:
                            fener_wins += 1
                        elif home_score < away_score:
                            gala_wins += 1
                        else:
                            draws += 1
                except:
                    pass
        
        total = len(h2h_matches)
        print(f"Son {total} mac:")
        print(f"  Galatasaray: {gala_wins} galibiyet ({gala_wins*100//total if total > 0 else 0}%)")
        print(f"  Fenerbahce: {fener_wins} galibiyet ({fener_wins*100//total if total > 0 else 0}%)")
        print(f"  Beraberlik: {draws} ({draws*100//total if total > 0 else 0}%)")
    
    # 5. TOPLAM VERİ MİKTARI
    print(f"\n5. TOPLAM VERI:")
    print("-"*80)
    
    # Toplam maç sayısı
    total_count = client.table('matches').select('id', count='exact').execute()
    print(f"Veritabanindaki toplam mac: {total_count.count:,}")
    
    # Tarih aralığı
    oldest = client.table('matches').select('id,date').order('id', desc=False).limit(1).execute()
    newest = client.table('matches').select('id,date').order('id', desc=True).limit(1).execute()
    
    if oldest.data and newest.data:
        oldest_date = oldest.data[0].get('date', 'N/A')
        newest_date = newest.data[0].get('date', 'N/A')
        print(f"ID araligi: {oldest.data[0]['id']} - {newest.data[0]['id']}")
    
except Exception as e:
    print(f"\n❌ HATA: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("SONUC:")
print("="*80)
print("""
EGER H2H MACLARI BULUNURSA:
   MUKEMMEL! Sahadan 502 verdiginde kendi datamizdan cekelim!
   
AVANTAJLAR:
   ✅ Hizli (kendi database'imiz)
   ✅ Guvenilir (zaten elimizde)
   ✅ Kapsamli (2020-2026 arasi tum maclar)
   ✅ API limit yok
   ✅ Maliyet yok
   
UYGULAMA:
   1. Sahadan'dan dene
   2. 502 error -> Kendi DB'den cek
   3. Her ikisi de yoksa "Detay yok" goster
   
COVERAGE TAHMINI:
   • Sahadan: %40 (49 mac)
   • Kendi DB: +%30-40 (populer takimlar icin)
   • TOPLAM: %70-80 basari!
""")

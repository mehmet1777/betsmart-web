"""
Match Detail API'den gelen verileri analiz et
Hangi veriler tahmin için önemli?
"""
import json

with open('match_detail_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

match_data = data.get('data', {})

print("MATCH DETAIL API - VERI ANALIZI")
print("="*80)

# 1. H2H (Head to Head - Aralarındaki Maçlar)
print("\n1. ARALARINDAKI MACLAR (H2H)")
print("-"*80)

h2h = match_data.get('h2h', {})

if h2h:
    print(f"Toplam mac sayisi: {len(h2h.get('matches', []))}")
    
    # İstatistikler
    stats = h2h.get('statistics', {})
    if stats:
        print(f"\nGenel Istatistikler:")
        print(f"  Ev sahibi galibiyet: {stats.get('team_A', {}).get('win', 0)}")
        print(f"  Beraberlik: {stats.get('draw', 0)}")
        print(f"  Deplasman galibiyet: {stats.get('team_B', {}).get('win', 0)}")
    
    # Son maçlar
    matches = h2h.get('matches', [])
    print(f"\nSon 5 mac:")
    for idx, match in enumerate(matches[:5], 1):
        date = match.get('date_time_utc', '')[:10]
        home = match.get('team_A', {}).get('name', '')
        away = match.get('team_B', {}).get('name', '')
        score_home = match.get('fts_A', 0)
        score_away = match.get('fts_B', 0)
        print(f"  {idx}. {date}: {home} {score_home}-{score_away} {away}")
    
    print(f"\nONEMLI MI? ✅ EVET")
    print(f"  - Son N macdaki galibiyetler")
    print(f"  - Ortalama skorlar")
    print(f"  - Ev/deplasman avantaji")

# 2. FORM DURUMU
print("\n\n2. FORM DURUMU (Son Maçlar)")
print("-"*80)

forms = match_data.get('forms', {})

if forms:
    team_a_form = forms.get('team_A', {}).get('all_competitions', {})
    team_b_form = forms.get('team_B', {}).get('all_competitions', {})
    
    print(f"Ev Sahibi Form:")
    print(f"  Serie: {team_a_form.get('serie', 'N/A')}")  # WWDLL gibi
    print(f"  Atilan gol: {team_a_form.get('goal_pro', 0)}")
    print(f"  Yenilen gol: {team_a_form.get('goal_against', 0)}")
    print(f"  2.5 ust: {team_a_form.get('over_2_goals', 0)}/5 mac")
    print(f"  Karsilikli gol: {team_a_form.get('two_teams_scored', 0)}/5 mac")
    
    print(f"\nDeplasman Form:")
    print(f"  Serie: {team_b_form.get('serie', 'N/A')}")
    print(f"  Atilan gol: {team_b_form.get('goal_pro', 0)}")
    print(f"  Yenilen gol: {team_b_form.get('goal_against', 0)}")
    print(f"  2.5 ust: {team_b_form.get('over_2_goals', 0)}/5 mac")
    print(f"  Karsilikli gol: {team_b_form.get('two_teams_scored', 0)}/5 mac")
    
    # Son maçları göster
    team_a_matches = team_a_form.get('matches', [])
    if team_a_matches:
        print(f"\n  Ev Sahibi Son 3 Mac:")
        for idx, match in enumerate(team_a_matches[:3], 1):
            home = match.get('team_A', {}).get('name', '')
            away = match.get('team_B', {}).get('name', '')
            score_home = match.get('fts_A', 0)
            score_away = match.get('fts_B', 0)
            date = match.get('date_time_utc', '')[:10]
            print(f"    {idx}. {date}: {home} {score_home}-{score_away} {away}")
    
    print(f"\nONEMLI MI? ✅ EVET")
    print(f"  - Galibiyetsizlik serisi (W/D/L)")
    print(f"  - Gol atma/yeme ortalamasi")
    print(f"  - 2.5 ust/alt trend")
    print(f"  - KG (Karsilikli Gol) trend")

# 3. LEAGUE STANDINGS (Puan durumu)
print("\n\n3. PUAN DURUMU")
print("-"*80)

standings = match_data.get('standings', {})

if standings and isinstance(standings, list):
    print(f"Toplam takim: {len(standings)}")
    
    # Ev sahibi ve deplasman takımlarını bul
    home_team_name = match_data.get('match', {}).get('team_A', {}).get('name', '')
    away_team_name = match_data.get('match', {}).get('team_B', {}).get('name', '')
    
    for team in standings:
        if team.get('team', {}).get('name') in [home_team_name, away_team_name]:
            print(f"\n  {team.get('team', {}).get('name')}:")
            print(f"    Siralama: {team.get('rank', 'N/A')}")
            print(f"    Puan: {team.get('points', 'N/A')}")
            print(f"    Oynanan: {team.get('played', 0)}")
            print(f"    Galibiyet: {team.get('won', 0)}")
            print(f"    Beraberlik: {team.get('draw', 0)}")
            print(f"    Maglubiyet: {team.get('lost', 0)}")
            print(f"    Atilan: {team.get('goals_pro', 0)}")
            print(f"    Yenilen: {team.get('goals_against', 0)}")
            print(f"    Averaj: {team.get('goal_difference', 0)}")
    
    print(f"\nONEMLI MI? ✅ EVET")
    print(f"  - Siralama farki (ust sirayla oynarken)")
    print(f"  - Puan farki")
    print(f"  - Gol averaji")
else:
    print("Puan durumu yok")

# 4. PROBABILITIES (Olasılıklar)
print("\n\n4. MAC OLASILIKLARI")
print("-"*80)

probabilities = match_data.get('mr_probabilities', {})

if probabilities:
    print(f"Ev sahibi: %{probabilities.get('home', 0)}")
    print(f"Beraberlik: %{probabilities.get('draw', 0)}")
    print(f"Deplasman: %{probabilities.get('away', 0)}")
    
    print(f"\nONEMLI MI? ⚠️  OPSIYONEL")
    print(f"  - Mackolik'in kendi tahminleri")
    print(f"  - Bizim analizimizle karsilastirabiliriz")

# 5. REFEREE (Hakem)
print("\n\n5. HAKEM BILGILERI")
print("-"*80)

referee = match_data.get('match', {}).get('referee', {})

if referee:
    print(f"Isim: {referee.get('name', 'N/A')}")
    print(f"Ortalama kirmizi kart: {referee.get('avg_rc', 'N/A')}")
    print(f"Ortalama sari kart: {referee.get('avg_yc', 'N/A')}")
    
    print(f"\nONEMLI MI? ⚠️  OPSIYONEL")
    print(f"  - Kart bahisleri icin kullanilabilir")
    print(f"  - MS tahmininde cok etkili degil")

# 6. INJURIES / SUSPENSIONS (Sakatlık/Ceza)
print("\n\n6. SAKATLIK / CEZA DURUMU")
print("-"*80)

injuries = match_data.get('injuries', {})
suspensions = match_data.get('suspensions', {})

if injuries or suspensions:
    print(f"Injuries: {len(injuries) if injuries else 0}")
    print(f"Suspensions: {len(suspensions) if suspensions else 0}")
    print(f"\nONEMLI MI? ✅ EVET (eger varsa)")
    print(f"  - Onemli oyuncu yoksa takim zayiflar")
else:
    print("Bu API'de sakatlik verisi yok (baska endpoint gerekebilir)")

# ÖZET
print("\n\n" + "="*80)
print("OZET - SAKLAMAMIZ GEREKEN VERILER:")
print("="*80)

print("""
1. H2H (Aralarindaki Maclar) - YUKSEK ONCELIK
   ✅ Son 10 mac
   ✅ Ev sahibi / deplasman / beraberlik sayilari
   ✅ Toplam gol ortalamasi
   ✅ KG (Karsilikli Gol) orani

2. FORM DURUMU - YUKSEK ONCELIK
   ✅ Her takim icin son 5 mac (W/D/L)
   ✅ Atilan gol ortalamasi (son 5 mac)
   ✅ Yenilen gol ortalamasi (son 5 mac)
   ✅ 2.5 Ust/Alt orani
   ✅ KG orani

3. PUAN DURUMU - ORTA ONCELIK
   ✅ Siralama (1. ile 20. farkli oynar)
   ✅ Puan
   ✅ Son 5 mac formu

4. MACKOLIK OLASILIKLARI - DUSUK ONCELIK
   ⚠️  Mackolik'in kendi tahmini
   ⚠️  Referans olarak kullanilabilir

5. HAKEM / SAKATLIK - OPSIYONEL
   ⚪ Ileri analiz icin

SUPABASE TABLO YAPISI:
-----------------------
Tablo: match_analysis
  - match_uuid (PK)
  - home_team, away_team
  - h2h_data (JSON: son maçlar, istatistikler)
  - form_home (JSON: son 5 maç, goller, seriler)
  - form_away (JSON: son 5 maç, goller, seriler)
  - standings_home (JSON: sıra, puan, averaj)
  - standings_away (JSON: sıra, puan, averaj)
  - probabilities (JSON: home/draw/away %)
  - fetched_at (timestamp)
""")

print("="*80)
print("\nSONRAKI ADIM: Bu verileri nasil kullanacagiz?")
print("  1. Bizim analiz algoritmamizla karsilastir")
print("  2. Kullaniciya 'Detayli Analiz' butonu goster")
print("  3. AI ile metinsel rapor olustur")

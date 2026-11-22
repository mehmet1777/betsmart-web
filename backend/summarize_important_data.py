"""
Match Detail API - SADECE ONEMLI VERILER
"""
import json

with open('match_detail_response.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

match_data = data.get('data', {})

print("MATCH DETAIL - ONEMLI VERILER OZETI")
print("="*80)

# Takım isimleri
home_team = match_data.get('match', {}).get('team_A', {}).get('name', 'N/A')
away_team = match_data.get('match', {}).get('team_B', {}).get('name', 'N/A')

print(f"\nMac: {home_team} vs {away_team}")
print("-"*80)

# 1. H2H - Aralarındaki Maçlar
print("\n1. ARALARINDAKI MACLAR (H2H)")
print("   Ne icerir:")
print("   - Son 10 mac skorlari")
print("   - Ev sahibi / Deplasman / Beraberlik sayilari")
print("   - Ortalama gol")

h2h = match_data.get('h2h', {})
if h2h:
    matches = h2h.get('matches', [])
    print(f"\n   Toplam mac: {len(matches)}")
    
    # Skorları say
    home_wins = 0
    away_wins = 0
    draws = 0
    
    for match in matches:
        score_a = match.get('fts_A', 0)
        score_b = match.get('fts_B', 0)
        team_a_name = match.get('team_A', {}).get('name', '')
        
        # Ev sahibi kim kazandı?
        if team_a_name == home_team:
            if score_a > score_b:
                home_wins += 1
            elif score_a < score_b:
                away_wins += 1
            else:
                draws += 1
        else:
            if score_a < score_b:
                home_wins += 1
            elif score_a > score_b:
                away_wins += 1
            else:
                draws += 1
    
    print(f"   {home_team}: {home_wins} galibiyet")
    print(f"   Beraberlik: {draws}")
    print(f"   {away_team}: {away_wins} galibiyet")

# 2. FORM DURUMU
print("\n2. FORM DURUMU")
print("   Ne icerir:")
print("   - Son 5 mac sonuclari (W/D/L)")
print("   - Atilan/Yenilen gol ortalamasi")
print("   - 2.5 Ust orani")
print("   - Karsilikli Gol orani")

forms = match_data.get('forms', {})
if forms:
    team_a_form = forms.get('team_A', {}).get('all_competitions', {})
    team_b_form = forms.get('team_B', {}).get('all_competitions', {})
    
    print(f"\n   {home_team}:")
    print(f"     Serie: {team_a_form.get('serie', 'N/A')}")  # WDLWW
    print(f"     Goller: {team_a_form.get('goal_pro', 0)} atilan, {team_a_form.get('goal_against', 0)} yenilen")
    print(f"     2.5 Ust: {team_a_form.get('over_2_goals', 0)}/5")
    print(f"     KG: {team_a_form.get('two_teams_scored', 0)}/5")
    
    print(f"\n   {away_team}:")
    print(f"     Serie: {team_b_form.get('serie', 'N/A')}")
    print(f"     Goller: {team_b_form.get('goal_pro', 0)} atilan, {team_b_form.get('goal_against', 0)} yenilen")
    print(f"     2.5 Ust: {team_b_form.get('over_2_goals', 0)}/5")
    print(f"     KG: {team_b_form.get('two_teams_scored', 0)}/5")

# 3. PUAN DURUMU (eğer varsa)
print("\n3. PUAN DURUMU (STANDINGS)")
print("   Ne icerir:")
print("   - Siralama")
print("   - Puan")
print("   - Averaj")

standings = match_data.get('standings', [])
if standings:
    for team in standings:
        team_name = team.get('team', {}).get('name', '')
        if team_name in [home_team, away_team]:
            print(f"\n   {team_name}:")
            print(f"     Sira: {team.get('rank', 'N/A')}")
            print(f"     Puan: {team.get('points', 'N/A')}")
            print(f"     Oynanan: {team.get('played', 0)} (G:{team.get('won', 0)} B:{team.get('draw', 0)} M:{team.get('lost', 0)})")
            print(f"     Averaj: {team.get('goal_difference', 0)}")

# 4. MACKOLIK OLASILIĞI
print("\n4. MACKOLIK TAHMINI")
print("   Ne icerir:")
print("   - Ev sahibi %")
print("   - Beraberlik %")
print("   - Deplasman %")

probs = match_data.get('mr_probabilities', {})
if probs:
    print(f"\n   Ev sahibi: %{probs.get('home', 0)}")
    print(f"   Beraberlik: %{probs.get('draw', 0)}")
    print(f"   Deplasman: %{probs.get('away', 0)}")

# ÖZET
print("\n\n" + "="*80)
print("KARAR: HANGI VERILER SAKLANMALI?")
print("="*80)

print("""
YUKSEK ONCELIK (Mutlaka sakla):
✅ 1. H2H (Aralarindaki Maclar)
     - Son 10 mac
     - Kazanan takim (home/draw/away)
     - Skorlar
     
✅ 2. FORM (Son 5 Mac)
     - Her takim icin W/D/L serisi
     - Atilan/Yenilen gol ortalamasi
     - 2.5 Ust orani (%)
     - KG orani (%)

ORTA ONCELIK (Kullanisli):
⚠️  3. PUAN DURUMU
     - Siralama (ust siralar daha guclu)
     - Puan farki
     - Averaj
     
DUSUK ONCELIK (Referans):
⚪ 4. MACKOLIK TAHMINI
     - Ev/Beraberlik/Deplasman %
     - Bizim tahminle karsilastir

SUPABASE TABLO:
--------------
CREATE TABLE match_details (
  id SERIAL PRIMARY KEY,
  match_uuid TEXT UNIQUE NOT NULL,
  home_team TEXT,
  away_team TEXT,
  match_date TIMESTAMP,
  
  -- H2H
  h2h_matches JSONB,  -- [{date, home, away, score_home, score_away}]
  h2h_home_wins INT,
  h2h_draws INT,
  h2h_away_wins INT,
  
  -- Form
  form_home_serie TEXT,  -- "WDLWW"
  form_home_goals_for FLOAT,
  form_home_goals_against FLOAT,
  form_home_over_25 INT,  -- 0-5
  form_home_btts INT,  -- 0-5
  
  form_away_serie TEXT,
  form_away_goals_for FLOAT,
  form_away_goals_against FLOAT,
  form_away_over_25 INT,
  form_away_btts INT,
  
  -- Standings (optional)
  standings_home_rank INT,
  standings_home_points INT,
  standings_away_rank INT,
  standings_away_points INT,
  
  -- Mackolik prediction
  prob_home INT,
  prob_draw INT,
  prob_away INT,
  
  fetched_at TIMESTAMP DEFAULT NOW()
);

KULLANIM:
--------
1. /yeniveri calisinca:
   - Her mac icin uuid sakla
   - match_details API'yi cagir
   - Verileri parse et ve Supabase'e kaydet

2. Web sitesinde:
   - Mac kartinda "Detayli Analiz" butonu
   - Butona tiklayinca match_details'ten veri cek
   - Kullaniciya goster:
     * Aralarindaki son maclar
     * Form karsilastirmasi
     * AI tahmin raporu

3. Bizim analiz algoritmasiyla birlestir:
   - H2H verisini skorlamaya ekle
   - Form verisini skorlamaya ekle
   - Daha isabetli tahmin!
""")

print("="*80)
print("\nONAY GEREKLIMI?")
print("  Bu tasarimla devam edelim mi?")
print("  Yoksa baska veriler de ekleyelim mi?")

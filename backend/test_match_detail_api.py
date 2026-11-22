"""
Sahadan Match Detail API Test
Takım karşılaştırmaları, form durumu, aralarındaki maçlar
"""
import requests
import json

# Senin verdiğin örnek
test_uuid = "7tto7hbwd8o4wifwovvhbk1zo"

url = f"https://www.sahadan.com/api/index/match-detail?application=com.kokteyl.mackolik&language=tr&country=tr&e=sam&match_uuid={test_uuid}&a=bs"

print("SAHADAN MATCH DETAIL API TEST")
print("="*80)
print(f"Test UUID: {test_uuid}")
print(f"URL: {url}\n")

headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/json',
    'Referer': 'https://www.sahadan.com/'
}

try:
    response = requests.get(url, headers=headers, timeout=30)
    
    print(f"Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.json()
        
        # JSON yapısını incele
        print("="*80)
        print("JSON YAPISI:")
        print("="*80)
        
        # Ana keyler
        print("\nAna Keys:")
        for key in data.keys():
            print(f"  - {key}")
        
        # Match bilgileri
        if 'data' in data:
            match_data = data['data']
            
            print("\n" + "="*80)
            print("MAC BILGILERI:")
            print("="*80)
            
            # Takım isimleri
            home_team = match_data.get('home_team', {}).get('name', 'Unknown')
            away_team = match_data.get('away_team', {}).get('name', 'Unknown')
            
            print(f"\nMac: {home_team} vs {away_team}")
            print(f"Tarih: {match_data.get('date', 'N/A')} {match_data.get('time', 'N/A')}")
            print(f"Lig: {match_data.get('league', {}).get('name', 'N/A')}")
            
            # Aralarındaki maçlar (Head to Head)
            if 'head_to_head' in match_data:
                h2h = match_data['head_to_head']
                
                print("\n" + "="*80)
                print("ARALARINDAKI MACLAR (Head to Head):")
                print("="*80)
                
                if isinstance(h2h, list):
                    print(f"\nToplam {len(h2h)} mac bulundu:")
                    
                    for idx, match in enumerate(h2h[:5], 1):  # İlk 5'i göster
                        date = match.get('date', 'N/A')
                        home = match.get('home_team', {}).get('name', 'N/A')
                        away = match.get('away_team', {}).get('name', 'N/A')
                        score = match.get('score', 'N/A')
                        
                        print(f"  {idx}. {date}: {home} {score} {away}")
            
            # Form durumu
            if 'form' in match_data:
                form_data = match_data['form']
                
                print("\n" + "="*80)
                print("FORM DURUMU:")
                print("="*80)
                
                # Ev sahibi formu
                if 'home' in form_data:
                    home_form = form_data['home']
                    print(f"\n{home_team} - Son Maclar:")
                    
                    if isinstance(home_form, list):
                        for idx, match in enumerate(home_form[:5], 1):
                            date = match.get('date', 'N/A')
                            home = match.get('home_team', {}).get('name', 'N/A')
                            away = match.get('away_team', {}).get('name', 'N/A')
                            score = match.get('score', 'N/A')
                            result = match.get('result', 'N/A')  # W/D/L
                            
                            result_icon = "✅" if result == 'W' else "⚪" if result == 'D' else "❌"
                            print(f"  {idx}. {date}: {home} {score} {away} {result_icon}")
                
                # Deplasman formu
                if 'away' in form_data:
                    away_form = form_data['away']
                    print(f"\n{away_team} - Son Maclar:")
                    
                    if isinstance(away_form, list):
                        for idx, match in enumerate(away_form[:5], 1):
                            date = match.get('date', 'N/A')
                            home = match.get('home_team', {}).get('name', 'N/A')
                            away = match.get('away_team', {}).get('name', 'N/A')
                            score = match.get('score', 'N/A')
                            result = match.get('result', 'N/A')
                            
                            result_icon = "✅" if result == 'W' else "⚪" if result == 'D' else "❌"
                            print(f"  {idx}. {date}: {home} {score} {away} {result_icon}")
            
            # İstatistikler
            if 'statistics' in match_data:
                stats = match_data['statistics']
                
                print("\n" + "="*80)
                print("ISTATISTIKLER:")
                print("="*80)
                print(json.dumps(stats, indent=2, ensure_ascii=False)[:500])
        
        # Ham JSON'u kaydet (inceleme için)
        with open('match_detail_response.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print("\n" + "="*80)
        print("Tam JSON 'match_detail_response.json' dosyasina kaydedildi")
        
    else:
        print(f"API Hatasi: {response.status_code}")
        print(response.text[:500])

except Exception as e:
    print(f"Hata: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("SONRAKI ADIM:")
print("  1. match_uuid nasil bulunur? (Bultenden mac secince)")
print("  2. Hangi veriler analiz icin onemli?")
print("  3. Supabase'de nasil saklanir?")

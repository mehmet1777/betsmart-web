import re
from bs4 import BeautifulSoup

# HTML'i oku
with open('debug_html.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script')

print(f"📄 Toplam script tag: {len(scripts)}")

# Tüm scriptlerde __NUXT__ ara
for i, script in enumerate(scripts):
    if script.string:
        if '__NUXT__' in script.string or 'events' in script.string or 'fixtures' in script.string:
            script_text = script.string
            
            # Çok uzunsa sadece anahtar kelimeleri kontrol et
            has_nuxt = '__NUXT__' in script_text
            has_events = '"events"' in script_text or "'events'" in script_text
            has_matches = '"matches"' in script_text or "'matches'" in script_text
            has_fixtures = '"fixtures"' in script_text or "'fixtures'" in script_text
            
            if has_nuxt or has_events or has_matches or has_fixtures:
                print(f"\n✅ Script #{i}:")
                print(f"   Uzunluk: {len(script_text)}")
                print(f"   __NUXT__: {has_nuxt}")
                print(f"   events: {has_events}")
                print(f"   matches: {has_matches}")
                print(f"   fixtures: {has_fixtures}")
                
                if len(script_text) < 3000:
                    print(f"   İçerik (ilk 300 kar):")
                    print(f"   {script_text[:300]}")


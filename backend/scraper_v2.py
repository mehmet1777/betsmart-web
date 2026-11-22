from bs4 import BeautifulSoup
import re
import json

class BulletinScraperV2:
    """Geliştirilmiş Bülten Scraper - Selenium HTML'den veri çıkarma"""
    
    def __init__(self):
        pass
    
    def parse_html(self, html_content):
        """HTML'den maç verilerini çıkar"""
        soup = BeautifulSoup(html_content, 'html.parser')
        matches = []
        
        print(f"📄 HTML uzunluğu: {len(html_content)} karakter")
        print(f"🔍 Parser V2 başladı...")
        
        # Yöntem 1: __NUXT__ JSON'undan çek
        print("\n🔍 Yöntem 1: __NUXT__ JSON parsing...")
        matches = self._parse_nuxt_json(soup)
        
        if matches:
            print(f"✅ {len(matches)} maç bulundu (Yöntem 1)")
            return matches
        
        # Yöntem 2: Table/TR yapısından çek
        print("\n🔍 Yöntem 2: Table parsing...")
        matches = self._parse_tables(soup)
        
        if matches:
            print(f"✅ {len(matches)} maç bulundu (Yöntem 2)")
            return matches
        
        # Yöntem 3: Genel DOM tarama
        print("\n🔍 Yöntem 3: DOM scanning...")
        matches = self._parse_dom(soup)
        
        if matches:
            print(f"✅ {len(matches)} maç bulundu (Yöntem 3)")
            return matches
        
        print("❌ Hiçbir yöntem maç bulamadı")
        return []
    
    def _parse_nuxt_json(self, soup):
        """__NUXT__ değişkeninden maçları çıkar"""
        matches = []
        
        try:
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string and 'window.__NUXT__' in script.string:
                    print("   ✅ window.__NUXT__ bulundu")
                    
                    # JSON'u çıkar
                    script_text = script.string
                    
                    # window.__NUXT__={...} kısmını bul
                    start_idx = script_text.find('window.__NUXT__')
                    if start_idx == -1:
                        continue
                    
                    # = işaretinden sonra başla
                    json_start = script_text.find('=', start_idx) + 1
                    
                    # Basit yöntem: tüm scripti al ve eval kullanmadan parse et
                    # Sahadan'da maç verileri genelde text içinde görünüyor
                    
                    # Takım isimlerini regex ile bul
                    # Örnek: "team_A":"Fenerbahçe","team_B":"Galatasaray"
                    team_pattern = r'"team_A"\s*:\s*"([^"]+)"\s*,\s*"team_B"\s*:\s*"([^"]+)"'
                    team_matches = re.findall(team_pattern, script_text)
                    
                    print(f"   📊 {len(team_matches)} takım çifti bulundu")
                    
                    for home, away in team_matches:
                        if home and away:
                            match = {
                                'home_team': home,
                                'away_team': away,
                                'time': '',
                                'date': '',
                                'league': '',
                                'score': '',
                                'half_score': '',
                                'odd_1': 0,
                                'odd_x': 0,
                                'odd_2': 0,
                                'over': 0,
                                'under': 0,
                                'mbs': 0
                            }
                            matches.append(match)
                            print(f"   ✅ Maç: {home} vs {away}")
                    
                    if matches:
                        return matches
        
        except Exception as e:
            print(f"   ❌ NUXT parse hatası: {e}")
        
        return matches
    
    def _parse_tables(self, soup):
        """Table yapısından maçları çıkar"""
        matches = []
        
        try:
            tables = soup.find_all('table')
            print(f"   📊 {len(tables)} tablo bulundu")
            
            for table in tables:
                rows = table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    
                    # En az 3 hücre olmalı (takım1, vs, takım2 gibi)
                    if len(cells) >= 3:
                        # Hücrelerdeki metinleri al
                        texts = [cell.get_text(strip=True) for cell in cells]
                        
                        # Takım isimleri ara (3+ karakter, sayı değil)
                        teams = []
                        for text in texts:
                            if (len(text) > 3 and 
                                not text.replace('.', '').replace(',', '').isdigit() and
                                not re.match(r'^\d{1,2}:\d{2}$', text)):  # Saat değil
                                teams.append(text)
                        
                        # En az 2 takım bulunduysa
                        if len(teams) >= 2:
                            match = {
                                'home_team': teams[0],
                                'away_team': teams[1],
                                'time': '',
                                'date': '',
                                'league': '',
                                'score': '',
                                'half_score': '',
                                'odd_1': 0,
                                'odd_x': 0,
                                'odd_2': 0,
                                'over': 0,
                                'under': 0,
                                'mbs': 0
                            }
                            
                            # Oranları ara (1.50 formatı)
                            for text in texts:
                                if re.match(r'^\d+\.\d{2}$', text):
                                    odd_val = float(text)
                                    if 1.01 <= odd_val <= 50:
                                        if match['odd_1'] == 0:
                                            match['odd_1'] = odd_val
                                        elif match['odd_x'] == 0:
                                            match['odd_x'] = odd_val
                                        elif match['odd_2'] == 0:
                                            match['odd_2'] = odd_val
                            
                            matches.append(match)
                            print(f"   ✅ Maç: {match['home_team']} vs {match['away_team']}")
        
        except Exception as e:
            print(f"   ❌ Table parse hatası: {e}")
        
        return matches
    
    def _parse_dom(self, soup):
        """Genel DOM tarama ile maçları bul"""
        matches = []
        
        try:
            # Tüm text içeriğini al
            page_text = soup.get_text()
            
            # "vs" veya " - " içeren satırları ara
            lines = page_text.split('\n')
            
            for line in lines:
                line = line.strip()
                
                # "Fenerbahçe - Galatasaray" veya "Fenerbahçe vs Galatasaray" formatı
                if ' - ' in line and len(line) < 100:  # Çok uzun satırları atla
                    parts = line.split(' - ')
                    if len(parts) == 2:
                        home = parts[0].strip()
                        away = parts[1].strip()
                        
                        # Geçerli takım isimleri mi?
                        if (3 < len(home) < 50 and 3 < len(away) < 50 and
                            home.replace(' ', '').isalpha() and 
                            away.replace(' ', '').isalpha()):
                            
                            match = {
                                'home_team': home,
                                'away_team': away,
                                'time': '',
                                'date': '',
                                'league': '',
                                'score': '',
                                'half_score': '',
                                'odd_1': 0,
                                'odd_x': 0,
                                'odd_2': 0,
                                'over': 0,
                                'under': 0,
                                'mbs': 0
                            }
                            matches.append(match)
                            print(f"   ✅ Maç: {home} vs {away}")
        
        except Exception as e:
            print(f"   ❌ DOM parse hatası: {e}")
        
        return matches
    
    def validate_matches(self, matches):
        """Maç verilerini doğrula ve temizle"""
        valid_matches = []
        seen = set()
        
        for match in matches:
            # Minimum gereksinimler
            if not (match.get('home_team') and match.get('away_team')):
                continue
            
            # Duplicate kontrolü
            key = f"{match['home_team']}_{match['away_team']}"
            if key in seen:
                continue
            
            seen.add(key)
            valid_matches.append(match)
        
        print(f"\n📊 {len(valid_matches)} geçerli maç (duplike temizlendi)")
        return valid_matches

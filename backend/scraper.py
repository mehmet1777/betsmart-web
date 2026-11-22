from bs4 import BeautifulSoup
import re

class BulletinScraper:
    """Bahis sitelerinden bülten çekme modülü"""
    
    def __init__(self):
        pass
    
    def parse_html(self, html_content):
        """HTML'den maç verilerini çıkar (genel parser)"""
        soup = BeautifulSoup(html_content, 'html.parser')
        matches = []
        
        print(f"📄 HTML uzunluğu: {len(html_content)} karakter")
        print(f"🔍 Parser başladı...")
        
        # Farklı site yapıları için multiple parser deneyelim
        parsers = [
            self._parse_sahadan,
            self._parse_generic_table,
            self._parse_div_structure,
            self._parse_nesine,
            self._parse_bilyoner,
        ]
        
        for parser in parsers:
            try:
                print(f"   Deneniyor: {parser.__name__}")
                matches = parser(soup)
                if matches:
                    print(f"✅ {len(matches)} maç bulundu ({parser.__name__})")
                    return matches
                else:
                    print(f"   ❌ {parser.__name__} maç bulamadı")
            except Exception as e:
                print(f"   ❌ Parser hatası ({parser.__name__}): {e}")
                continue
        
        print(f"⚠️ Hiçbir parser maç bulamadı")
        return matches
    
    def _parse_generic_table(self, soup):
        """Genel tablo yapısı parser"""
        matches = []
        tables = soup.find_all('table')
        
        for table in tables:
            rows = table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                
                # En az 10 sütun olmalı (maç bilgileri için)
                if len(cells) >= 10:
                    try:
                        match = self._extract_match_from_cells(cells)
                        if match and match.get('home_team') and match.get('away_team'):
                            matches.append(match)
                    except:
                        continue
        
        return matches
    
    def _parse_div_structure(self, soup):
        """Div tabanlı yapı parser"""
        matches = []
        
        # Yaygın class isimleri
        match_containers = soup.find_all(['div', 'article'], 
            class_=re.compile(r'(match|game|event|fixture)', re.I))
        
        for container in match_containers:
            try:
                # Takım isimlerini bul
                teams = container.find_all(class_=re.compile(r'(team|participant)', re.I))
                
                if len(teams) >= 2:
                    # Oranları bul
                    odds = container.find_all(class_=re.compile(r'(odd|rate|coef)', re.I))
                    
                    match = {
                        'home_team': teams[0].get_text(strip=True),
                        'away_team': teams[1].get_text(strip=True),
                        'odd_1': self._extract_number(odds[0]) if len(odds) > 0 else 0,
                        'odd_x': self._extract_number(odds[1]) if len(odds) > 1 else 0,
                        'odd_2': self._extract_number(odds[2]) if len(odds) > 2 else 0,
                    }
                    
                    matches.append(match)
            except:
                continue
        
        return matches
    
    def _parse_nesine(self, soup):
        """Nesine.com özel parser"""
        matches = []
        # Nesine'ye özel HTML yapısı burada
        return matches
    
    def _parse_sahadan(self, soup):
        """Sahadan.com özel parser - JSON veriden"""
        matches = []
        
        try:
            # Sahadan script tagında JSON veri var
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string and '__NUXT__' in script.string:
                    print("   ✅ __NUXT__ script bulundu")
                    
                    # JSON veriyi bul - Sahadan'ın özel yapısı
                    import re
                    import json
                    
                    script_text = script.string
                    
                    # window.__NUXT__={...} formatını ara
                    # Sahadan'da genelde: window.__NUXT__={};window.__NUXT__.config=...
                    # veya window.__NUXT__={data...}
                    
                    # Önce tüm __NUXT__ değişkenlerini bul
                    nuxt_pattern = r'window\.__NUXT__(?:\.[a-zA-Z_$][a-zA-Z0-9_$]*)?\s*=\s*(\{[^;]*\})'
                    nuxt_matches = re.finditer(nuxt_pattern, script_text)
                    
                    all_data = {}
                    for nuxt_match in nuxt_matches:
                        try:
                            json_str = nuxt_match.group(1)
                            if json_str != '{}':  # Boş objeyi atla
                                parsed = json.loads(json_str)
                                # Tüm dataları birleştir
                                if isinstance(parsed, dict):
                                    all_data.update(parsed)
                        except:
                            continue
                    
                    match = None  # Eski match değişkenini temizle
                    
                    match = None  # Eski match değişkenini temizle
                    
                    if all_data:
                        print(f"   📄 Birleştirilmiş JSON boyutu: {len(str(all_data))} karakter")
                        print(f"   🔑 Ana keyler: {list(all_data.keys())[:10]}")
                        
                        try:
                            # JSON'u parse et
                            data = all_data
                            print("   ✅ JSON başarıyla birleştirildi")
                            
                            # State içinde data var mı?
                            if 'state' in data:
                                print("   🔍 'state' bulundu, içerik kontrol ediliyor...")
                                
                                # Sahadan'da genelde state.$siddaa veya state.$sfixtures gibi
                                # Tüm state keylerini incele
                                for key, value in data['state'].items():
                                    if isinstance(value, dict):
                                        # Maçları ara
                                        found_matches = self._extract_sahadan_matches_v2(value)
                                        if found_matches:
                                            print(f"   ✅ '{key}' içinde {len(found_matches)} maç bulundu")
                                            matches.extend(found_matches)
                                
                                if matches:
                                    return matches
                            
                            # data içinde doğrudan maçlar var mı?
                            else:
                                print("   🔍 Root level'da maç aranıyor...")
                                matches = self._extract_sahadan_matches_v2(data)
                                if matches:
                                    return matches
                        
                        except json.JSONDecodeError as e:
                            print(f"   ❌ JSON parse hatası: {e}")
                            # JSON hatasını debug et
                            error_pos = e.pos
                            start = max(0, error_pos - 50)
                            end = min(len(json_str), error_pos + 50)
                            print(f"   Hata konumu: ...{json_str[start:end]}...")
                        except Exception as e:
                            print(f"   ❌ Parser hatası: {e}")
        
        except Exception as e:
            print(f"   ❌ Sahadan genel hata: {e}")
        
        return matches
    
    def _extract_sahadan_matches(self, data, matches=None):
        """Nested JSON'dan maçları çıkar"""
        if matches is None:
            matches = []
        
        if isinstance(data, dict):
            # Maç objesi mi kontrol et
            if all(k in data for k in ['team_A', 'team_B', 'time']):
                match = {
                    'time': str(data.get('time', '')),
                    'league': '',
                    'home_team': str(data.get('team_A', '')),
                    'away_team': str(data.get('team_B', '')),
                    'score': '',
                    'half_score': '',
                    'odd_1': 0,
                    'odd_x': 0,
                    'odd_2': 0,
                    'date': '',
                    'over': 0,
                    'under': 0,
                    'mbs': 0
                }
                
                # Oranları bul (markets içinde)
                if 'markets' in data:
                    markets = data['markets']
                    for market in markets:
                        if isinstance(market, dict) and 'i' in market:
                            # İddaa oranları genelde 'i' değeri 21 olanda
                            if market.get('i') == 21:
                                # Odds listesini bul
                                if 'o' in market:
                                    odds_list = market['o']
                                    if isinstance(odds_list, list) and len(odds_list) > 0:
                                        # İlk elemandan oranları çıkar
                                        # Bu karmaşık nested yapı, basitleştir
                                        pass
                
                if match['home_team'] and match['away_team']:
                    matches.append(match)
            
            # Recursive olarak tüm dict'leri tara
            for value in data.values():
                self._extract_sahadan_matches(value, matches)
        
        elif isinstance(data, list):
            for item in data:
                self._extract_sahadan_matches(item, matches)
        
        return matches
    
    def _extract_sahadan_matches_v2(self, data, matches=None):
        """Gelişmiş Sahadan maç çıkarıcı - tüm olası formatları dene"""
        if matches is None:
            matches = []
        
        if isinstance(data, dict):
            # Format 1: events arrayi (Sahadan'ın yeni formatı)
            if 'events' in data and isinstance(data['events'], list):
                print(f"      'events' array bulundu: {len(data['events'])} element")
                
                for event in data['events']:
                    if isinstance(event, dict):
                        match = self._parse_sahadan_event(event)
                        if match and match.get('home_team'):
                            matches.append(match)
            
            # Format 2: matches arrayi
            elif 'matches' in data and isinstance(data['matches'], list):
                print(f"      'matches' array bulundu: {len(data['matches'])} element")
                
                for match_data in data['matches']:
                    if isinstance(match_data, dict):
                        match = self._parse_sahadan_event(match_data)
                        if match and match.get('home_team'):
                            matches.append(match)
            
            # Format 3: data arrayi
            elif 'data' in data:
                if isinstance(data['data'], list):
                    print(f"      'data' array bulundu: {len(data['data'])} element")
                    for item in data['data']:
                        sub_matches = self._extract_sahadan_matches_v2(item)
                        matches.extend(sub_matches)
                elif isinstance(data['data'], dict):
                    sub_matches = self._extract_sahadan_matches_v2(data['data'])
                    matches.extend(sub_matches)
            
            # Format 4: Doğrudan maç objesi
            else:
                match = self._parse_sahadan_event(data)
                if match and match.get('home_team'):
                    matches.append(match)
        
        elif isinstance(data, list):
            # Liste ise her elemanı kontrol et
            for item in data:
                if isinstance(item, dict):
                    sub_matches = self._extract_sahadan_matches_v2(item)
                    matches.extend(sub_matches)
        
        return matches
    
    def _parse_sahadan_event(self, event):
        """Sahadan event objesinden maç bilgisi çıkar"""
        if not isinstance(event, dict):
            return None
        
        match = {
            'date': '',
            'time': '',
            'league': '',
            'home_team': '',
            'away_team': '',
            'score': '',
            'half_score': '',
            'odd_1': 0,
            'odd_x': 0,
            'odd_2': 0,
            'over': 0,
            'under': 0,
            'mbs': 0
        }
        
        # Takım isimlerini bul (çeşitli format kombinasyonları)
        # Format 1: home/away veya homeTeam/awayTeam
        if 'home' in event:
            match['home_team'] = str(event['home'].get('name', '')) if isinstance(event['home'], dict) else str(event.get('home', ''))
        elif 'homeTeam' in event:
            match['home_team'] = str(event['homeTeam'].get('name', '')) if isinstance(event['homeTeam'], dict) else str(event.get('homeTeam', ''))
        elif 'home_team' in event:
            match['home_team'] = str(event.get('home_team', ''))
        elif 'team_A' in event:
            match['home_team'] = str(event.get('team_A', ''))
        elif 'teamA' in event:
            match['home_team'] = str(event.get('teamA', ''))
        
        if 'away' in event:
            match['away_team'] = str(event['away'].get('name', '')) if isinstance(event['away'], dict) else str(event.get('away', ''))
        elif 'awayTeam' in event:
            match['away_team'] = str(event['awayTeam'].get('name', '')) if isinstance(event['awayTeam'], dict) else str(event.get('awayTeam', ''))
        elif 'away_team' in event:
            match['away_team'] = str(event.get('away_team', ''))
        elif 'team_B' in event:
            match['away_team'] = str(event.get('team_B', ''))
        elif 'teamB' in event:
            match['away_team'] = str(event.get('teamB', ''))
        
        # Saat bilgisi
        if 'time' in event:
            match['time'] = str(event.get('time', ''))
        elif 'startTime' in event:
            match['time'] = str(event.get('startTime', ''))
        elif 'kickoff' in event:
            match['time'] = str(event.get('kickoff', ''))
        
        # Lig bilgisi
        if 'league' in event:
            match['league'] = str(event['league'].get('name', '')) if isinstance(event['league'], dict) else str(event.get('league', ''))
        elif 'competition' in event:
            match['league'] = str(event['competition'].get('name', '')) if isinstance(event['competition'], dict) else str(event.get('competition', ''))
        elif 'tournament' in event:
            match['league'] = str(event['tournament'].get('name', '')) if isinstance(event['tournament'], dict) else str(event.get('tournament', ''))
        
        # Oranlar - çeşitli formatlar
        # Format 1: odds objesi
        if 'odds' in event and isinstance(event['odds'], dict):
            odds = event['odds']
            match['odd_1'] = float(odds.get('1', 0) or odds.get('home', 0) or 0)
            match['odd_x'] = float(odds.get('x', 0) or odds.get('draw', 0) or odds.get('0', 0) or 0)
            match['odd_2'] = float(odds.get('2', 0) or odds.get('away', 0) or 0)
        
        # Format 2: markets arrayi
        elif 'markets' in event and isinstance(event['markets'], list):
            for market in event['markets']:
                if isinstance(market, dict):
                    # MBS (1X2) marketini bul
                    market_type = market.get('type', '') or market.get('i', '') or market.get('id', '')
                    
                    # 1X2 veya MBS marketini ara
                    if market_type in [1, '1', 'MBS', '1X2', 21]:
                        # Outcomes/odds arrayi
                        outcomes = market.get('outcomes', []) or market.get('o', []) or market.get('odds', [])
                        
                        if isinstance(outcomes, list) and len(outcomes) >= 3:
                            # İlk 3 oran: 1-X-2
                            match['odd_1'] = float(outcomes[0].get('odd', 0) if isinstance(outcomes[0], dict) else outcomes[0])
                            match['odd_x'] = float(outcomes[1].get('odd', 0) if isinstance(outcomes[1], dict) else outcomes[1])
                            match['odd_2'] = float(outcomes[2].get('odd', 0) if isinstance(outcomes[2], dict) else outcomes[2])
                            break
        
        # Format 3: Direkt odd_1, odd_x, odd_2
        elif 'odd_1' in event:
            match['odd_1'] = float(event.get('odd_1', 0) or 0)
            match['odd_x'] = float(event.get('odd_x', 0) or 0)
            match['odd_2'] = float(event.get('odd_2', 0) or 0)
        
        # MBS varsa al
        if 'mbs' in event:
            match['mbs'] = float(event.get('mbs', 0) or 0)
        
        # Over/Under
        if 'over' in event:
            match['over'] = float(event.get('over', 0) or 0)
        if 'under' in event:
            match['under'] = float(event.get('under', 0) or 0)
        
        # Eğer en az takım isimleri varsa match'i döndür
        if match['home_team'] and match['away_team']:
            return match
        
        return None
    
    def _parse_bilyoner(self, soup):
        """Bilyoner.com özel parser"""
        matches = []
        # Bilyoner'e özel HTML yapısı burada
        return matches
    
    def _extract_match_from_cells(self, cells):
        """Hücrelerden maç bilgisi çıkar"""
        match = {
            'date': '',
            'time': '',
            'league': '',
            'home_team': '',
            'away_team': '',
            'score': '',
            'half_score': '',
            'odd_1': 0,
            'odd_x': 0,
            'odd_2': 0,
            'over': 0,
            'under': 0,
            'mbs': 0
        }
        
        # Hücreleri oku
        for i, cell in enumerate(cells):
            text = cell.get_text(strip=True)
            
            # Tarih/saat pattern
            if re.match(r'\d{1,2}:\d{2}', text):
                match['time'] = text
            
            # Takım isimleri (kelime içeren, sayı olmayan)
            elif text and not text.replace('.', '').replace(',', '').isdigit():
                if not match['home_team']:
                    match['home_team'] = text
                elif not match['away_team'] and text != match['home_team']:
                    match['away_team'] = text
                elif not match['league']:
                    match['league'] = text
            
            # Oranlar (1.50 formatında)
            elif re.match(r'\d+\.\d+', text):
                odd_val = float(text)
                if 1.01 <= odd_val <= 50:  # Geçerli oran aralığı
                    if match['odd_1'] == 0:
                        match['odd_1'] = odd_val
                    elif match['odd_x'] == 0:
                        match['odd_x'] = odd_val
                    elif match['odd_2'] == 0:
                        match['odd_2'] = odd_val
        
        return match
    
    def _extract_number(self, element):
        """Elemandan sayı çıkar"""
        try:
            text = element.get_text(strip=True)
            # Sadece sayıları al
            number = re.findall(r'\d+\.?\d*', text)
            if number:
                return float(number[0])
        except:
            pass
        return 0
    
    def validate_matches(self, matches):
        """Maç verilerini doğrula ve temizle"""
        valid_matches = []
        
        for match in matches:
            # Minimum gereksinimler
            if (match.get('home_team') and 
                match.get('away_team') and
                match.get('odd_1', 0) > 1.0):
                valid_matches.append(match)
        
        return valid_matches

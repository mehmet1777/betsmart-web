"""
Mackolik AJAX API - Direkt JSON ile veri çekme
"""
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import re

def fetch_mackolik_matches(days_ahead=2, status_callback=None):
    """
    Mackolik AJAX API'den maç verilerini çek
    
    Args:
        days_ahead: Kaç gün sonrasına kadar maçları çek
        
    Returns:
        (success: bool, matches: list, error: str)
    """
    try:
        all_matches = []
        use_time_view = False  # İlk gün LİG'de bulamazsak, hep SAAT kullan
        
        # Bugünden itibaren belirtilen gün sayısı kadar çek
        for day in range(days_ahead):
            target_date = datetime.now() + timedelta(days=day)
            date_str = target_date.strftime("%d.%m.%Y")
            
            print(f"[{date_str}] tarihi cekiliyor...")
            
            # İlk günden sonra eğer LİG çalışmadıysa, direkt SAAT kullan
            if use_time_view:
                print(f"   ℹ️  SAAT görünümü kullanılıyor (önceki deneyimden)")
                byKickOffTime = "true"
            else:
                byKickOffTime = "false"
            
            # Mackolik AJAX API URL
            url = (
                f"https://www.mackolik.com/ajax/iddaa/events/soccer"
                f"?byKickOffTime={byKickOffTime}"
                f"&competitionId="
                f"&selectedDate={date_str}"
                f"&eventUrlPrefixType=iddaaPage"
                f"&eventUrlSuffixType=iddaaPage"
                f"&googleAnalyticsAction=IddaaOddsClick"
                f"&googleAnalyticsCategory=IddaaOddsClick"
                f"&googleAnalyticsLabel=Iddaa%20Page%20Odds%20Click"
            )
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Referer': 'https://www.mackolik.com/iddaa'
            }
            
            # Retry mekanizması: 3 kez dene
            max_retries = 3
            response = None
            last_error = None
            
            for attempt in range(max_retries):
                try:
                    response = requests.get(url, headers=headers, timeout=30)
                    break  # Başarılı, döngüden çık
                except requests.exceptions.Timeout:
                    last_error = f"Timeout (deneme {attempt + 1}/{max_retries})"
                    print(f"⏳ {last_error}")
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(2)  # 2 saniye bekle ve tekrar dene
                    continue
                except Exception as e:
                    last_error = str(e)
                    print(f"❌ Hata: {last_error}")
                    break
            
            if response is None:
                print(f"❌ {date_str} çekilemedi: {last_error}")
                continue
            
            if response.status_code != 200:
                print(f"❌ API hatası: {response.status_code}")
                continue
            
            data = response.json()
            
            if data.get('status') != 'success':
                print(f"❌ API response başarısız")
                continue
            
            # HTML'i parse et
            html = data.get('data', {}).get('html', '')
            
            if not html or 'Veri yok' in html:
                # Sadece ilk günde LİG denediyse ve bulamadıysa
                if not use_time_view:
                    if status_callback:
                        status_callback(f"date_{date_str}_trying_time_view")
                    
                    print(f"⚠️  LİG görünümünde maç yok, SAAT görünümü deneniyor...")
                    use_time_view = True  # Bundan sonra hep SAAT kullan
                    
                    # SAAT görünümünü dene (byKickOffTime=true)
                    url_time = url.replace('byKickOffTime=false', 'byKickOffTime=true')
                    
                    try:
                        response = requests.get(url_time, headers=headers, timeout=30)
                        if response.status_code == 200:
                            data = response.json()
                            html = data.get('data', {}).get('html', '')
                            print(f"✅ SAAT görünümü kullanılıyor")
                    except:
                        pass
                else:
                    # Zaten SAAT kullanıyoruz, yine bulamadık
                    print(f"⚠️  Bu tarihte maç yok")
            
            if not html or 'Veri yok' in html:
                print(f"⚠️  HTML boş, atlanıyor")
                continue
            
            # BeautifulSoup ile parse
            soup = BeautifulSoup(html, 'html.parser')
            
            # Lig başlıklarını bul
            competition_sections = soup.find_all('section', class_='widget-iddaa-events__competition-section')
            
            for section in competition_sections:
                # Lig adını al
                league_name_elem = section.find('div', class_='widget-iddaa-events__competition-name')
                if league_name_elem:
                    league_link = league_name_elem.find('a')
                    league_name = league_link.text.strip() if league_link else 'Unknown'
                else:
                    league_name = 'Unknown'
                
                # Maçları bul
                rows = section.find_all('tr', class_='widget-iddaa-events__row--markets-summary')
                
                print(f"  [{league_name}]: {len(rows)} mac satiri bulundu")
                
                for row in rows:
                    try:
                        # Saat - UTC bilgisi satırda data-utc olarak
                        time_cell = row.find('td', {'data-dateformat': 'time'})
                        if time_cell:
                            match_time = time_cell.text.strip()
                        else:
                            # Alternatif: Bir önceki selection row'dan al
                            prev_row = row.find_previous_sibling('tr', class_='widget-iddaa-events__row--selections')
                            if prev_row:
                                time_cell = prev_row.find('td', {'data-dateformat': 'time'})
                                match_time = time_cell.text.strip() if time_cell else ''
                            else:
                                match_time = ''
                        
                        # Takımlar - brief-details içinde
                        brief_details = row.find('div', class_='widget-iddaa-events__brief-details')
                        if not brief_details:
                            continue
                        
                        team_links = brief_details.find_all('a', class_='widget-iddaa-events__team-name')
                        if len(team_links) < 2:
                            continue
                        
                        home_team = team_links[0].text.strip()
                        away_team = team_links[1].text.strip()
                        
                        # Match ID'yi bul - takım linklerinden birinden çıkar
                        # Format: /mac/MATCHID/team-vs-team
                        mackolik_match_id = None
                        for link in team_links:
                            href = link.get('href', '')
                            match_id_search = re.search(r'/mac/(\d+)/', href)
                            if match_id_search:
                                mackolik_match_id = match_id_search.group(1)
                                break
                        
                        print(f"    -> {home_team} vs {away_team} - {match_time}")
                        
                        # Oranlar - tablodaki value span'larını bul
                        value_spans = row.find_all('span', class_='widget-iddaa-events__value')
                        
                        odd_1 = None
                        odd_x = None
                        odd_2 = None
                        over_25 = None
                        under_25 = None
                        
                        # İlk 3 hücre: 1, X, 2 (Maç Sonucu)
                        if len(value_spans) >= 3:
                            try:
                                val = value_spans[0].text.strip()
                                if val and val != '-':
                                    odd_1 = float(val)
                            except:
                                pass
                            try:
                                val = value_spans[1].text.strip()
                                if val and val != '-':
                                    odd_x = float(val)
                            except:
                                pass
                            try:
                                val = value_spans[2].text.strip()
                                if val and val != '-':
                                    odd_2 = float(val)
                            except:
                                pass
                        
                        # Alt/Üst 2.5 oranları - sondan 2. ve son
                        if len(value_spans) >= 8:
                            try:
                                val = value_spans[-2].text.strip()
                                if val and val != '-':
                                    under_25 = float(val)
                            except:
                                pass
                            try:
                                val = value_spans[-1].text.strip()
                                if val and val != '-':
                                    over_25 = float(val)
                            except:
                                pass
                        
                        # Datetime oluştur
                        datetime_str = f"{date_str} {match_time}"
                        
                        match = {
                            'datetime': datetime_str,
                            'home_team': home_team,
                            'away_team': away_team,
                            'league': league_name,
                            'odd_1': odd_1,
                            'odd_x': odd_x,
                            'odd_2': odd_2,
                            'over_25': over_25,
                            'under_25': under_25,
                            'mackolik_match_id': mackolik_match_id  # 🆕 Eklendi
                        }
                        
                        all_matches.append(match)
                        
                    except Exception as e:
                        print(f"⚠️  Maç parse hatası: {str(e)}")
                        continue
            
            day_match_count = len([m for m in all_matches if date_str in m['datetime']])
            print(f"✅ {date_str}: {day_match_count} maç bulundu")
            
            # Telegram'a ilerleme bildir
            if status_callback:
                status_callback(f"day_{day}_{day_match_count}")
        
        print(f"\n✅ Toplam {len(all_matches)} maç çekildi")
        return True, all_matches, ""
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return False, [], f"API hatası: {str(e)}"


if __name__ == "__main__":
    # Test
    success, matches, error = fetch_mackolik_matches(days_ahead=2)
    
    if success:
        print(f"\n✅ Başarılı! {len(matches)} maç bulundu")
        print("\nİlk 3 maç:")
        for match in matches[:3]:
            print(f"  {match['datetime']} | {match['league']}")
            print(f"    {match['home_team']} vs {match['away_team']}")
            print(f"    1: {match['odd_1']}, X: {match['odd_x']}, 2: {match['odd_2']}")
    else:
        print(f"❌ Hata: {error}")

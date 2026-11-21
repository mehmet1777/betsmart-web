"""
Sahadan.com API - İddaa programı veri çekme
"""
import requests
from datetime import datetime, timedelta
import json

def fetch_sahadan_matches(days_ahead=2, status_callback=None):
    """
    Sahadan.com API'den maç verilerini çek
    
    Args:
        days_ahead: Kaç gün sonrasına kadar maçları çek
        status_callback: İlerleme bildirimi için callback
        
    Returns:
        (success: bool, matches: list, error: str)
    """
    try:
        all_matches = []
        
        # Bugünden itibaren belirtilen gün sayısı kadar çek
        for day in range(days_ahead):
            target_date = datetime.now() + timedelta(days=day)
            date_str = target_date.strftime("%Y-%m-%d")  # Sahadan formatı: 2026-11-21
            
            print(f"📅 [Sahadan] {date_str} tarihi çekiliyor...")
            
            if status_callback:
                status_callback(f"sahadan_fetching_{date_str}")
            
            # Sahadan API URL
            url = (
                f"https://www.sahadan.com/api/index/betting-service-bulletin-soccer"
                f"?a=bs"
                f"&e=bsbp"
                f"&u=soccer"
                f"&application=mackolik.com"
                f"&language=tr"
                f"&country=tr"
                f"&date={date_str}"
            )
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'application/json',
                'Referer': 'https://www.sahadan.com/'
            }
            
            # Retry mekanizması: 3 kez dene
            max_retries = 3
            response = None
            last_error = None
            
            for attempt in range(max_retries):
                try:
                    response = requests.get(url, headers=headers, timeout=30)
                    break
                except requests.exceptions.Timeout:
                    last_error = f"Timeout (deneme {attempt + 1}/{max_retries})"
                    print(f"⏳ {last_error}")
                    if attempt < max_retries - 1:
                        import time
                        time.sleep(2)
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
            
            # JSON parse
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse hatası: {e}")
                continue
            
            # Sahadan API response formatını parse et
            day_matches = parse_sahadan_response(data, date_str)
            
            print(f"✅ {date_str}: {len(day_matches)} maç bulundu")
            
            if status_callback:
                status_callback(f"sahadan_found_{date_str}_{len(day_matches)}")
            
            all_matches.extend(day_matches)
        
        print(f"🎯 Toplam {len(all_matches)} maç toplandı (Sahadan)")
        
        if len(all_matches) == 0:
            return (False, [], "Sahadan'da maç bulunamadı")
        
        return (True, all_matches, None)
        
    except Exception as e:
        error_msg = f"Sahadan API hatası: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return (False, [], error_msg)


def parse_sahadan_response(data, date_str):
    """
    Sahadan API response'unu parse et
    
    Format:
    {
      "data": {
        "soccer": [
          {
            "title": "Lig adı",
            "matches": [...]
          }
        ]
      }
    }
    """
    matches = []
    
    try:
        soccer_data = data.get('data', {}).get('soccer', [])
        
        for league_group in soccer_data:
            league_name = league_group.get('title', 'Unknown')
            league_matches = league_group.get('matches', [])
            
            for match in league_matches:
                parsed_match = parse_sahadan_match(match, date_str, league_name)
                if parsed_match:
                    matches.append(parsed_match)
        
        print(f"   ✅ {len(matches)} maç parse edildi")
        
    except Exception as e:
        print(f"⚠️ Parse hatası: {e}")
        import traceback
        traceback.print_exc()
    
    return matches


def parse_sahadan_match(item, date_str, league_name):
    """
    Tek bir Sahadan maç objesini parse et
    
    Args:
        date_str: ISO format (YYYY-MM-DD) - örn: "2026-11-21"
    """
    try:
        home_team = item.get('team_A', '')
        away_team = item.get('team_B', '')
        time = item.get('time', '00:00')
        
        # Maç Sonucu (MS) oranlarını bul
        # market i:1 = MS
        odd_1 = '-'
        odd_x = '-'
        odd_2 = '-'
        
        markets = item.get('markets', [])
        for market in markets:
            if market.get('i') == 1:  # MS (Maç Sonucu)
                options = market.get('o', [])
                if options:
                    outcomes = options[0].get('l', [])
                    for outcome in outcomes:
                        name = outcome.get('n', '')
                        value = outcome.get('v', '-')
                        
                        if name == '1':
                            odd_1 = value
                        elif name == 'X':
                            odd_x = value
                        elif name == '2':
                            odd_2 = value
                break
        
        # Temel validasyon
        if not home_team or not away_team:
            return None
        
        # Tarihi ISO -> Mackolik formatına çevir (2026-11-21 -> 21.11.2026)
        try:
            from datetime import datetime
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = dt.strftime("%d.%m.%Y")  # 21.11.2026
        except:
            formatted_date = date_str  # Hata olursa olduğu gibi kullan
        
        # BetSmart formatına dönüştür (Mackolik ile uyumlu)
        datetime_str = f"{formatted_date} {time}"  # "21.11.2026 04:00"
        
        match = {
            'datetime': datetime_str,  # Supabase için datetime key'i (Mackolik formatında)
            'date': formatted_date,
            'time': time,
            'league': league_name,
            'home_team': home_team,
            'away_team': away_team,
            'score': None,
            'half_score': None,
            'odd_1': convert_odd_to_float(odd_1),
            'odd_x': convert_odd_to_float(odd_x),
            'odd_2': convert_odd_to_float(odd_2),
            'over_25': None,
            'under_25': None,
            'gg_yes': None,
            'gg_no': None
        }
        
        return match
        
    except Exception as e:
        print(f"⚠️ Maç parse hatası: {e}")
        return None


def convert_odd_to_float(odd_str):
    """
    Oran string'ini float'a çevir
    '-' veya geçersiz ise None döndür
    """
    if odd_str == '-' or odd_str == '' or odd_str is None:
        return None
    
    try:
        return float(odd_str)
    except:
        return None

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
        # Hedef tarih aralığını hesapla (bugün + days_ahead gün)
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        target_dates = []
        for day in range(days_ahead):
            target_date = today + timedelta(days=day)
            target_dates.append(target_date)
        
        print(f"🎯 Hedef tarihler: {[d.strftime('%d.%m.%Y') for d in target_dates]}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Referer': 'https://www.sahadan.com/'
        }
        
        all_matches = []
        
        # Her tarih için ayrı API çağrısı yap
        for target_date in target_dates:
            date_iso = target_date.strftime('%Y-%m-%d')  # 2026-11-22 format
            date_display = target_date.strftime('%d.%m.%Y')
            
            print(f"📅 [Sahadan] {date_display} maçları çekiliyor...")
            
            if status_callback:
                status_callback(f"sahadan_fetching_{date_display}")
            
            # Sahadan API URL - date parametresi ile
            url = (
                f"https://www.sahadan.com/api/index/betting-service-bulletin-soccer"
                f"?a=bs"
                f"&e=bsbp"
                f"&u=soccer"
                f"&application=mackolik.com"
                f"&language=tr"
                f"&country=tr"
                f"&date={date_iso}"
            )
            
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
                print(f"❌ Sahadan {date_display} çekilemedi: {last_error}")
                continue
            
            if response.status_code != 200:
                print(f"❌ API hatası {date_display}: {response.status_code}")
                continue
            
            # JSON parse
            try:
                data = response.json()
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse hatası {date_display}: {e}")
                continue
            
            # Sahadan API response formatını parse et
            day_matches = parse_sahadan_response(data, date_display)
            
            print(f"   📦 {date_display}: {len(day_matches)} maç")
            all_matches.extend(day_matches)
        
        print(f"✅ Sahadan: Toplam {len(all_matches)} maç çekildi")
        
        if status_callback:
            status_callback(f"sahadan_found_{len(all_matches)}")
        
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
    
    Args:
        data: API response JSON
        date_str: Tarih (dd.mm.yyyy format) - API çağrısında kullanılan tarih
    
    Format:
    {
      "data": {
        "soccer": [
          {
            "title": "Lig adı",
            "time": "09:00",  // Lig seviyesinde saat
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
            league_time = league_group.get('time', '')  # ← LİG seviyesinde saat!
            league_matches = league_group.get('matches', [])
            
            for match in league_matches:
                # Lig saatini ve tarihi maça geçir
                parsed_match = parse_sahadan_match(match, league_name, league_time, date_str)
                if parsed_match:
                    matches.append(parsed_match)
        
        print(f"   ✅ {len(matches)} maç parse edildi")
        
    except Exception as e:
        print(f"⚠️ Parse hatası: {e}")
        import traceback
        traceback.print_exc()
    
    return matches


def parse_sahadan_match(item, league_name, league_time='', date_str=None):
    """
    Tek bir Sahadan maç objesini parse et
    
    Args:
        item: Sahadan match object
        league_name: Lig adı
        league_time: Lig seviyesindeki saat bilgisi (örn: "09:00")
        date_str: Maç tarihi (dd.mm.yyyy format) - API çağrısında kullanılan tarih
    """
    try:
        home_team = item.get('team_A', '')
        away_team = item.get('team_B', '')
        
        # Önce maç seviyesinde time var mı bak, yoksa lig time'ını kullan
        time = item.get('time', '') or league_time or ''
        
        # Saat bilgisi yoksa atla (geçersiz maç)
        if not time or time == '':
            return None
        
        # Maç durumu kontrolü - 's' field'ı bitmiş maçları gösterir
        match_status = item.get('s', '')
        
        # Eğer skor varsa (bitmiş maç), atla
        home_score = item.get('score_A')
        away_score = item.get('score_B')
        
        if home_score is not None and away_score is not None:
            # Maç bitmiş, atla
            return None
        
        # 's' field'ı da kontrol et (1 = bitmiş, 0 = oynanmamış gibi olabilir)
        if match_status and str(match_status) != '0' and str(match_status) != '':
            # Maç başlamış/bitmiş olabilir, atla
            return None
        
        # Tarihi belirle
        if date_str:
            # API çağrısında kullanılan tarih (dd.mm.yyyy)
            formatted_date = date_str
        else:
            # Sahadan'dan gelen tarih bilgisi (eğer varsa)
            date_from_api = item.get('date', '')
            
            if date_from_api:
                # Tarihi normalize et
                if '-' in date_from_api:
                    # ISO format: "2026-11-21" -> "21.11.2026"
                    try:
                        dt = datetime.strptime(date_from_api, "%Y-%m-%d")
                        formatted_date = dt.strftime("%d.%m.%Y")
                    except:
                        formatted_date = None
                elif '.' in date_from_api:
                    # Zaten doğru format: "21.11.2026"
                    formatted_date = date_from_api
                else:
                    formatted_date = None
            else:
                # Tarih yok, bugünün tarihini kullan
                today = datetime.now()
                formatted_date = today.strftime("%d.%m.%Y")
        
        # Maç Sonucu (MS) oranlarını bul
        # market i:1 = MS
        # BOOKMAKER 14 = NESİNE (düşük oranlar)
        # BOOKMAKER 15 = OLEY (yüksek oranlar)
        odd_1 = '-'
        odd_x = '-'
        odd_2 = '-'
        
        markets = item.get('markets', [])
        for market in markets:
            if market.get('i') == 1:  # MS (Maç Sonucu)
                options = market.get('o', [])
                
                # NESİNE oranlarını al (bookmaker_id = 14)
                nesine_option = None
                for option in options:
                    if option.get('b') == 14:
                        nesine_option = option
                        break
                
                # Eğer bookmaker 14 yoksa, fallback olarak options[0] kullan
                if nesine_option is None and options:
                    nesine_option = options[0]
                
                if nesine_option:
                    outcomes = nesine_option.get('l', [])
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
        if not home_team or not away_team or not formatted_date:
            return None
        
        # Oran kontrolü - eğer hiç oran yoksa, maç iptal/bitmiş olabilir
        if odd_1 == '-' and odd_x == '-' and odd_2 == '-':
            return None
        
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

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
        days_ahead: Kaç gün sonrasına kadar maçları çek (referans için)
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
        
        # Sahadan API - tarih parametresi OLMADAN (otomatik olarak güncel maçları getirir)
        print(f"📅 [Sahadan] Güncel maçlar çekiliyor (tarih filtresi yok)...")
        
        if status_callback:
            status_callback(f"sahadan_fetching_current")
        
        # Sahadan API URL - date parametresi YOK
        url = (
            f"https://www.sahadan.com/api/index/betting-service-bulletin-soccer"
            f"?a=bs"
            f"&e=bsbp"
            f"&u=soccer"
            f"&application=mackolik.com"
            f"&language=tr"
            f"&country=tr"
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
            print(f"❌ Sahadan çekilemedi: {last_error}")
            return (False, [], last_error)
        
        if response.status_code != 200:
            error_msg = f"API hatası: {response.status_code}"
            print(f"❌ {error_msg}")
            return (False, [], error_msg)
        
        # JSON parse
        try:
            data = response.json()
        except json.JSONDecodeError as e:
            error_msg = f"JSON parse hatası: {e}"
            print(f"❌ {error_msg}")
            return (False, [], error_msg)
        
        # Sahadan API response formatını parse et (date_str artık gerekli değil)
        all_matches = parse_sahadan_response(data, None)
        
        print(f"   📦 API'den {len(all_matches)} maç geldi")
        
        # Gelen maçları tarih filtresinden geçir - sadece hedef tarihlerdeki maçları al
        filtered_matches = []
        for match in all_matches:
            try:
                # Match datetime formatı: "21.11.2026 04:00"
                match_datetime_str = match.get('datetime', '')
                match_date_str = match_datetime_str.split(' ')[0]  # "21.11.2026"
                
                # Parse et
                day, month, year = match_date_str.split('.')
                match_date = datetime(int(year), int(month), int(day))
                
                # Hedef tarihler arasında mı kontrol et
                if any(match_date.date() == target.date() for target in target_dates):
                    filtered_matches.append(match)
                else:
                    # Debug için sadece ilk 3 atlamayı yazdır
                    if len([m for m in all_matches if m not in filtered_matches]) < 3:
                        print(f"   ⏭️  Atlandı (tarih dışı): {match['home_team']} vs {match['away_team']} - {match_date_str}")
            except Exception as e:
                print(f"   ⚠️  Tarih parse hatası: {e}")
                continue
        
        print(f"✅ Sahadan: {len(filtered_matches)} geçerli maç (toplam {len(all_matches)} maçtan)")
        
        if status_callback:
            status_callback(f"sahadan_found_{len(filtered_matches)}")
        
        if len(filtered_matches) == 0:
            return (False, [], "Sahadan'da hedef tarihlerde maç bulunamadı")
        
        return (True, filtered_matches, None)
        
    except Exception as e:
        error_msg = f"Sahadan API hatası: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return (False, [], error_msg)


def parse_sahadan_response(data, date_str=None):
    """
    Sahadan API response'unu parse et
    
    Args:
        data: API response JSON
        date_str: İsteğe bağlı tarih (eski uyumluluk için)
    
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
                parsed_match = parse_sahadan_match(match, league_name)
                if parsed_match:
                    matches.append(parsed_match)
        
        print(f"   ✅ {len(matches)} maç parse edildi")
        
    except Exception as e:
        print(f"⚠️ Parse hatası: {e}")
        import traceback
        traceback.print_exc()
    
    return matches


def parse_sahadan_match(item, league_name):
    """
    Tek bir Sahadan maç objesini parse et
    
    Args:
        item: Sahadan match object
        league_name: Lig adı
    """
    try:
        home_team = item.get('team_A', '')
        away_team = item.get('team_B', '')
        time = item.get('time', '00:00')
        
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
        
        # Sahadan'dan gelen tarih bilgisi (eğer varsa)
        # API'den date field gelebilir (örn: "2026-11-21" veya "21.11.2026")
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
            # Tarih yok, sadece saat var - bugünün tarihini kullan
            today = datetime.now()
            formatted_date = today.strftime("%d.%m.%Y")
        
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

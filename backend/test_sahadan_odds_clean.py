"""
Sahadan AP'nin hangi oranlar verdiini test et (Nesine mi Oley mi?)
"""
import requests
import json
from datetime import datetime

def test_sahadan_odds():
    """Sahadan AP'den bugnk malar ek ve oran detaylarn gster"""
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.sahadan.com/'
    }
    
    # Bugnn tarihi
    today = datetime.now().strftime('%Y-%m-%d')
    
    url = (
        f"https://www.sahadan.com/api/index/betting-service-bulletin-soccer"
        f"?a=bs"
        f"&e=bsbp"
        f"&u=soccer"
        f"&application=mackolik.com"
        f"&language=tr"
        f"&country=tr"
        f"&date={today}"
    )
    
    print(f"[SAHADAN AP TEST]")
    print(f"URL: {url}\n")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f" HTTP {response.status_code}")
            return
        
        data = response.json()
        
        # JSON yapsn incele
        print("=" * 80)
        print(" JSON YAPS:")
        print("=" * 80)
        
        soccer_data = data.get('data', {}).get('soccer', [])
        
        if not soccer_data:
            print(" Ma bulunamad")
            return
        
        print(f" {len(soccer_data)} lig grubu bulundu\n")
        
        # İlk ligi al
        first_league = soccer_data[0]
        league_name = first_league.get('title', 'Unknown')
        matches = first_league.get('matches', [])
        
        print(f" Lig: {league_name}")
        print(f" Ma says: {len(matches)}\n")
        
        if not matches:
            print(" Bu ligde ma yok")
            return
        
        # İlk ma detayl incele
        first_match = matches[0]
        
        print("=" * 80)
        print(" İLK MA DETAY:")
        print("=" * 80)
        
        home_team = first_match.get('team_A', '')
        away_team = first_match.get('team_B', '')
        time = first_match.get('time', '')
        
        print(f" Ev Sahibi: {home_team}")
        print(f"  Deplasman: {away_team}")
        print(f" Saat: {time}\n")
        
        # Markets incelemesi
        markets = first_match.get('markets', [])
        print(f" Toplam Market Says: {len(markets)}\n")
        
        # Her market'i incele
        for idx, market in enumerate(markets, 1):
            market_id = market.get('i')
            market_name = market.get('n', 'Unknown')
            
            print(f"Market #{idx}:")
            print(f"  D: {market_id}")
            print(f"  İsim: {market_name}")
            
            # Options (farkl bahis siteleri?)
            options = market.get('o', [])
            print(f"  Option Says: {len(options)}")
            
            if options:
                for opt_idx, option in enumerate(options):
                    # BTN FELD'LAR GSTER
                    print(f"\n    Option #{opt_idx + 1}:")
                    print(f"      RAW DATA: {json.dumps(option, indent=8, ensure_ascii=False)}")
                    
                    # Oranlar
                    outcomes = option.get('l', [])
                    if outcomes:
                        print(f"      Oranlar:")
                        for outcome in outcomes:
                            out_name = outcome.get('n', '')
                            out_value = outcome.get('v', '')
                            print(f"        {out_name}: {out_value}")
            
            print()
        
        # Sadece MS (Ma Sonucu) market'ini gster
        print("=" * 80)
        print(" MA SONUCU (MS) ORANLAR:")
        print("=" * 80)
        
        for market in markets:
            if market.get('i') == 1:  # MS market
                options = market.get('o', [])
                
                if options:
                    for option in options:
                        provider_name = option.get('n', 'Bilinmeyen')
                        
                        print(f"\n Salayc: {provider_name}")
                        
                        outcomes = option.get('l', [])
                        for outcome in outcomes:
                            bet_name = outcome.get('n', '')
                            bet_value = outcome.get('v', '')
                            print(f"  {bet_name}: {bet_value}")
                
                break
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f" Hata: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_sahadan_odds()


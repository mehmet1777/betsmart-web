"""
Football-Data.org - Günlük Maç Çekme
Her gün otomatik çalışacak script
"""

import requests
import json
from datetime import datetime, timedelta

# API Token
API_TOKEN = "b72db84e56364f16983d2959e0da95dc"
BASE_URL = "https://api.football-data.org/v4"

# Popüler ligler (Free tier'da mevcut)
LEAGUES = {
    "2021": "Premier League",
    "2014": "La Liga", 
    "2002": "Bundesliga",
    "2019": "Serie A",
    "2015": "Ligue 1",
    "2001": "UEFA Champions League",
    "2152": "Copa Libertadores",
    "2013": "Campeonato Brasileiro Série A"
}

def fetch_matches_for_date(date_str):
    """Belirli bir tarihteki tüm maçları çek"""
    
    headers = {"X-Auth-Token": API_TOKEN}
    all_matches = []
    
    print(f"\n{'='*70}")
    print(f"📅 {date_str} TARİHİNİN MAÇLARI ÇEKILIYOR...")
    print(f"{'='*70}\n")
    
    for league_id, league_name in LEAGUES.items():
        print(f"🔍 {league_name} kontrol ediliyor...")
        
        try:
            # Tarih aralığı (bugün + yarın)
            date_from = date_str
            date_to = (datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
            
            response = requests.get(
                f"{BASE_URL}/competitions/{league_id}/matches",
                headers=headers,
                params={
                    "dateFrom": date_from,
                    "dateTo": date_to
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                matches = data.get('matches', [])
                
                if matches:
                    print(f"   ✅ {len(matches)} maç bulundu")
                    
                    for match in matches:
                        # Maç bilgilerini parse et
                        match_data = {
                            'id': match.get('id'),
                            'league': league_name,
                            'date': match.get('utcDate'),
                            'home_team': match.get('homeTeam', {}).get('name'),
                            'away_team': match.get('awayTeam', {}).get('name'),
                            'status': match.get('status'),
                            'score': match.get('score', {}),
                        }
                        
                        all_matches.append(match_data)
                        
                        # Console'a yazdır
                        time = match_data['date'][:16] if match_data['date'] else 'Unknown'
                        print(f"      • {time} | {match_data['home_team']} vs {match_data['away_team']}")
                else:
                    print(f"   ℹ️ Maç yok")
            else:
                print(f"   ⚠️ API hatası: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Hata: {str(e)[:50]}")
            continue
    
    return all_matches

def save_matches_to_json(matches, filename="data/daily_matches.json"):
    """Maçları JSON dosyasına kaydet"""
    
    import os
    
    # data klasörünü oluştur
    os.makedirs("data", exist_ok=True)
    
    # JSON'a kaydet
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'updated_at': datetime.now().isoformat(),
            'match_count': len(matches),
            'matches': matches
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {len(matches)} maç kaydedildi: {filename}")

def fetch_matches_for_date_rapidapi(date_str):
    """RapidAPI - Free Football Data ile maç çek"""
    
    headers = {
        "X-RapidAPI-Key": "66169584d0msh7057db92927118cp13bd3ejsn55faa1294dce",
        "X-RapidAPI-Host": "free-api-live-football-data.p.rapidapi.com"
    }
    
    print(f"\n{'='*70}")
    print(f"📅 {date_str} TARİHİNİN MAÇLARI ÇEKILIYOR (RapidAPI)...")
    print(f"{'='*70}\n")
    
    try:
        response = requests.get(
            "https://free-api-live-football-data.p.rapidapi.com/football-get-matches-by-date",
            headers=headers,
            params={"date": date_str.replace("-", "")},  # YYYYMMDD formatı
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Response alındı!")
            print(f"📦 Response type: {type(data)}")
            
            # Response yapısını göster
            if isinstance(data, dict):
                status = data.get('status')
                message = data.get('message')
                
                print(f"   Status: {status}")
                if message:
                    print(f"   Message: {message}")
                
                # Tüm key'leri kontrol et
                print(f"   Keys: {list(data.keys())}")
                
                # Response içeriğini kontrol et
                response_content = data.get('response')
                print(f"   Response content type: {type(response_content)}")
                
                if isinstance(response_content, dict):
                    print(f"   Response dict keys: {list(response_content.keys())}")
                    
                    # Maçları farklı key'lerde ara
                    for possible_key in ['matches', 'events', 'fixtures', 'data', 'results']:
                        if possible_key in response_content:
                            matches = response_content[possible_key]
                            if isinstance(matches, list) and len(matches) > 0:
                                print(f"   ✅ Maçlar '{possible_key}' içinde bulundu: {len(matches)}")
                                
                                # İlk maçı göster
                                print(f"\n   📋 İLK MAÇ:")
                                print(f"   {json.dumps(matches[0], indent=4, ensure_ascii=False)[:500]}")
                                
                                return matches
                elif isinstance(response_content, list):
                    print(f"   ✅ Response direkt liste: {len(response_content)} item")
                    if len(response_content) > 0:
                        print(f"\n   📋 İLK ITEM:")
                        print(f"   {json.dumps(response_content[0], indent=4, ensure_ascii=False)[:500]}")
                    return response_content
                else:
                    print(f"   ⚠️ Response content: {str(response_content)[:200]}")
                
                # Hiçbir yerde maç bulunamadı
                print(f"\n   ⚠️ Maç listesi bulunamadı")
                print(f"   📄 FULL RESPONSE:")
                print(f"   {json.dumps(data, indent=2, ensure_ascii=False)[:500]}")
                return []
            else:
                print(f"⚠️ Beklenmeyen response formatı")
                return []
        else:
            print(f"❌ API Hatası: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return []
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        return []

def main():
    """Ana fonksiyon - İki API'yi de dene"""
    
    print("\n" + "="*70)
    print("⚽ GÜNLÜK MAÇ ÇEKME SERVİSİ (TÜRKİYE LİGİ DAHİL)")
    print("="*70)
    
    # Bugün
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n📅 Tarih: {today}")
    
    print("\n🔄 API 1: RapidAPI (Türkiye ligi olabilir)")
    print("-" * 70)
    matches_rapid = fetch_matches_for_date_rapidapi(today)
    
    # Türkiye maçları var mı filtrele
    turkey_matches = []
    if matches_rapid:
        for match in matches_rapid:
            league = str(match.get('league', match.get('competition', {}).get('name', ''))).lower()
            if 'türk' in league or ('super' in league and 'lig' in league) or 'turkey' in league:
                turkey_matches.append(match)
    
    # Özet
    print("\n" + "="*70)
    print(f"📊 ÖZET")
    print("="*70)
    print(f"✅ Toplam {len(matches_rapid)} maç bulundu")
    print(f"🇹🇷 Türkiye ligi maçları: {len(turkey_matches)}")
    
    if turkey_matches:
        print("\n🇹🇷 TÜRKİYE LİGİ MAÇLARI:")
        for i, match in enumerate(turkey_matches, 1):
            home = match.get('home', match.get('homeTeam', {}).get('name', 'Unknown'))
            away = match.get('away', match.get('awayTeam', {}).get('name', 'Unknown'))
            print(f"   {i}. {home} vs {away}")
    
    print("\n" + "="*70)
    print("✅ İşlem tamamlandı!")
    print("="*70)

if __name__ == "__main__":
    main()

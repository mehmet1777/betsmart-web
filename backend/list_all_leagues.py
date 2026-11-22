"""
Football-Data.org - Tüm Ligleri Listele
Hangi ligler mevcut görelim
"""

import requests

API_TOKEN = "b72db84e56364f16983d2959e0da95dc"
BASE_URL = "https://api.football-data.org/v4"

def list_all_leagues():
    """Tüm ligleri listele"""
    
    headers = {"X-Auth-Token": API_TOKEN}
    
    print("=" * 80)
    print("🌍 FOOTBALL-DATA.ORG - TÜM LİGLER")
    print("=" * 80)
    
    try:
        response = requests.get(
            f"{BASE_URL}/competitions",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            competitions = data.get('competitions', [])
            
            print(f"\n✅ {len(competitions)} lig bulundu!\n")
            
            # Ülkelere göre grupla
            by_country = {}
            
            for comp in competitions:
                country = comp.get('area', {}).get('name', 'Unknown')
                league_name = comp.get('name', 'Unknown')
                league_id = comp.get('id', 'Unknown')
                league_code = comp.get('code', 'N/A')
                
                if country not in by_country:
                    by_country[country] = []
                
                by_country[country].append({
                    'id': league_id,
                    'name': league_name,
                    'code': league_code
                })
            
            # Alfabetik sırala ve yazdır
            for country in sorted(by_country.keys()):
                print(f"\n🌍 {country.upper()}:")
                print("-" * 80)
                
                for league in by_country[country]:
                    print(f"   ID: {league['id']:<6} | Code: {league['code']:<6} | {league['name']}")
            
            # Türkiye var mı kontrol et
            print("\n" + "=" * 80)
            if 'Turkey' in by_country or 'Türkiye' in by_country:
                turkey_key = 'Turkey' if 'Turkey' in by_country else 'Türkiye'
                print(f"✅ TÜRKİYE LİGİ BULUNDU!")
                print("-" * 80)
                for league in by_country[turkey_key]:
                    print(f"   ID: {league['id']} | {league['name']}")
            else:
                print("❌ Türkiye ligi yok (ücretsiz tier'da olmayabilir)")
                print("\n💡 Free tier'da olan popüler ligler:")
                
                popular_countries = ['England', 'Spain', 'Germany', 'Italy', 'France', 'Europe', 'Brazil']
                for country in popular_countries:
                    if country in by_country:
                        print(f"\n🏆 {country}:")
                        for league in by_country[country]:
                            print(f"   • {league['name']} (ID: {league['id']})")
            
            print("\n" + "=" * 80)
            print("✅ Liste tamamlandı!")
            print("=" * 80)
            
            return competitions
        else:
            print(f"❌ API Hatası: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    list_all_leagues()

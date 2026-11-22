"""
mackolik_api.py'nin cektigi HTML'de match ID var mi?
"""

import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

print("="*80)
print("MACKOLIK API HTML - MATCH ID KONTROLU")
print("="*80)

# mackolik_api.py'deki aynı endpoint
date_str = datetime.now().strftime("%d.%m.%Y")

url = (
    f"https://www.mackolik.com/ajax/iddaa/events/soccer"
    f"?byKickOffTime=false"
    f"&competitionId="
    f"&selectedDate={date_str}"
    f"&eventUrlPrefixType=iddaaPage"
    f"&eventUrlSuffixType=iddaaPage"
)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://www.mackolik.com/iddaa'
}

print(f"\nTarih: {date_str}")
print(f"URL: {url[:100]}...")

try:
    response = requests.get(url, headers=headers, timeout=30)
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        if data.get('status') == 'success':
            html = data.get('data', {}).get('html', '')
            
            print(f"HTML size: {len(html)} chars")
            
            if html:
                # BeautifulSoup ile parse
                soup = BeautifulSoup(html, 'html.parser')
                
                # Tüm linkleri bul
                links = soup.find_all('a', href=True)
                print(f"\nToplam {len(links)} link bulundu")
                
                # Match ID pattern'lerini ara
                patterns = {
                    '/mac/MATCHID/': r'/mac/(\d+)/',
                    'Match/Default.aspx?id=': r'Match/Default\.aspx\?id=(\d+)',
                    'matchId': r'matchId["\s:=]+(\d+)',
                }
                
                found_any = False
                
                for pattern_name, pattern_regex in patterns.items():
                    matches = re.findall(pattern_regex, html)
                    
                    if matches:
                        unique = list(set(matches))
                        print(f"\nPattern '{pattern_name}':")
                        print(f"  {len(unique)} benzersiz ID bulundu")
                        print(f"  Ilk 5: {unique[:5]}")
                        found_any = True
                        
                        # İlk ID ile H2H test et
                        if unique:
                            test_id = unique[0]
                            h2h_url = f"https://arsiv.mackolik.com/Match/Head2Head.aspx?id={test_id}&s=1"
                            print(f"\n  H2H TEST:")
                            print(f"  URL: {h2h_url}")
                            
                            h2h_response = requests.get(h2h_url, timeout=10)
                            if h2h_response.status_code == 200:
                                if 'Aralarındaki' in h2h_response.text or len(h2h_response.text) > 5000:
                                    print(f"  BASARILI! H2H data var")
                                    
                                    # Takım isimlerini bul
                                    team_match = re.search(r'<title>([^<]+)</title>', h2h_response.text)
                                    if team_match:
                                        print(f"  Takimlar: {team_match.group(1)}")
                                else:
                                    print(f"  HATALI: H2H data yok (size: {len(h2h_response.text)})")
                            else:
                                print(f"  H2H failed: {h2h_response.status_code}")
                
                if not found_any:
                    print("\nHICBIR PATTERN MATCH ETMEDI!")
                    print("\nHTML'in ilk 500 karakteri:")
                    print(html[:500])
                    print("\n...")
                    print("\nIlk 5 link ornegi:")
                    for i, link in enumerate(links[:5], 1):
                        href = link.get('href', '')
                        text = link.get_text(strip=True)[:30]
                        print(f"  {i}. {href} ({text})")
                        
except Exception as e:
    print(f"\nERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*80)
print("SONUC:")
print("="*80)
print("""
EGER MATCH ID BULUNURSA:
   BASARILI! mackolik_api.py'de match ID parse edilebilir
   -> Supabase'e kaydet
   -> Fallback icin kullan

EGER MATCH ID BULUNMAZSA:
   • HTML yapisini incelememiz gerekir
   • Belki JavaScript ile yukleniyor
   • Alternatif endpoint aramaliyiz
""")

"""
Telegram bildirimi test scripti
"""
import os
from dotenv import load_dotenv
import requests

load_dotenv()

def test_telegram():
    """Telegram'a test mesajı gönder"""
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    print("=" * 70)
    print("TELEGRAM TEST")
    print("=" * 70)
    print()
    
    if not bot_token or bot_token == 'your_bot_token_here':
        print("HATA: TELEGRAM_BOT_TOKEN .env dosyasinda tanimli degil!")
        print("Lutfen .env dosyasina bot token'i ekleyin")
        return False
    
    if not chat_id or chat_id == 'your_chat_id_here':
        print("HATA: TELEGRAM_CHAT_ID .env dosyasinda tanimli degil!")
        print("Lutfen .env dosyasina chat ID'yi ekleyin")
        return False
    
    print(f"Bot Token: {bot_token[:20]}...")
    print(f"Chat ID: {chat_id}")
    print()
    
    # Test mesajı gönder
    message = """<b>BetSmart - Test Mesaji</b>

Telegram baglantisi basariyla kuruldu!

<b>Ornek Oran Degisikligi:</b>
Fenerbahce vs Galatasaray
MS1: 2.00 -> 2.20 (+10.0%)
MSX: 3.50 -> 3.40 (-2.9%)
MS2: 3.20 -> 3.30 (+3.1%)

Toplam degisim: 16.0%
"""
    
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        print("Telegram'a mesaj gonderiliyor...")
        response = requests.post(url, data=data, timeout=10)
        
        if response.status_code == 200:
            print("BASARILI! Telegram'a mesaj gonderildi")
            print("Telegram uygulamasini kontrol edin")
            return True
        else:
            print(f"HATA: HTTP {response.status_code}")
            print(f"Yanit: {response.text}")
            return False
            
    except Exception as e:
        print(f"HATA: {e}")
        return False

if __name__ == '__main__':
    test_telegram()

"""
Yeni Telegram mesaj formatını test et
"""
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

now = datetime.now().strftime('%d.%m.%Y %H:%M')

message = f"""═══════════════════════════════
  ORAN DEGISIKLIKLERI TESPIT EDILDI
═══════════════════════════════

>> 12 macta oran degisti

>> Tum detaylar ve analizler icin:
   https://betsmart-web.vercel.app/

>> Kontrol zamani: {now}

═══════════════════════════════"""

print("Test mesaji gonderiliyor...")
print(message)
print()

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {
    'chat_id': chat_id,
    'text': message
}

response = requests.post(url, data=data, timeout=10)

if response.status_code == 200:
    print("BASARILI! Telegram'i kontrol et")
else:
    print(f"HATA: {response.status_code}")
    print(response.text)

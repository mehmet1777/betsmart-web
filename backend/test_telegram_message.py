"""
Yeni birleştirilmiş Telegram mesaj formatını test et
"""
import os
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

now = datetime.now().strftime('%d.%m.%Y %H:%M')

# Test mesajı - her iki bölüm de dahil
message = f"""═══════════════════════════════
  📊 SISTEM GÜNCELLEMESİ
═══════════════════════════════

🔄 Oran Değişiklikleri: 2 maç

📊 Maç Detayları Durumu:
  • 650 maçtan 544 hazır (%84)
  • 86 yeni eklendi bu turda
  • 20 başarısız (tekrar denenecek)

🌐 https://betsmart-web-snowy.vercel.app/

🕐 {now}
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
    print("✅ BASARILI! Telegram'i kontrol et")
else:
    print(f"❌ HATA: {response.status_code}")
    print(response.text)

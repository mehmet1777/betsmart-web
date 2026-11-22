"""
Veritabanını sıfırlayıp Excel'i yeniden yükle
"""

import os
from database import Database

print("🗑️ VERİTABANI SIFIRLANIYOR...")
print("="*60)

# Eski veritabanını sil
if os.path.exists('betsmart.db'):
    os.remove('betsmart.db')
    print("✅ Eski veritabanı silindi")

# Yeni veritabanı oluştur
db = Database()
print("✅ Yeni veritabanı oluşturuldu")

print("\n" + "="*60)
print("✅ Hazır!")
print("\n📝 ŞİMDİ YAPIN:")
print("1. Programı başlatın: python app.py")
print("2. 'Dosya Yükle' butonuna tıklayın")
print("3. Excel dosyasını seçin")
print("4. Yüklenince Telegram'da test edin!")

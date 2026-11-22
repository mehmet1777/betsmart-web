# 🎯 BETSMART - AKILLI BAHİS ANALİZ BOTU

## 📸 YENİ ÖZELLİK: SCREENSHOT ANALİZİ!

Artık bahis sitesinden **screenshot** atmanız yeterli!  
Bot otomatik olarak oranları okur, geçmiş verilerle karşılaştırır ve **öneri verir**! 🚀

---

## ✨ ÖZELLİKLER:

### 1️⃣ **SCREENSHOT ANALİZİ** 📸 ⭐ YENİ
```
✅ Screenshot at
✅ Bot oranları otomatik okur (OCR)
✅ Geçmiş verilerle karşılaştırır
✅ Analiz ve öneri verir
```

### 2️⃣ **EXCEL YÖNET İMİ** 📊
```
✅ Excel bülteni yükle
✅ Otomatik veritabanına kaydet
✅ Telegram'a bildirim gönder
```

### 3️⃣ **TELEGRAM BOT** 🤖
```
✅ /start - Bot'u başlat
✅ /bulten - Maçları göster
✅ Screenshot at - Analiz al
```

### 4️⃣ **AKILLI ANALİZ** 🧠
```
✅ Geçmiş karşılaşmalar
✅ Oran değerlendirmesi
✅ İstatistiksel öneri
```

---

## 🚀 HIZLI BAŞLANGIÇ:

### **1. KURULUM:**

```bash
# Gerekli kütüphaneleri yükle
pip install -r requirements.txt

# Tesseract OCR kur (Windows)
# https://github.com/UB-Mannheim/tesseract/releases
# En son release'den exe dosyasını indirin ve kurun
# ⚠️ Kurulum sırasında Türkçe dil paketi seçin!
```

### **2. TELEGRAM AYARLARI:**

```bash
# Programı başlat
python app.py

# Menü > Ayarlar > Telegram Bağlantısı
# Bot Token: BotFather'dan alın
# Chat ID: @userinfobot'tan alın
# Kaydet ve Test Et
```

### **3. KULLANIM:**

#### **A) SCREENSHOT ANALİZİ** (Önerilen):
```
1. Bahis sitesinden maç screenshot'ı çek
2. Telegram bot'a at
3. 2 saniyede analiz ve öneri al!
```

#### **B) EXCEL YÖNETİMİ:**
```
1. Sahadan.com'dan Excel indir
2. Programa sürükle
3. Telegram'dan /bulten ile gör
```

---

## 📱 TELEGRAM KULLANIM ÖRNEĞİ:

### **SCREENSHOT ATINCA:**
```
Kullanıcı: 📸 [Nesine.com screenshot]

Bot:
⚽ Fenerbahçe vs Galatasaray

📱 OKUNAN ORANLAR:
MS1: 2.10  MSX: 3.40  MS2: 3.20

📊 GEÇMİŞ KARŞILAŞMALAR:
📅 15.03.2024 | Skor: 2-1
📅 10.12.2023 | Skor: 1-1

📈 İSTATİSTİK:
🏠 Ev Sahibi: 2 galibiyet (67%)
🤝 Beraberlik: 1 (33%)

💰 ORAN ANALİZİ:
MSX (3.40): İyi değer! ✅

🎯 TAVSİYE:
✅ MS1 (2.10) mantıklı - Ev sahibi geçmişte üstün
```

---

## 📸 İYİ SCREENSHOT NASIL OLMALI?

### ✅ **İYİ ÖRNEKİ:**
- Takım isimleri net görünüyor
- MS1, MSX, MS2 oranları var
- Büyük ve okunaklı
- Fazla karmaşık değil

### ❌ **KÖTÜ ÖRNEK:**
- Bulanık veya küçük
- Oranlar kesik
- Çok fazla reklam
- Takım isimleri yok

---

## 🛠️ SORUN GİDERME:

### ❌ "Tesseract not found":
```python
# ocr_analyzer.py dosyasında:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### ❌ "OCR oran okunamadı":
- Daha net screenshot çekin
- Oranlar ve takım isimleri tam görünsün
- MS1, MSX, MS2 yazıları olsun

### ❌ Telegram bot çalışmıyor:
- Token ve Chat ID'yi kontrol edin
- /start yazıp bot'u başlatın

---

## 📋 DOSYA YAPISI:

```
BetSmart/
├── app.py                 # Ana program
├── telegram_bot.py        # Telegram bot
├── ocr_analyzer.py        # OCR screenshot analizi ⭐ YENİ
├── database.py            # Veritabanı
├── scraper.py             # Web scraper
├── browser_window.py      # Selenium browser
├── requirements.txt       # Gerekli kütüphaneler
├── README.md              # Bu dosya
└── OCR_KULLANIM_KILAVUZU.md  # Detaylı OCR kılavuzu
```

---

## 🎯 KULLANIM SENARYOLARI:

### **SENARYO 1: MOBİL KULLANICI**
```
1. Telefonda Nesine'yi aç
2. Maçı bul, screenshot çek
3. Telegram'a at
4. Analiz ve öneri al
5. Bahsi oyna!
```

### **SENARYO 2: MASAÜSTÜ KULLANICI**
```
1. Excel bültenini yükle
2. Telegram'dan /bulten
3. Maça tıkla
4. Detaylı analiz gör
```

### **SENARYO 3: OTOMATİK**
```
1. Her gün Excel yükle
2. Bot bildirimi gönderir
3. Telegram'dan maçlara bak
```

---

## 💡 NEDEN OCR?

### **AVANTAJLAR:**
- ✅ Tüm bahis siteleri için çalışır
- ✅ API'ye gerek yok
- ✅ Çok hızlı (2-3 saniye)
- ✅ Kolay kullanım
- ✅ %90+ doğruluk

### **DİĞER ÇÖZÜMLERE KARŞI:**
- ❌ **API:** Çoğu site kapalı, değişiyor
- ❌ **Scraping:** JavaScript ile yükleniyor, zor
- ❌ **Manuel:** Oran yazma çok uzun sürer
- ✅ **OCR:** Sadece screenshot! 🎉

---

## 🔄 GÜNCELLEME GEÇMİŞİ:

### **v2.0 - OCR ÖZELLİĞİ** 📸
- ✅ Screenshot analizi eklendi
- ✅ Tesseract OCR entegrasyonu
- ✅ Akıllı oran okuma
- ✅ Geçmiş verilerle karşılaştırma
- ✅ Otomatik öneri sistemi

### **v1.0 - İLK SÜRÜM**
- ✅ Excel yükleme
- ✅ Telegram bot
- ✅ Veritabanı
- ✅ Basit analiz

---

## 📞 DESTEK:

**Sorun mu var?**
1. `OCR_KULLANIM_KILAVUZU.md` oku
2. Tesseract kurulumunu kontrol et
3. Error loglarına bak

**Özellik önerisi?**
- Yeni fikirler her zaman hoş gelir! 💡

---

## 🎉 BAŞARILAR!

Artık bahis analizi için:
- ❌ Site API'si araştırmaya gerek yok
- ❌ Elle oran yazmaya gerek yok  
- ❌ Karmaşık scraping yapmaya gerek yok

**Sadece screenshot at, analizi al! 📸🎯**

---

## 📄 LİSANS:

Bu proje kişisel kullanım içindir.

---

**🚀 Kolay gelsin ve bol kazançlar!**

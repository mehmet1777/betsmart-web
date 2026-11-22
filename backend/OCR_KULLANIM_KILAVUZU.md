# 📸 OCR SCREENSHOT ANALİZİ - KULLANIM KILAVUZU

## 🎯 YENİ ÖZELLİK: SCREENSHOT İLE ORAN ANALİZİ

Artık bahis sitesinden screenshot atmanız yeterli!
Bot otomatik olarak:
- ✅ Takım isimlerini okur
- ✅ Oranları tespit eder
- ✅ Geçmiş verilerle karşılaştırır
- ✅ Analiz ve öneri verir

---

## 📋 KURULUM ADIMLARI:

### **1. TESSERACT OCR YÜKLEME (Windows):**

**İndirin:**
```
https://github.com/UB-Mannheim/tesseract/releases
```

**Kurulum:**
1. En son release'den `tesseract-ocr-w64-setup-5.3.3.20231005.exe` indirin
2. Kurun (varsayılan: `C:\Program Files\Tesseract-OCR\`)
3. ⚠️ **ÖNEMLİ:** Türkçe dil paketi seçin (installation sırasında "Turkish" işaretleyin)

**Path Ayarı:**
`ocr_analyzer.py` dosyasını açın ve şu satırı düzenleyin:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 2️⃣ PYTHON PİHANELERİNİ YÜKLEYIN:

```bash
pip install pytesseract Pillow
```

Veya:
```bash
pip install -r requirements.txt
```

---

## 🚀 KULLANIM:

### **TELEGRAM'DAN KULLANIM:**

**Adım 1:** Bot'u başlatın
```bash
python app.py
```

**Adım 2:** Telegram'da `/start` yazın

**Adım 3:** Bahis sitesinden screenshot çekin
- Nesine.com
- Bilyoner.com  
- Misli.com
- veya herhangi bir bahis sitesi

**Screenshot'ta olması gerekenler:**
- ✅ Takım isimleri (örn: "Fenerbahçe - Galatasaray")
- ✅ MS1, MSX, MS2 oranları
- ✅ Net ve okunaklı

**Adım 4:** Screenshot'u Telegram'a atın

**Adım 5:** Bot otomatik analiz edecek! 🎉

---

## 📱 ÖRNEK KULLANIM:

### **SİZİN YAPMANZ GEREKEN:**
```
1. Nesine.com'u aç
2. Fenerbahçe - Galatasaray maçını bul
3. Oranları gösteren ekranı screenshot al
4. Telegram bot'a at
```

### **BOT'UN CEVABI:**
```
⚽ Fenerbahçe vs Galatasaray

📱 OKUNAN ORANLAR:
MS1 (Ev Sahibi): 2.10
MSX (Beraberlik): 3.40
MS2 (Deplasman): 3.20

🤖 OCR Güven Skoru: 100%

📊 GEÇMİŞ KARŞILAŞMALAR:
📅 15.03.2024 | Skor: 2-1
📅 10.12.2023 | Skor: 1-1
📅 05.09.2023 | Skor: 3-0

📈 İSTATİSTİK:
🏠 Ev Sahibi: 2 galibiyet (67%)
🤝 Beraberlik: 1 (33%)
✈️ Deplasman: 0 galibiyet (0%)

💰 ORAN ANALİZİ:
MS1 (2.10): Normal değer
MSX (3.40): İyi değer! ✅
MS2 (3.20): İyi değer! ✅

🎯 TAVSİYE:
✅ MS1 (2.10) mantıklı - Ev sahibi geçmişte üstün
```

---

## 🔧 SORUN GİDERME:

### ❌ "Tesseract not found" HATASI:
**Çözüm:**
```python
# ocr_analyzer.py dosyasında bu satırı ekleyin:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### ❌ "OCR ile oran okunamadı" HATASI:
**Çözüm:**
- Screenshot daha net olsun
- Oranlar ve takım isimleri tam görünsün
- Fazla küçük screenshot atmayın
- MS1, MSX, MS2 yazıları görünsün

### ❌ Türkçe karakterler okunamıyor:
**Çözüm:**
Tesseract kurulumunda Türkçe dil paketi seçildiğinden emin olun.

---

## 💡 İPUÇLARI:

### **İYİ SCREENSHOT:**
✅ Net ve okunaklı
✅ Takım isimleri tam görünüyor
✅ Oranlar büyük ve belirgin
✅ MS1, MSX, MS2 etiketleri var

### **KÖTÜ SCREENSHOT:**
❌ Bulanık veya küçük
❌ Oranlar kesik
❌ Takım isimleri eksik
❌ Fazla karmaşık (çok reklam, bilgi)

---

## 🎯 AVANTAJLAR:

### **Neden OCR Kullanmalıyım?**

1. **⚡ HIZLI:**
   - Screenshot at → 2 saniyede sonuç

2. **🌐 EVRENSEL:**
   - Tüm bahis siteleri için çalışır
   - API'ye gerek yok

3. **📊 AKILLI:**
   - Geçmiş verilerle karşılaştırır
   - Öneri verir

4. **💪 KOLAY:**
   - Oran yazmaya gerek yok
   - Sadece screenshot!

---

## 🚀 TEST:

### **Hemen Test Edin:**

1. Kurulumu tamamlayın
2. `python app.py` çalıştırın
3. Telegram'da `/start`
4. Test screenshot'ı atın

**Test için örnek screenshot oluşturun:**
- Herhangi bir bahis sitesini açın
- Bir maçın oranlarını gösterin
- Screenshot alın ve bot'a atın

---

## 📞 DESTEK:

**Sorun mu yaşıyorsunuz?**
- `test_ocr.py` ile test edin
- Error loglarını kontrol edin
- Tesseract kurulumunu doğrulayın

---

## 🎉 SONUÇ:

Artık bahis analizi için:
- ❌ API araştırmaya gerek yok
- ❌ Elle oran yazmaya gerek yok
- ❌ Site scraping yapmaya gerek yok

**Sadece screenshot at, analizi al! 📸🎯**

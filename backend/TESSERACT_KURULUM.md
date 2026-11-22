# 🔧 TESSERACT OCR KURULUM KILAVUZU

## 📥 İNDİRME LİNKLERİ:

### **WINDOWS İÇİN:**

**Seçenek 1: GitHub Releases (ÖNERİLEN):**
```
https://github.com/UB-Mannheim/tesseract/releases
```

**En son sürümü indirin:**
- `tesseract-ocr-w64-setup-5.3.3.20231005.exe` (64-bit)
- veya
- `tesseract-ocr-w32-setup-5.3.3.20231005.exe` (32-bit)

**Seçenek 2: Direkt İndirme:**
```
https://digi.bib.uni-mannheim.de/tesseract/
```

---

## 📦 KURULUM ADIMLARI:

### **1. EXE Dosyasını İndirin**
- Yukarıdaki linklerden `.exe` dosyasını indirin
- 64-bit Windows için `w64` versiyonunu seçin

### **2. Kurulumu Başlatın**
- İndirilen `.exe` dosyasını çalıştırın
- "Next" tıklayın

### **3. Dil Paketlerini Seçin** ⚠️ ÖNEMLİ
```
Additional language data (download) bölümünde:
✅ Turkish (tur) - MUTLAKA SEÇİN
✅ English (eng) - Varsayılan
```

### **4. Kurulum Yolunu Kontrol Edin**
```
Varsayılan: C:\Program Files\Tesseract-OCR
(Bu yolu değiştirmeyin, önerilen budur)
```

### **5. Kurulumu Tamamlayın**
- "Install" tıklayın
- Kurulum bitince "Finish"

---

## ⚙️ PYTHON AYARLARI:

### **1. Kütüphaneleri Yükleyin:**
```bash
pip install pytesseract Pillow
```

### **2. OCR Analyzer'ı Ayarlayın:**

`ocr_analyzer.py` dosyasını açın ve bu satırı bulun:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**Farklı bir yere kurduysanız:**
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\SIZIN\YOLUNUZ\tesseract.exe'
```

---

## ✅ TEST:

### **Python ile Test:**
```python
import pytesseract
from PIL import Image

# Tesseract path (kendi yolunuzu yazın)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Test
print(pytesseract.get_languages())
# Çıktı: ['eng', 'tur', ...] görmelisiniz
```

### **Komut Satırından Test:**
```bash
cd "C:\Program Files\Tesseract-OCR"
tesseract --version
# Sürüm bilgisi görmelisiniz

tesseract --list-langs
# eng, tur görmelisiniz
```

---

## 🐛 SORUN GİDERME:

### ❌ "tesseract is not recognized":
**Çözüm 1:** Path'i Python'da manuel ayarlayın
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**Çözüm 2:** Sistem PATH'ine ekleyin
```
1. Windows + R
2. sysdm.cpl yazın
3. Advanced > Environment Variables
4. System Variables > Path > Edit
5. New > C:\Program Files\Tesseract-OCR
6. OK > OK > OK
7. Bilgisayarı yeniden başlatın
```

### ❌ "tur.traineddata not found":
**Çözüm:** Türkçe dil paketini manuel indirin
```
https://github.com/tesseract-ocr/tessdata/blob/main/tur.traineddata

İndirin ve buraya kopyalayın:
C:\Program Files\Tesseract-OCR\tessdata\
```

### ❌ Python'dan çalışmıyor:
**Kontrol listesi:**
```
1. Tesseract kurulu mu?
   > tesseract --version

2. Path doğru mu?
   > print(pytesseract.pytesseract.tesseract_cmd)

3. Türkçe paketi var mı?
   > tesseract --list-langs
   > "tur" görünmeli

4. PIL/Pillow kurulu mu?
   > pip list | grep -i pillow
```

---

## 🔗 ALTERNATİF KURULUM YÖNTEMLERİ:

### **Seçenek 1: Chocolatey (Windows Paket Yöneticisi)**
```bash
choco install tesseract
```

### **Seçenek 2: Scoop**
```bash
scoop install tesseract
```

### **Seçenek 3: Manuel İndirme**
1. https://github.com/UB-Mannheim/tesseract/releases
2. En son release'i bul
3. Assets bölümünden `.exe` indir
4. Kur

---

## 📝 HANGİ LİNK ÇALIŞIR?

### **DOĞRU LİNKLER (2024):**

**1. GitHub Releases Sayfası:**
```
https://github.com/UB-Mannheim/tesseract/releases
```

**2. Direkt İndirme Sunucusu:**
```
https://digi.bib.uni-mannheim.de/tesseract/
```

**3. En Son Sürüm (Direkt):**
```
https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.3.20231005/tesseract-ocr-w64-setup-5.3.3.20231005.exe
```

---

## 🎯 KURULUM SONRASI:

### **1. Doğrulama:**
```bash
# Komut satırında:
tesseract --version
tesseract --list-langs
```

### **2. Python Test:**
```python
# test_ocr.py oluşturun
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Basit test
print("Tesseract version:", pytesseract.get_tesseract_version())
print("Languages:", pytesseract.get_languages())
```

### **3. BetSmart ile Test:**
```bash
python app.py
# Telegram'da screenshot at ve test et
```

---

## 💡 ÖNEMLİ İPUÇLARI:

1. **Türkçe Paketi Mutlaka Yükleyin**
   - Kurulum sırasında "Turkish (tur)" seçin
   - Yoksa manuel indirin

2. **Path'i Doğru Ayarlayın**
   - `ocr_analyzer.py` içinde path kontrolü yapın
   - Varsayılan: `C:\Program Files\Tesseract-OCR\tesseract.exe`

3. **Python Kütüphanelerini Güncel Tutun**
   ```bash
   pip install --upgrade pytesseract Pillow
   ```

4. **Test Edin**
   - Basit bir screenshot ile test yapın
   - Hata varsa log'lara bakın

---

## 📞 HALA SORUN VAR MI?

### **Adım Adım Kontrol:**

1. ✅ Tesseract kurulu mu?
   ```bash
   cd "C:\Program Files\Tesseract-OCR"
   tesseract --version
   ```

2. ✅ Python kütüphanesi kurulu mu?
   ```bash
   pip show pytesseract
   ```

3. ✅ Path doğru mu?
   ```python
   import pytesseract
   print(pytesseract.pytesseract.tesseract_cmd)
   ```

4. ✅ Türkçe paketi var mı?
   ```bash
   tesseract --list-langs
   ```

**Hepsi ✅ ise çalışmalı!**

---

## 🎉 BAŞARILI KURULUM SONRASI:

```
✅ Tesseract kurulu
✅ Türkçe paketi yüklü
✅ Python entegrasyonu tamam
✅ BetSmart hazır!

Artık screenshot analizi yapabilirsiniz! 📸
```

---

## 📚 EK KAYNAKLAR:

- **Tesseract Dökümantasyon:** https://tesseract-ocr.github.io/
- **GitHub Repo:** https://github.com/tesseract-ocr/tesseract
- **Dil Paketleri:** https://github.com/tesseract-ocr/tessdata

---

**🚀 Kolay gelsin!**

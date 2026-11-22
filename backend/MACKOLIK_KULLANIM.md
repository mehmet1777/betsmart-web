# 🔄 MACKOLIK PARSER KULLANIM KILAVUZU

## 📋 NE İŞE YARAR?

Mackolik.com'dan kopyaladığınız maç verilerini otomatik olarak düzenleyip Excel dosyası oluşturur.

---

## ⚠️ SORUN:

Mackolik'ten kopyala-yapıştır yaptığınızda:
- **Sol kısım** (Saat, Takımlar, Skorlar) → Bir grup
- **Oranlar** (1, X, 2) → Başka bir grup

Excel'de **yan yana gelmiyor**, iki ayrı sütun grubu oluşuyor!

---

## ✅ ÇÖZÜM: MACKOLIK PARSER

Bu araç iki kısmı birleştirip düzgün bir Excel oluşturur.

---

## 🚀 NASIL KULLANILIR?

### **ADIM 1: Mackolik'i Aç**
```
https://www.mackolik.com/
```

### **ADIM 2: Maçları Görüntüle**
- Bugünün maçlarını veya istediğiniz günü seçin
- Tüm ligleri görebilirsiniz

### **ADIM 3: Sol Kısmı Kopyala**
```
Fare ile seçin:
- Saat
- Durum (MS, 90, HT vs.)
- Takım isimleri
- Skorlar

Ctrl+C yapın
```

**Örnek:**
```
15:30  MS  Çaykur Rizespor  2 - 1  Erzurumspor
16:00  MS  Çorum FK  0 - 5  Fenerbahçe
18:30  90  Alanyaspor  0 - 2  Trabzonspor
```

### **ADIM 4: BetSmart'ta "Mackolik Parser" Butonu**
```
Ana ekranda pembe renkli buton:
🔄 Mackolik Parser
```

### **ADIM 5: Sol Kısmı Yapıştır**
```
İlk kutuya (Sol Kısım) Ctrl+V yapın
```

### **ADIM 6: Oranları Kopyala**
```
Mackolik'te oranlar kısmını seçin:
- 1 (Ev sahibi)
- X (Beraberlik)
- 2 (Deplasman)

Ctrl+C yapın
```

**Örnek:**
```
1.87  3.17  3.63
3.08  3.37  1.77
4.59  3.72  1.42
```

### **ADIM 7: Oranları Yapıştır**
```
İkinci kutuya (Oranlar) Ctrl+V yapın
```

### **ADIM 8: Birleştir!**
```
"🔄 Birleştir ve Excel Oluştur" butonuna basın
```

### **ADIM 9: Excel Hazır!**
```
Masaüstünde dosya oluşur:
mackolik_data_20240108_153042.xlsx
```

---

## 📊 OLUŞAN EXCEL FORMATI:

| time  | home_team        | score | away_team      | odd_1 | odd_x | odd_2 |
|-------|------------------|-------|----------------|-------|-------|-------|
| 15:30 | Çaykur Rizespor  | 2 - 1 | Erzurumspor    | 1.87  | 3.17  | 3.63  |
| 16:00 | Çorum FK         | 0 - 5 | Fenerbahçe     | 3.08  | 3.37  | 1.77  |
| 18:30 | Alanyaspor       | 0 - 2 | Trabzonspor    | 4.59  | 3.72  | 1.42  |

**Bu Excel'i artık veritabanına yükleyebilirsiniz!**

---

## 🎯 İPUÇLARI:

### ✅ DOĞRU KULLANIM:
```
1. Satır sayıları eşit olmalı
   - 10 maç → Sol 10 satır, Oran 10 satır
   
2. Satırlar sırayla olmalı
   - 1. maç sol, 1. maç oran
   - 2. maç sol, 2. maç oran
   
3. Temiz kopyala
   - Ekstra boşluklar sorun olmaz
   - Program otomatik temizler
```

### ❌ HATALAR:
```
1. Satır sayısı farklı
   → ⚠️ "Satır sayıları eşleşmiyor!" hatası
   → Çözüm: Tekrar kopyala, dikkatli ol
   
2. Boş alan
   → ⚠️ "Lütfen her iki alanı da doldurun!"
   → Çözüm: Her iki kutuyu da doldur
   
3. Hatalı format
   → ⚠️ "Hiç maç parse edilemedi!"
   → Çözüm: Mackolik'ten doğru alanı seç
```

---

## 🔄 TOPLU VERİ ÇEKME:

### **Farklı Günler İçin:**
```
1. Mackolik'te tarihi değiştir
2. Aynı işlemi tekrarla
3. Her gün için ayrı Excel oluşur
```

### **Farklı Ligler İçin:**
```
1. Her ligi ayrı ayrı kopyala
2. Hepsini aynı kutulara yapıştırabilirsin
3. Tek Excel'de birleşir
```

---

## 🎬 GÖRSELLİ ANLATIM:

### **Mackolik Ekranı:**
```
┌─────────────────────────────────────────┐
│  SAAT  DURUM  TAKIM1  SKOR  TAKIM2     │  ← Sol kısım (Kopyala)
├─────────────────────────────────────────┤
│  15:30   MS   Rizespor  2-1  Erzurum   │
│  16:00   MS   Çorum    0-5  Fenerbahçe │
└─────────────────────────────────────────┘

┌─────────────────────┐
│   1    X    2       │  ← Oranlar (Kopyala)
├─────────────────────┤
│  1.87  3.17  3.63  │
│  3.08  3.37  1.77  │
└─────────────────────┘
```

### **BetSmart Parser:**
```
┌────────────────────────────────────┐
│ 📊 Sol Kısım (Takımlar ve Skorlar)│
│ ┌────────────────────────────────┐ │
│ │ [Buraya sol kısmı yapıştır]   │ │
│ └────────────────────────────────┘ │
│                                    │
│ 🎲 Oranlar (1, X, 2)              │
│ ┌────────────────────────────────┐ │
│ │ [Buraya oranları yapıştır]    │ │
│ └────────────────────────────────┘ │
│                                    │
│  [🔄 Birleştir ve Excel Oluştur]  │
└────────────────────────────────────┘
```

---

## 📁 DOSYA KONUMU:

```
Masaüstü/
└── mackolik_data_20240108_153042.xlsx
                     ^^^^^^^^^^^^^^^^
                     Tarih ve Saat
```

**Otomatik isimlendirme:**
- `mackolik_data_` + tarih + saat
- Örnek: `mackolik_data_20240108_153042.xlsx`

---

## 🐛 SORUN GİDERME:

### **1. Buton Çalışmıyor**
```
Çözüm:
- Programı yeniden başlat
- python app.py
```

### **2. Excel Oluşmuyor**
```
Kontrol:
- Masaüstü yolu erişilebilir mi?
- openpyxl kütüphanesi yüklü mü?
  pip install openpyxl
```

### **3. Veriler Yanlış Eşleşiyor**
```
Neden:
- Satır sayıları farklı
- Kopyalama sırası karışmış

Çözüm:
- 🗑️ Temizle butonuna bas
- Tekrar dikkatli kopyala
```

### **4. Takım İsimleri Yanlış**
```
Neden:
- Mackolik formatı değişmiş olabilir

Çözüm:
- Excel'i aç, manuel düzelt
- Veya bana haber ver, parser'ı güncellerim
```

---

## 💡 GELECEK İYİLEŞTİRMELER:

### **v2.1 (Planlanıyor):**
- [ ] Otomatik lig tespiti
- [ ] Tarih ekleme
- [ ] Yarım skor desteği
- [ ] 2.5 Alt/Üst oranları

### **v2.2 (İstek Üzerine):**
- [ ] Direkt veritabanına kaydetme
- [ ] Çoklu Excel birleştirme
- [ ] Web scraper (otomatik çekme)

---

## 🎯 ÖZETİ ÖZET:

```
1. Mackolik'i aç
2. Sol kısmı kopyala → BetSmart'a yapıştır
3. Oranları kopyala → BetSmart'a yapıştır
4. "Birleştir" butonuna bas
5. Excel masaüstünde hazır!
```

**Sadece 5 adım! ⚡**

---

## 📞 DESTEK:

**Sorun mu var?**
- Bu dosyayı oku
- HIZLI_BASLANGIÇ.md'ye bak
- Hata mesajını kaydet
- Bana ilet

**Her şey yolunda mı?**
🎉 **Harika! Bol veri toplama! 📊**

---

**Kolay gelsin! 🚀**

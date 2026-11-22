# 📊 ORAN ANALİZİ ÖZELLİĞİ - KURULUM KILAVUZU

## ✨ YENİ ÖZELLİK: OTOMATİK ORAN ANALİZİ

Artık web sitesindeki **her maç kartında** sağ üstte **"📊 Analiz"** butonu var!

### **NASIL ÇALIŞIR?**

```
Kullanıcı "📊 Analiz" butonuna tıklar
         ↓
Modal açılır, oranlar API'ye gönderilir
         ↓
Python Backend (SQLite) benzer oranları arar
         ↓
İstatistikler hesaplanır:
  - Ev sahibi kazanma oranı
  - Beraberlik oranı
  - Deplasman kazanma oranı
  - Karşılıklı gol istatistiği
         ↓
Öneri ve güven seviyesi gösterilir
         ↓
Kullanıcıya sonuç sunulur (2-3 saniye)
```

---

## 🚀 HIZLI BAŞLANGIÇ

### **1. GEREKLİ KÜTÜPHANELER**

```bash
# Python Backend için
pip install flask flask-cors

# veya toplu kurulum:
pip install -r requirements.txt
```

### **2. SERVİSLERİ BAŞLAT**

#### **A) Otomatik (Önerilen):**
```bash
# Her iki servisi de başlat
START_ALL.bat
```

#### **B) Manuel:**
```bash
# Terminal 1: Python API
python api_server.py

# Terminal 2: Next.js Web
cd betsmart-web
npm run dev
```

### **3. TEST ET**

1. **Web sitesini aç:** http://localhost:3000
2. Herhangi bir maça git
3. Sağ üstteki **"📊 Analiz"** butonuna tıkla
4. Modal açılır ve analiz sonucu gösterilir!

---

## 🏗️ SİSTEM MİMARİSİ

```
┌─────────────────────────────────────┐
│  Frontend (Next.js - Port 3000)     │
│                                     │
│  • MatchCard Component              │
│  • "📊 Analiz" Butonu               │
│  • OddsAnalysisModal                │
└──────────────┬──────────────────────┘
               │ HTTP POST /api/analyze
               ↓
┌─────────────────────────────────────┐
│  Next.js API Route                  │
│  /app/api/analyze/route.ts          │
└──────────────┬──────────────────────┘
               │ HTTP POST /api/analyze-odds
               ↓
┌─────────────────────────────────────┐
│  Python Backend (Flask - Port 5000) │
│                                     │
│  • api_server.py                    │
│  • /api/analyze-odds endpoint       │
└──────────────┬──────────────────────┘
               │ SQL Query
               ↓
┌─────────────────────────────────────┐
│  SQLite Database (betsmart.db)      │
│                                     │
│  • 50,000+ maç verisi               │
│  • Oranlar, skorlar, tarihler       │
└─────────────────────────────────────┘
```

---

## 📂 DOSYA YAPISI

```
BetSmart/
├── api_server.py                    # 🔥 YENİ - Flask API Backend
├── database.py                      # SQLite işlemleri
├── betsmart.db                      # Veritabanı (50,000+ maç)
├── requirements.txt                 # Python dependencies (flask, flask-cors eklendi)
│
├── betsmart-web/
│   ├── app/
│   │   ├── api/
│   │   │   └── analyze/
│   │   │       └── route.ts         # 🔥 GÜNCELLENDİ - API endpoint
│   │   └── page.tsx                 # Ana sayfa
│   │
│   ├── components/
│   │   ├── MatchCard.tsx            # 🔥 GÜNCELLENDİ - Analiz butonu eklendi
│   │   └── OddsAnalysisModal.tsx    # 🔥 YENİ - Analiz modal'ı
│   │
│   └── .env.local                   # 🔥 GÜNCELLENDİ - PYTHON_API_URL eklendi
│
├── START_ALL.bat                    # 🔥 YENİ - Tüm servisleri başlat
├── start_api.bat                    # 🔥 YENİ - Sadece API başlat
└── start_web.bat                    # 🔥 YENİ - Sadece Web başlat
```

---

## 🎯 API ENDPOINT DETAYLARI

### **POST /api/analyze-odds**

#### **Request:**
```json
{
  "odd_1": 2.65,
  "odd_x": 2.80,
  "odd_2": 2.00,
  "home_team": "Ukebo",       // Optional
  "away_team": "Sabadell"     // Optional
}
```

#### **Response:**
```json
{
  "success": true,
  "total_count": 50,
  "exact": [
    {
      "date": "12.11.2026",
      "time": "21:00",
      "home_team": "Barcelona",
      "away_team": "Real Madrid",
      "score": "2-1",
      "odd_1": 2.65,
      "odd_x": 2.80,
      "odd_2": 2.00,
      "similarity": 100.0
    }
  ],
  "similar": [...],
  "statistics": {
    "home_wins": 15,
    "draws": 10,
    "away_wins": 25,
    "gg_yes": 30,
    "gg_no": 20,
    "total_valid": 50
  },
  "recommendation": {
    "type": "MS2",
    "odds": 2.00,
    "confidence": "Yüksek",
    "reason": "Benzer oranlı 50 maçta deplasman 25 kez kazandı (%50)",
    "percentage": 50.0
  }
}
```

---

## 🔍 ORAN EŞLEŞTIRME ALGORITMASI

### **İKİ SEVİYELİ TOLERANS SİSTEMİ**

1. **Exact Match (±0.01):**
   - %100 oran benzerliği
   - Örnek: `2.65/2.80/2.00` → `2.64/2.81/2.01` ✅

2. **Similar Match (±0.02):**
   - %98+ oran benzerliği
   - Örnek: `2.65/2.80/2.00` → `2.63/2.82/2.02` ✅

### **SQL Sorgusu:**
```sql
SELECT * FROM matches 
WHERE is_played = 1
  AND odd_1 BETWEEN (input_odd_1 - 0.01) AND (input_odd_1 + 0.01)
  AND odd_x BETWEEN (input_odd_x - 0.01) AND (input_odd_x + 0.01)
  AND odd_2 BETWEEN (input_odd_2 - 0.01) AND (input_odd_2 + 0.01)
ORDER BY ABS(odd_1 - input_odd_1) + ABS(odd_x - input_odd_x) + ABS(odd_2 - input_odd_2) ASC
LIMIT 100
```

---

## 🧪 TEST SENARYOLARI

### **1. Başarılı Analiz:**
```bash
# Örnek: Popüler oran (2.65 / 2.80 / 2.00)
# Beklenen: 50+ benzer maç bulunur
# Sonuç: İstatistik + Öneri gösterilir
```

### **2. Nadir Oran:**
```bash
# Örnek: Çok yüksek oran (9.50 / 5.20 / 1.15)
# Beklenen: 0-5 benzer maç bulunur
# Sonuç: "Benzer maç bulunamadı" mesajı
```

### **3. Backend Yok:**
```bash
# Python API kapalıysa
# Fallback: Mock data döner
# Mesaj: "Veritabanı bağlantısı yok"
```

---

## 🐛 SORUN GİDERME

### **❌ "Veritabanı bağlantısı yok" hatası:**

**Çözüm:**
```bash
# Python API'yi başlat
python api_server.py
```

### **❌ Modal açılmıyor:**

**Çözüm:**
```bash
# Next.js'i yeniden başlat
cd betsmart-web
npm run dev
```

### **❌ CORS hatası:**

**Çözüm:**
```bash
# flask-cors kurulu mu kontrol et
pip install flask-cors
```

### **❌ Port 5000 kullanımda:**

**Çözüm:**
```bash
# api_server.py'de portu değiştir:
app.run(host='0.0.0.0', port=5001, debug=True)

# .env.local'i güncelle:
PYTHON_API_URL=http://localhost:5001
```

---

## 📊 VERİTABANI DURUMU

Mevcut veritabanı kontrolü:

```bash
# Toplam maç sayısı
python -c "import sqlite3; conn = sqlite3.connect('betsmart.db'); print(f'Toplam maç: {conn.execute(\"SELECT COUNT(*) FROM matches\").fetchone()[0]:,}'); conn.close()"
```

---

## 🎨 FRONTEND ÖZELLEŞTİRME

### **Buton Rengini Değiştir:**

`betsmart-web/components/MatchCard.tsx`:
```tsx
<button className="bg-blue-500/10 hover:bg-blue-500/20 text-blue-500 ...">
  📊 Analiz
</button>
```

### **Modal Boyutunu Ayarla:**

`betsmart-web/components/OddsAnalysisModal.tsx`:
```tsx
<div className="relative w-full sm:max-w-3xl ...">  {/* max-w-2xl → max-w-3xl */}
```

---

## 🚀 PRODUCTION DEPLOYMENT

### **1. Python Backend (Railway/Heroku):**
```bash
# Procfile
web: python api_server.py
```

### **2. Next.js (Vercel):**
```bash
# Environment Variables
PYTHON_API_URL=https://your-api.railway.app
```

---

## 📈 GELECEKTEKİ GELİŞTİRMELER

- [ ] Makine öğrenmesi ile tahmin iyileştirme
- [ ] Daha fazla istatistik (ilk yarı, ikinci yarı, alt/üst)
- [ ] Grafik görselleştirme (chart.js)
- [ ] Favori analiz kaydetme
- [ ] PDF rapor indirme
- [ ] Canlı oran değişimi takibi

---

## 🎉 BAŞARILAR!

Artık web sitenizde **otomatik oran analizi** var!

**50+ maç varsa → Hepsine analiz butonu eklendi! 🚀**

---

## 📞 DESTEK

Sorun mu var?
1. Bu dosyayı oku
2. Error loglarını kontrol et
3. GitHub Issues açabilirsin

**Kolay gelsin ve bol kazançlar! 💰**

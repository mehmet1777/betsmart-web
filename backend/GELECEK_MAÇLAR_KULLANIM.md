# ⚽ Gelecek Maçlar Özelliği - Hızlı Kullanım Kılavuzu

## 🎯 Ne İşe Yarar?
Mackolik'ten **gelecek maçları** ve **oranlarını** kopyalayıp, tek tıkla SQLite veritabanına kaydedersin. Böylece:
- API kotası harcamazsın
- Mackolik'teki güncel oranları kullanırsın
- Geçmiş maçlar gibi, gelecek maçların da kaydını tutarsın

## 📋 Adım Adım Kullanım

### 1. Mackolik'ten Veri Al
1. **Mackolik.com** → Gelecek Maçlar sayfasına git
2. Tüm sayfayı seç: `Ctrl + A`
3. Kopyala: `Ctrl + C`

### 2. Desktop Uygulamada Parse Et
1. **BetSmart** uygulamasını aç
2. **"🔄 Mackolik Parser"** butonuna tıkla
3. Kopyalanan veriyi büyük text box'a yapıştır (`Ctrl + V`)
4. **"⚽ Gelecek Maçları Çek ve Kaydet"** (mavi buton) tıkla
5. Bekle... (birkaç saniye)
6. ✅ Başarı mesajı: "X gelecek maç veritabanına kaydedildi!"

### 3. Verileri Görüntüle
Terminal'den:
```bash
python view_future_matches.py
```

## 🔍 Takım Arama
Belirli bir takımın gelecek maçlarını görmek için:
```bash
python view_future_matches.py search "Galatasaray"
python view_future_matches.py search "Barcelona"
```

## 🗑️ Tüm Verileri Sil (Test için)
```bash
python view_future_matches.py delete
```

## 💾 Veritabanı Şeması
```sql
CREATE TABLE future_matches (
    id INTEGER PRIMARY KEY,
    datetime TEXT,           -- "Bugün 20:00", "Yarın 18:30", "15/11 19:00"
    home_team TEXT,          -- Ev sahibi takım
    away_team TEXT,          -- Deplasman takım
    league TEXT,             -- Lig adı
    odd_1 REAL,              -- Ev sahibi kazanır oranı
    odd_x REAL,              -- Beraberlik oranı
    odd_2 REAL,              -- Deplasman kazanır oranı
    over_25 REAL,            -- 2.5 üst oranı
    under_25 REAL,           -- 2.5 alt oranı
    created_at TIMESTAMP,    -- Kaydedilme zamanı
    UNIQUE(datetime, home_team, away_team)
)
```

## 🆚 Farklar: Geçmiş vs Gelecek

| Özellik | Geçmiş Maçlar (Excel) | Gelecek Maçlar (DB) |
|---------|----------------------|---------------------|
| **Format** | Skor bazlı (1-0, 2-1) | Tarih/saat bazlı |
| **Skor** | ✅ Var | ❌ Yok |
| **İlk Yarı** | ✅ Var | ❌ Yok |
| **Tarih** | Genelde yok | ✅ Bugün/Yarın/01/12 |
| **Kayıt** | Excel dosyası | SQLite DB |
| **Tablo** | `matches` (is_played=1) | `future_matches` |
| **Oranlar** | 1, X, 2, 2.5A/Ü | 1, X, 2, 2.5A/Ü |

## 🧪 Test Verisi Ekleme
```bash
python test_future_matches.py
```
Bu script 2 örnek maç ekler, sonra görüntüler.

## 📊 Python'dan Sorgu Örneği
```python
import sqlite3

conn = sqlite3.connect('betsmart.db')
cursor = conn.cursor()

# Tüm gelecek maçlar
cursor.execute('SELECT * FROM future_matches ORDER BY datetime')
for row in cursor.fetchall():
    print(f"{row[1]}: {row[2]} vs {row[3]}")

# Belirli takım
cursor.execute('SELECT * FROM future_matches WHERE home_team LIKE "%Galatasaray%"')
for row in cursor.fetchall():
    print(f"{row[2]} vs {row[3]} - Oranlar: {row[5]}/{row[6]}/{row[7]}")

conn.close()
```

## ⚠️ Dikkat Edilmesi Gerekenler

### 1. Format Hatası
**Hata**: "Oran başlıkları bulunamadı!"
**Sebep**: Mackolik'ten kopyalama eksik
**Çözüm**: Sayfanın tamamını seç (Ctrl+A) ve tekrar kopyala

### 2. Eksik Oranlar
**Durum**: Bazı maçların oranları `1.01` görünüyor
**Sebep**: O maçlar için Mackolik'te oran yok veya parse sırasında eşleşmedi
**Normal mi?**: Evet, sorun değil

### 3. Duplikasyon
**Durum**: Aynı maçı iki kez kaydettim
**Ne olur?**: Veritabanı güncellenir (REPLACE). Tekrar olmaz.
**Unique Key**: `datetime + home_team + away_team`

### 4. Tarih Formatı
Mackolik'ten gelen formatlar:
- `Bugün 20:00`
- `Yarın 18:30`
- `15/11 19:00` (gün/ay formatı)

## 🚀 Gelecek Planlar

1. **Web Entegrasyonu**: Next.js uygulamasına future_matches tablosunu göster
2. **Otomatik Güncelleme**: Günde 1 kez otomatik parse
3. **Bildirim**: Favori takımın maçı yaklaşınca bildirim
4. **Oran Karşılaştırma**: API oranları vs Mackolik oranları
5. **Sonuç Karşılaştırma**: Maç bittikten sonra tahmin doğru mu?

## 📞 Destek
Sorun yaşarsan:
1. `error_log.txt` dosyasını kontrol et
2. Terminal'deki hata mesajlarını oku
3. Discord/Telegram'dan yaz

---

**Güncelleme**: 9 Kasım 2026  
**Durum**: ✅ Hazır ve test edildi  
**Test Script**: `test_future_matches.py`  
**View Script**: `view_future_matches.py`

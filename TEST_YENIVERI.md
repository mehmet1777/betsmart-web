# /yeniveri + Oran Takibi Test Planı

## Yapılan Değişiklik
✅ `/yeniveri` komutu başarıyla bittiğinde otomatik olarak `check_odds_changes()` fonksiyonunu çağırıyor

## Test Adımları

### 1. Backend'i Yeniden Başlat
```bash
cd C:\Users\worda\Desktop\BetSmart\backend
python telegram_bot.py
```

### 2. Telegram'dan Test Et
```
/yeniveri
```

### 3. Beklenen Davranış

**İşlem Akışı:**
1. ✅ Sahadan'dan yeni maçlar çekilir
2. ✅ `future_matches` tablosuna kaydedilir
3. 🔄 `check_odds_changes()` otomatik çalışır:
   - Yeni maçları kontrol eder
   - İlk oranları `odds_changes` tablosuna ekler
   - `first_odd_1/x/2` = `current_odd_1/x/2` (ilk kayıtta aynı)
4. ✅ Telegram'a "Oran takibi tamamlandı" mesajı gelir

**Telegram Mesajı:**
```
✅ İşlem Tamamlandı!

📊 150 maç kaydedildi
☁️ Supabase'e yüklendi
🌐 Web sitesinde görünür
✅ Oran takibi tamamlandı

📅 Tarih Dağılımı:
   • Bugün: 75 maç
   • Yarın: 75 maç
   • Diğer: 0 maç

🔗 Web Sitesi
```

### 4. Supabase Kontrol

**`odds_changes` tablosu:**
```sql
SELECT 
    home_team, 
    away_team, 
    first_odd_1, 
    current_odd_1,
    first_detected_at
FROM odds_changes
ORDER BY first_detected_at DESC
LIMIT 10;
```

**Beklenen:** Yeni maçların ilk oranları kaydedilmiş olmalı

### 5. Sonraki Kontrol (10 dakika sonra)

`odds_tracker.py` schedule ile otomatik çalıştığında:
- Oranlar değişmişse `current_odd_*` güncellenir
- `first_odd_*` sabit kalır
- Telegram bildirimi gönderilir

## Mantık Özeti

### Daha Önce (Hatalı)
```
/yeniveri → Maçlar kaydedildi → future_matches güncellendi
                                   ❌ odds_changes boş kaldı
```

### Şimdi (Doğru)
```
/yeniveri → Maçlar kaydedildi → future_matches güncellendi
                              → ✅ check_odds_changes() çalıştı
                              → ✅ İlk oranlar odds_changes'e kaydedildi
```

## Olası Hatalar

### Hata 1: "Module not found: odds_tracker"
**Çözüm:** `telegram_bot.py` ve `odds_tracker.py` aynı dizinde olmalı

### Hata 2: "Oran takibi hatası: ..."
**Çözüm:** Hata mesajını kontrol et, Supabase bağlantısı veya .env eksik olabilir

### Hata 3: Telegram mesajı gelmiyor
**Çözüm:** 
- .env dosyasında TELEGRAM_BOT_TOKEN ve CHAT_ID olmalı
- Backend'de `load_dotenv()` çağrılmalı

## Sonuç

✅ Artık `/yeniveri` ile yeni maçlar çekildiğinde:
   - Maçlar `future_matches`'e kaydediliyor
   - İlk oranlar `odds_changes`'e kaydediliyor
   - Sonraki 10 dakikalık kontrollerde değişiklikler takip ediliyor

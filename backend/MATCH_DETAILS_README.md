# Match Details Özelliği - Kullanım Kılavuzu

## ✅ TAMAMLANAN İŞLER

### 1. Backend Kodları Hazır
- ✅ `match_details_api.py` - API çağrısı ve parsing
- ✅ `match_details_sync.py` - Supabase'e kaydetme
- ✅ `fetch_all_match_details.py` - Toplu çekme
- ✅ `sahadan_api.py` - UUID eklendi
- ✅ `supabase_sync.py` - UUID kaydetme eklendi

### 2. SQL Scriptleri Hazır
- ✅ `create_match_details_table.sql` - match_details tablosu
- ✅ `add_uuid_column.sql` - future_matches'e UUID kolonu

### 3. Test Edildi
- ✅ API çalışıyor
- ✅ Parsing çalışıyor
- ✅ Supabase'e kayıt çalışıyor

---

## 📋 YAPILACAKLAR

### Adım 1: Supabase'de SQL'leri Çalıştır

**1a) `add_uuid_column.sql` çalıştır:**
```sql
ALTER TABLE future_matches 
ADD COLUMN IF NOT EXISTS match_uuid TEXT;

CREATE INDEX IF NOT EXISTS idx_future_matches_uuid ON future_matches(match_uuid);

COMMENT ON COLUMN future_matches.match_uuid IS 'Sahadan API match UUID - match details için kullanılır';
```

**1b) `create_match_details_table.sql` zaten çalıştırıldı** ✅

### Adım 2: Manuel Test

```bash
cd C:\Users\worda\Desktop\BetSmart\backend

# Önce /yeniveri çalıştır (Telegram'dan)
# Sonra:
python fetch_all_match_details.py
```

Bu komut:
- future_matches'ten UUID'leri çeker
- Her maç için match details API çağırır
- Supabase'e kaydeder

### Adım 3: Telegram Bot'a Entegre Et (OPSİYONEL)

`telegram_bot.py` dosyasında `handle_yeniveri_callback` fonksiyonuna ekle:

**Nereye:** İlk oranlar kaydedildikten SONRA (satır ~365 civarı)

**Ne eklenecek:**
```python
# Match details çek (arka planda)
await status_msg.edit_text(
    f"✅ <b>Maçlar Kaydedildi!</b>\n\n"
    f"📊 {success_count} maç\n"
    f"☁️ Supabase'e yüklendi\n\n"
    f"🔄 Takım karşılaştırmaları çekiliyor...",
    parse_mode='HTML'
)

# Match details çek
try:
    from fetch_all_match_details import fetch_all_match_details_for_future_matches
    details_success, details_error, details_skip = await loop.run_in_executor(
        None, 
        fetch_all_match_details_for_future_matches
    )
    
    details_msg = f"📊 Detaylar: {details_success} başarılı, {details_error} hata"
except Exception as e:
    details_msg = f"⚠️ Detaylar çekilemedi"

# Final mesaj
await status_msg.edit_text(
    f"✅ <b>İşlem Tamamlandı!</b>\n\n"
    f"📊 {success_count} maç kaydedildi\n"
    f"{details_msg}\n\n"
    f"🔗 <a href='https://betsmart-web.vercel.app'>Web Sitesi</a>",
    parse_mode='HTML',
    disable_web_page_preview=True
)
```

---

## 🎯 KULLANIM

### Manuel Çekme
```bash
python fetch_all_match_details.py
```

### Telegram'dan Otomatik
```
/yeniveri
```
↓
Maçlar çekilir
↓
UUID'ler kaydedilir
↓
Match details otomatik çekilir (entegre edildiyse)

---

## 📊 VERİ YAPISI

### match_details Tablosu:
```json
{
  "match_uuid": "7tto7hbwd8o4wifwovvhbk1zo",
  "home_team": "Monza",
  "away_team": "Fiorentina",
  "h2h_data": {
    "total_matches": 7,
    "home_wins": 2,
    "draws": 2,
    "away_wins": 3,
    "avg_goals": 3.14,
    "matches": [...]
  },
  "form_home": {
    "serie": "LLLLW",
    "goals_for": 8,
    "goals_against": 10,
    "over_25": 4,
    "btts": 3,
    "matches": [...]
  },
  "form_away": {...}
}
```

---

## 🌐 WEB SİTESİNDE KULLANIM

### API Endpoint (Next.js):
```typescript
// app/api/match-details/route.ts
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const matchUuid = searchParams.get('uuid');
  
  const { data } = await supabase
    .from('match_details')
    .select('*')
    .eq('match_uuid', matchUuid)
    .single();
  
  return Response.json(data);
}
```

### Frontend:
```typescript
// Match kartında "📊 Detaylı Analiz" butonu
// Tıklayınca:
const details = await fetch(`/api/match-details?uuid=${match.uuid}`);
// Modal/drawer aç ve göster
```

---

## ⚠️ ÖNEMLİ NOTLAR

1. **UUID sadece Sahadan API'den gelir**
   - Mackolik fallback kullanılırsa UUID olmaz
   - Bu maçlar için match details çekilemez

2. **Rate Limiting**
   - Paralel 3 thread kullanılıyor
   - 100 maç için ~30-40 saniye sürer

3. **Hata Yönetimi**
   - API hatası alınırsa o maç atlanır
   - Diğer maçlar etkilenmez

4. **Cache**
   - Zaten çekilmiş maçlar tekrar çekilmez
   - `force_update=True` ile zorlayabilirsin

---

## 🚀 SONRAKİ ADIMLAR

1. ✅ Backend hazır
2. ⏳ SQL'leri çalıştır (add_uuid_column.sql)
3. ⏳ Manuel test et
4. ⏳ Telegram'a entegre et (opsiyonel)
5. ⏳ Web sitesinde göster (frontend)

---

## 📞 YARDIM

Hata alırsan:
1. Supabase'de tablolar var mı kontrol et
2. UUID'ler kaydediliyor mu kontrol et: `SELECT match_uuid FROM future_matches LIMIT 5;`
3. Log'lara bak: `python fetch_all_match_details.py`

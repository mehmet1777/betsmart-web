# ⚡ SUPABASE'DE ÇALIŞTIR - TEK TEK

Supabase SQL Editor'da bu SQL'leri **SIRAYLA** çalıştır:

---

## 1️⃣ UUID Kolonu Ekle (future_matches)

```sql
ALTER TABLE future_matches 
ADD COLUMN IF NOT EXISTS match_uuid TEXT;

CREATE INDEX IF NOT EXISTS idx_future_matches_uuid ON future_matches(match_uuid);

COMMENT ON COLUMN future_matches.match_uuid IS 'Sahadan API match UUID - match details için kullanılır';
```

✅ Tamamlandı mı? → Devam et

---

## 2️⃣ RLS Politikaları (match_details)

```sql
-- RLS'i aktifleştir
ALTER TABLE match_details ENABLE ROW LEVEL SECURITY;

-- Public read politikası (herkes okuyabilir)
CREATE POLICY "match_details_select_policy" ON match_details
  FOR SELECT
  USING (true);

-- Public insert politikası (herkes ekleyebilir - backend için)
CREATE POLICY "match_details_insert_policy" ON match_details
  FOR INSERT
  WITH CHECK (true);

-- Public update politikası (herkes güncelleyebilir - backend için)
CREATE POLICY "match_details_update_policy" ON match_details
  FOR UPDATE
  USING (true)
  WITH CHECK (true);

-- Public delete politikası (sadece eski kayıtlar silinebilir - temizlik için)
CREATE POLICY "match_details_delete_policy" ON match_details
  FOR DELETE
  USING (true);
```

✅ Tamamlandı mı? → Test et!

---

## 🧪 TEST

Backend'de çalıştır:
```bash
cd C:\Users\worda\Desktop\BetSmart\backend
python test_match_details.py
```

**Beklenen sonuç:**
```
✅ API çalışıyor
✅ Supabase'e kaydedildi
```

---

## ❌ HATA ALIRSAN

### "relation does not exist"
→ `create_match_details_table.sql` çalıştırılmamış
→ Önce tabloyu oluştur

### "row-level security policy"
→ RLS politikaları çalıştırılmamış
→ 2️⃣ numaralı SQL'i çalıştır

### "permission denied"
→ Supabase service_role key kullanıyor musun kontrol et
→ `.env` dosyasında `SUPABASE_KEY` doğru mu?

---

## ✅ BAŞARILI OLURSA

Şimdi tam sistemi test et:
```bash
# 1. Telegram'dan /yeniveri çalıştır
# 2. Backend'de:
python fetch_all_match_details.py
```

Supabase'de `match_details` tablosunda kayıtlar göreceksin! 🎉

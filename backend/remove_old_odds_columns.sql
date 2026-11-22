-- Eski oran sütunlarını kaldır
-- Artık first_odd_* ve current_odd_* kullanıyoruz

-- 1. Eski sütunları sil
ALTER TABLE odds_changes 
DROP COLUMN IF EXISTS old_odd_1,
DROP COLUMN IF EXISTS old_odd_x,
DROP COLUMN IF EXISTS old_odd_2,
DROP COLUMN IF EXISTS new_odd_1,
DROP COLUMN IF EXISTS new_odd_x,
DROP COLUMN IF EXISTS new_odd_2;

-- 2. Kontrol et - sadece yeni sütunlar kalmalı
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'odds_changes'
AND column_name LIKE '%odd%'
ORDER BY column_name;

-- Beklenen sonuç:
-- current_odd_1, current_odd_2, current_odd_x
-- first_odd_1, first_odd_2, first_odd_x

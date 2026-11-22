-- 1. Yeni kolonları ekle
ALTER TABLE odds_changes 
ADD COLUMN IF NOT EXISTS first_odd_1 DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS first_odd_x DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS first_odd_2 DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS current_odd_1 DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS current_odd_x DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS current_odd_2 DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS first_detected_at TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS last_updated_at TIMESTAMP WITH TIME ZONE;

-- 2. Mevcut verileri migrate et
UPDATE odds_changes 
SET 
  first_odd_1 = old_odd_1,
  first_odd_x = old_odd_x,
  first_odd_2 = old_odd_2,
  current_odd_1 = new_odd_1,
  current_odd_x = new_odd_x,
  current_odd_2 = new_odd_2,
  first_detected_at = detected_at,
  last_updated_at = detected_at
WHERE first_odd_1 IS NULL;

-- 3. Duplicate kayıtları temizle (en son kaydı tut, eskilerini sil)
DELETE FROM odds_changes a
USING odds_changes b
WHERE a.id < b.id 
  AND a.home_team = b.home_team 
  AND a.away_team = b.away_team 
  AND a.match_datetime = b.match_datetime;

-- 4. Unique constraint ekle
CREATE UNIQUE INDEX IF NOT EXISTS idx_odds_changes_unique_match 
ON odds_changes(home_team, away_team, match_datetime);

SELECT 'Schema updated and duplicates removed!' as status;

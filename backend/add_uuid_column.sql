-- future_matches tablosuna match_uuid kolonu ekle

ALTER TABLE future_matches 
ADD COLUMN IF NOT EXISTS match_uuid TEXT;

-- Index ekle (hızlı arama için)
CREATE INDEX IF NOT EXISTS idx_future_matches_uuid ON future_matches(match_uuid);

-- Yorum ekle
COMMENT ON COLUMN future_matches.match_uuid IS 'Sahadan API match UUID - match details için kullanılır';

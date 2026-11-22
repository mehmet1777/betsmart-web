-- matches tablosuna H2H sorguları için index'ler ekle
-- 393,000 maç var, ILIKE sorguları çok yavaş!

-- 1. home_team için text pattern index (ILIKE için)
CREATE INDEX IF NOT EXISTS idx_matches_home_team_pattern 
ON matches USING gin (home_team gin_trgm_ops);

-- 2. away_team için text pattern index
CREATE INDEX IF NOT EXISTS idx_matches_away_team_pattern 
ON matches USING gin (away_team gin_trgm_ops);

-- 3. Composite index (home + away beraber)
CREATE INDEX IF NOT EXISTS idx_matches_home_away 
ON matches (home_team, away_team);

-- 4. ID için index (sorting için)
CREATE INDEX IF NOT EXISTS idx_matches_id 
ON matches (id DESC);

-- NOT: gin_trgm_ops için pg_trgm extension gerekli
-- Eğer yoksa önce bunu çalıştır:
-- CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Index'lerin durumunu kontrol et
SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes
WHERE tablename = 'matches'
ORDER BY indexname;

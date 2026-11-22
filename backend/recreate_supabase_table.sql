-- 1. Eski tabloyu sil
DROP TABLE IF EXISTS matches;

-- 2. Yeni tabloyu oluştur (half_score dahil)
CREATE TABLE matches (
  id BIGSERIAL PRIMARY KEY,
  date TEXT,
  league TEXT,
  home_team TEXT NOT NULL,
  away_team TEXT NOT NULL,
  score TEXT,
  half_score TEXT,
  odd_1 REAL,
  odd_x REAL,
  odd_2 REAL,
  gg_yes REAL,
  gg_no REAL,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(date, home_team, away_team)
);

-- 3. Index'leri oluştur
CREATE INDEX idx_matches_odds ON matches(odd_1, odd_x, odd_2);
CREATE INDEX idx_matches_date ON matches(date);
CREATE INDEX idx_matches_teams ON matches(home_team, away_team);

-- 4. RLS'yi kapat
ALTER TABLE matches DISABLE ROW LEVEL SECURITY;

-- 5. İzinleri ver
GRANT ALL ON matches TO anon;
GRANT ALL ON matches TO authenticated;

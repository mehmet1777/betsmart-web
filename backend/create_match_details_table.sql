-- Match Details tablosu
-- Takım karşılaştırmaları, form durumu, H2H verileri

CREATE TABLE IF NOT EXISTS match_details (
  id SERIAL PRIMARY KEY,
  match_uuid TEXT UNIQUE NOT NULL,
  home_team TEXT NOT NULL,
  away_team TEXT NOT NULL,
  match_datetime TIMESTAMP,
  
  -- H2H (Aralarındaki Maçlar) - JSON
  h2h_data JSONB,
  
  -- Form Durumu - JSON
  form_home JSONB,
  form_away JSONB,
  
  -- Timestamps
  fetched_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Index'ler
CREATE INDEX IF NOT EXISTS idx_match_details_uuid ON match_details(match_uuid);
CREATE INDEX IF NOT EXISTS idx_match_details_datetime ON match_details(match_datetime);
CREATE INDEX IF NOT EXISTS idx_match_details_teams ON match_details(home_team, away_team);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_match_details_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_match_details_updated_at
BEFORE UPDATE ON match_details
FOR EACH ROW
EXECUTE FUNCTION update_match_details_updated_at();

-- Yorum
COMMENT ON TABLE match_details IS 'Maç detayları: H2H, form durumu, istatistikler';
COMMENT ON COLUMN match_details.h2h_data IS 'JSON: {total_matches, home_wins, draws, away_wins, avg_goals, matches[]}';
COMMENT ON COLUMN match_details.form_home IS 'JSON: {serie, goals_for, goals_against, over_25, btts, matches[]}';
COMMENT ON COLUMN match_details.form_away IS 'JSON: {serie, goals_for, goals_against, over_25, btts, matches[]}';

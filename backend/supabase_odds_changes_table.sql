-- Oran Değişiklikleri Tablosu
-- Her oran güncellemesinde eski ve yeni oranları saklar

CREATE TABLE IF NOT EXISTS odds_changes (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Maç bilgileri
  match_datetime TEXT NOT NULL,
  home_team TEXT NOT NULL,
  away_team TEXT NOT NULL,
  league TEXT,
  
  -- Eski oranlar
  old_odd_1 DECIMAL(10,2),
  old_odd_x DECIMAL(10,2),
  old_odd_2 DECIMAL(10,2),
  
  -- Yeni oranlar
  new_odd_1 DECIMAL(10,2) NOT NULL,
  new_odd_x DECIMAL(10,2) NOT NULL,
  new_odd_2 DECIMAL(10,2) NOT NULL,
  
  -- Değişim yüzdeleri
  change_1 DECIMAL(10,2),  -- MS1 değişim yüzdesi (+/-)
  change_x DECIMAL(10,2),  -- MSX değişim yüzdesi (+/-)
  change_2 DECIMAL(10,2),  -- MS2 değişim yüzdesi (+/-)
  
  -- Değişim yönü (genel)
  change_direction TEXT,  -- 'up', 'down', 'mixed'
  
  -- Toplam değişim büyüklüğü (mutlak değerler toplamı)
  total_change DECIMAL(10,2),
  
  -- Tespit zamanı
  detected_at TIMESTAMPTZ DEFAULT NOW(),
  
  -- Telegram'a gönderildi mi?
  telegram_sent BOOLEAN DEFAULT FALSE,
  telegram_sent_at TIMESTAMPTZ
);

-- İndeksler (hızlı sorgulama için)
CREATE INDEX IF NOT EXISTS idx_odds_changes_match ON odds_changes(home_team, away_team, match_datetime);
CREATE INDEX IF NOT EXISTS idx_odds_changes_datetime ON odds_changes(match_datetime);
CREATE INDEX IF NOT EXISTS idx_odds_changes_detected ON odds_changes(detected_at DESC);
CREATE INDEX IF NOT EXISTS idx_odds_changes_telegram ON odds_changes(telegram_sent) WHERE telegram_sent = FALSE;
CREATE INDEX IF NOT EXISTS idx_odds_changes_total_change ON odds_changes(total_change DESC);

-- Yorum ekle
COMMENT ON TABLE odds_changes IS 'Maç oranlarındaki değişiklikleri takip eder';
COMMENT ON COLUMN odds_changes.change_1 IS 'MS1 oran değişim yüzdesi (pozitif = artış, negatif = düşüş)';
COMMENT ON COLUMN odds_changes.change_direction IS 'Genel yön: up (çoğu arttı), down (çoğu düştü), mixed (karışık)';
COMMENT ON COLUMN odds_changes.total_change IS 'Toplam değişim büyüklüğü (önem sıralaması için)';

-- Örnek sorgular (yorum olarak)
/*
-- En son değişen oranlar
SELECT * FROM odds_changes 
ORDER BY detected_at DESC 
LIMIT 10;

-- Belirli bir maçın oran geçmişi
SELECT * FROM odds_changes 
WHERE home_team = 'Hannover 96' 
  AND away_team = 'Greuther Fürth'
ORDER BY detected_at DESC;

-- En büyük değişimler
SELECT * FROM odds_changes 
WHERE total_change > 10  -- %10'dan fazla değişim
ORDER BY total_change DESC 
LIMIT 20;

-- Telegram'a gönderilmemiş değişiklikler
SELECT * FROM odds_changes 
WHERE telegram_sent = FALSE 
ORDER BY detected_at DESC;
*/

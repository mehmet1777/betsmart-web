-- odds_changes tablosu için RLS politikalarını düzenle

-- RLS'i kapat (tüm erişime izin ver)
ALTER TABLE odds_changes DISABLE ROW LEVEL SECURITY;

-- VEYA RLS'i aç ama herkesin yazmasına izin ver
-- ALTER TABLE odds_changes ENABLE ROW LEVEL SECURITY;

-- CREATE POLICY "Enable insert for all users" ON odds_changes
--   FOR INSERT 
--   WITH CHECK (true);

-- CREATE POLICY "Enable select for all users" ON odds_changes
--   FOR SELECT 
--   USING (true);

-- CREATE POLICY "Enable update for all users" ON odds_changes
--   FOR UPDATE 
--   USING (true);

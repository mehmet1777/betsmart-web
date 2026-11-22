-- match_details tablosu için RLS politikaları

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

-- Yorum
COMMENT ON POLICY "match_details_select_policy" ON match_details IS 'Herkes match details okuyabilir';
COMMENT ON POLICY "match_details_insert_policy" ON match_details IS 'Backend match details ekleyebilir';
COMMENT ON POLICY "match_details_update_policy" ON match_details IS 'Backend match details güncelleyebilir';
COMMENT ON POLICY "match_details_delete_policy" ON match_details IS 'Temizlik için silme izni';

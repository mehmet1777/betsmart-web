#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open('app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 951-1043 arası eski kodu sil, yerine yeni kodu yaz
new_function = '''        @pyqtSlot(str)
        def processFutureMatches(self, all_data):
            """Mackolik'ten gelecek maçları parse et ve veritabanına kaydet - YENİ FORMAT"""
            try:
                print("🔄 Gelecek maçlar işleniyor (YENİ MACKOLIK FORMAT)...")
                print("=" * 50)
                
                # Yeni parse fonksiyonunu kullan
                from process_future_matches_new import parse_new_mackolik_format
                future_matches = parse_new_mackolik_format(all_data)
                
                print(f"\\n✅ {len(future_matches)} gelecek maç bulundu")
                
                # TEKRAR EDEN MAÇLARI TEMİZLE
                seen = set()
                unique_matches = []
                for match in future_matches:
                    key = f"{match['datetime']}|{match['home_team']}|{match['away_team']}"
                    if key not in seen:
                        seen.add(key)
                        unique_matches.append(match)
                
                future_matches = unique_matches
                print(f"✅ {len(future_matches)} unique maç kaldı")
                
                # Veritabanına kaydet
                conn = self.db.get_connection()
                cursor = conn.cursor()
                
                # future_matches tablosunu oluştur
                cursor.execute(\'\'\'
                    CREATE TABLE IF NOT EXISTS future_matches (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        datetime TEXT NOT NULL,
                        home_team TEXT NOT NULL,
                        away_team TEXT NOT NULL,
                        league TEXT,
                        odd_1 REAL,
                        odd_x REAL,
                        odd_2 REAL,
                        over_25 REAL,
                        under_25 REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(datetime, home_team, away_team)
                    )
                \'\'\')
                
                # Maçları kaydet
                saved_count = 0
                for match in future_matches:
                    try:
                        cursor.execute(\'\'\'
                            INSERT OR REPLACE INTO future_matches 
                            (datetime, home_team, away_team, league, odd_1, odd_x, odd_2, over_25, under_25)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        \'\'\', (
                            match['datetime'],
                            match['home_team'],
                            match['away_team'],
                            match['league'],
                            match['odd_1'],
                            match['odd_x'],
                            match['odd_2'],
                            match['over_25'],
                            match['under_25']
                        ))
                        saved_count += 1
                    except Exception as e:
                        print(f"❌ Kayıt hatası: {e}")
                        print(f"   Maç: {match['home_team']} vs {match['away_team']}")
                
                conn.commit()
                conn.close()
                
                print(f"✅ {saved_count} gelecek maç veritabanına kaydedildi")
                print("=" * 50)
                
                QMessageBox.information(
                    None,
                    "Başarılı",
                    f"{saved_count} gelecek maç başarıyla kaydedildi!\\n\\n"
                    f"Web sitesinde görüntülemek için localhost:3000'i yenileyin."
                )
                
            except Exception as e:
                print(f"❌ HATA: {e}")
                import traceback
                traceback.print_exc()
                QMessageBox.critical(
                    None,
                    "Hata",
                    f"Gelecek maçlar işlenirken hata oluştu:\\n{str(e)}"
                )
        
'''

# 950. satırdan başlayıp 1043. satıra kadar sil
new_lines = lines[:950] + [new_function] + lines[1043:]

with open('app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("✅ Fonksiyon değiştirildi!")
print(f"Eski: {len(lines)} satır")
print(f"Yeni: {len(new_lines)} satır")
print(f"Fark: {len(lines) - len(new_lines)} satır silindi")

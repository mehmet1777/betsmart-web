import sqlite3
import json
from datetime import datetime
import os

class Database:
    def __init__(self, db_path='betsmart.db'):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Veritabanı bağlantısı"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Veritabanı tablolarını oluştur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Maçlar tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                league TEXT,
                home_team TEXT,
                away_team TEXT,
                score TEXT,
                half_score TEXT,
                odd_1 REAL,
                odd_x REAL,
                odd_2 REAL,
                over REAL,
                under REAL,
                gg_yes REAL,
                gg_no REAL,
                over_1 REAL,
                under_1 REAL,
                over_2 REAL,
                under_2 REAL,
                mbs INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_played INTEGER DEFAULT 0
            )
        ''')
        
        # Tahminler tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                match_id INTEGER,
                prediction TEXT,
                confidence REAL,
                reason TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (match_id) REFERENCES matches (id)
            )
        ''')
        
        # Ayarlar tablosu
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_matches(self, matches_data):
        """Excel'den gelen maçları kaydet (is_played=1 olarak - geçmiş maçlar)"""
        if not matches_data:
            return 0
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        print(f"💾 {len(matches_data)} maç kaydediliyor...")
        
        # Önce mevcut maçları al (unique key ile: tarih + saat + takımlar + skor)
        existing_keys = set()
        cursor.execute('SELECT date, time, home_team, away_team, score FROM matches')
        for row in cursor.fetchall():
            # Daha güçlü unique key: tarih + saat + takımlar + skor
            key = f"{row[0]}|{row[1]}|{row[2]}|{row[3]}|{row[4]}"
            existing_keys.add(key)
        
        print(f"✅ Mevcut {len(existing_keys)} maç kontrolü yapıldı")
        
        # Yeni maçları filtrele
        new_matches = []
        for match in matches_data:
            # Aynı unique key formatı
            key = f"{match.get('date', '')}|{match.get('time', '')}|{match.get('home_team', '')}|{match.get('away_team', '')}|{match.get('score', '')}"
            if key not in existing_keys:
                new_matches.append(match)
        
        print(f"✅ {len(new_matches)} yeni maç bulundu, kaydediliyor...")
        
        # Batch insert
        saved_count = 0
        batch_size = 1000
        
        for i in range(0, len(new_matches), batch_size):
            batch = new_matches[i:i+batch_size]
            
            for match in batch:
                cursor.execute('''
                    INSERT INTO matches (
                        date, time, league, home_team, away_team, score, half_score,
                        odd_1, odd_x, odd_2, over, under, gg_yes, gg_no,
                        over_1, under_1, over_2, under_2, mbs, is_played
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    match.get('date', ''),
                    match.get('time', ''),
                    match.get('league', ''),
                    match.get('home_team', ''),
                    match.get('away_team', ''),
                    match.get('score', ''),
                    match.get('half_score', ''),
                    match.get('odd_1', 0),
                    match.get('odd_x', 0),
                    match.get('odd_2', 0),
                    match.get('over', 0),
                    match.get('under', 0),
                    match.get('gg_yes', 0),
                    match.get('gg_no', 0),
                    match.get('over_1', 0),
                    match.get('under_1', 0),
                    match.get('over_2', 0),
                    match.get('under_2', 0),
                    match.get('mbs', 0),
                    1  # is_played=1
                ))
                saved_count += 1
            
            conn.commit()
            print(f"⏳ {saved_count}/{len(new_matches)} kaydedildi...")
        
        conn.close()
        print(f"✅ Toplam {saved_count} maç kaydedildi")
        return saved_count
    
    def get_today_matches(self):
        """Tüm maçları getir (analiz için)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, date, time, league, home_team, away_team,
                   odd_1, odd_x, odd_2, over, under
            FROM matches 
            ORDER BY time DESC
            LIMIT 1000
        ''')
        
        matches = []
        for row in cursor.fetchall():
            matches.append({
                'id': row[0],
                'date': row[1],
                'time': row[2],
                'league': row[3],
                'home_team': row[4],
                'away_team': row[5],
                'odd_1': row[6],
                'odd_x': row[7],
                'odd_2': row[8],
                'over': row[9],
                'under': row[10]
            })
        
        conn.close()
        return matches
    
    def get_match_analysis(self, match_id):
        """Maç analizi yap"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Maçı getir
        cursor.execute('SELECT * FROM matches WHERE id = ?', (match_id,))
        match = cursor.fetchone()
        
        if not match:
            conn.close()
            return None
        
        # Geçmiş karşılaşmaları bul
        cursor.execute('''
            SELECT * FROM matches 
            WHERE ((home_team = ? AND away_team = ?) OR (home_team = ? AND away_team = ?))
            AND is_played = 1
            AND id != ?
            ORDER BY created_at DESC
            LIMIT 5
        ''', (match[4], match[5], match[5], match[4], match_id))
        
        history = cursor.fetchall()
        
        conn.close()
        
        return {
            'match': match,
            'history': history,
            'history_count': len(history)
        }
    
    def save_prediction(self, match_id, prediction, confidence, reason):
        """Tahmin kaydet"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO predictions (match_id, prediction, confidence, reason)
            VALUES (?, ?, ?, ?)
        ''', (match_id, prediction, confidence, reason))
        
        conn.commit()
        conn.close()
    
    def get_setting(self, key):
        """Ayar getir"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else None
    
    def save_setting(self, key, value):
        """Ayar kaydet"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)
        ''', (key, value))
        
        conn.commit()
        conn.close()

    def search_team_history(self, home_team, away_team, limit=5):
        """Takım isimlerine göre geçmiş maçları bul (fuzzy search)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Takım isimlerini normalize et (küçük harf, boşlukları temizle)
        home_normalized = home_team.lower().strip()
        away_normalized = away_team.lower().strip()
        
        # Fuzzy match için LIKE kullan
        cursor.execute('''
            SELECT date, time, league, home_team, away_team, score, half_score,
                   odd_1, odd_x, odd_2, over, under
            FROM matches 
            WHERE (
                (LOWER(home_team) LIKE ? AND LOWER(away_team) LIKE ?) OR
                (LOWER(home_team) LIKE ? AND LOWER(away_team) LIKE ?)
            )
            AND is_played = 1
            ORDER BY created_at DESC
            LIMIT ?
        ''', (
            f'%{home_normalized}%', f'%{away_normalized}%',
            f'%{away_normalized}%', f'%{home_normalized}%',
            limit
        ))
        
        matches = []
        for row in cursor.fetchall():
            matches.append({
                'date': row[0],
                'time': row[1],
                'league': row[2],
                'home_team': row[3],
                'away_team': row[4],
                'score': row[5],
                'half_score': row[6],
                'odd_1': row[7],
                'odd_x': row[8],
                'odd_2': row[9],
                'over': row[10],
                'under': row[11]
            })
        
        conn.close()
        return matches
    
    def search_by_odds_range(self, home_team, away_team, odd_1, odd_x, odd_2, limit=50):
        """
        KADEMELİ TOLERANS ile benzer maçları bul ve seviyelerine göre ayır
        
        Returns:
            dict: {
                'exact': [],      # ±0.01 (Aynı oranlar)
                'similar': [],    # ±0.02 (Yakın oranlar)
                'total_count': 0
            }
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        results = {
            'exact': [],      # ±0.01 tolerans
            'similar': [],    # ±0.02 tolerans
            'total_count': 0
        }
        
        # Seviye 1: ±0.01 (Aynı oranlar)
        tolerance = 0.01
        odd_1_min = odd_1 - tolerance
        odd_1_max = odd_1 + tolerance
        odd_x_min = odd_x - tolerance
        odd_x_max = odd_x + tolerance
        odd_2_min = odd_2 - tolerance
        odd_2_max = odd_2 + tolerance
        
        cursor.execute('''
            SELECT date, time, league, home_team, away_team, score, half_score,
                   odd_1, odd_x, odd_2, over, under,
                   ABS(odd_1 - ?) + ABS(odd_x - ?) + ABS(odd_2 - ?) as distance
            FROM matches 
            WHERE is_played = 1
            AND odd_1 > 0 AND odd_x > 0 AND odd_2 > 0
            AND odd_1 BETWEEN ? AND ?
            AND odd_x BETWEEN ? AND ?
            AND odd_2 BETWEEN ? AND ?
            ORDER BY distance ASC
            LIMIT ?
        ''', (
            odd_1, odd_x, odd_2,
            odd_1_min, odd_1_max,
            odd_x_min, odd_x_max,
            odd_2_min, odd_2_max,
            limit
        ))
        
        exact_results = cursor.fetchall()
        print(f"🎯 Tolerans ±0.01 (Aynı): {len(exact_results)} maç bulundu")
        
        # Seviye 2: ±0.02 (Yakın oranlar)
        tolerance = 0.02
        odd_1_min = odd_1 - tolerance
        odd_1_max = odd_1 + tolerance
        odd_x_min = odd_x - tolerance
        odd_x_max = odd_x + tolerance
        odd_2_min = odd_2 - tolerance
        odd_2_max = odd_2 + tolerance
        
        cursor.execute('''
            SELECT date, time, league, home_team, away_team, score, half_score,
                   odd_1, odd_x, odd_2, over, under,
                   ABS(odd_1 - ?) + ABS(odd_x - ?) + ABS(odd_2 - ?) as distance
            FROM matches 
            WHERE is_played = 1
            AND odd_1 > 0 AND odd_x > 0 AND odd_2 > 0
            AND odd_1 BETWEEN ? AND ?
            AND odd_x BETWEEN ? AND ?
            AND odd_2 BETWEEN ? AND ?
            ORDER BY distance ASC
            LIMIT ?
        ''', (
            odd_1, odd_x, odd_2,
            odd_1_min, odd_1_max,
            odd_x_min, odd_x_max,
            odd_2_min, odd_2_max,
            limit
        ))
        
        similar_results = cursor.fetchall()
        print(f"📊 Tolerans ±0.02 (Yakın): {len(similar_results)} maç bulundu")
        
        # Exact'ten similar'ı çıkar (çakışmaları engelle)
        exact_ids = set()
        for row in exact_results:
            match_id = f"{row[0]}_{row[1]}_{row[3]}_{row[4]}"  # date_time_home_away
            exact_ids.add(match_id)
            
            results['exact'].append({
                'date': row[0],
                'time': row[1],
                'league': row[2],
                'home_team': row[3],
                'away_team': row[4],
                'score': row[5],
                'half_score': row[6],
                'odd_1': row[7],
                'odd_x': row[8],
                'odd_2': row[9],
                'over': row[10],
                'under': row[11],
                'similarity': round(100 - (row[12] * 10), 1)
            })
        
        for row in similar_results:
            match_id = f"{row[0]}_{row[1]}_{row[3]}_{row[4]}"
            
            # Exact'te yoksa similar'a ekle
            if match_id not in exact_ids:
                results['similar'].append({
                    'date': row[0],
                    'time': row[1],
                    'league': row[2],
                    'home_team': row[3],
                    'away_team': row[4],
                    'score': row[5],
                    'half_score': row[6],
                    'odd_1': row[7],
                    'odd_x': row[8],
                    'odd_2': row[9],
                    'over': row[10],
                    'under': row[11],
                    'similarity': round(100 - (row[12] * 10), 1)
                })
        
        results['total_count'] = len(results['exact']) + len(results['similar'])
        
        print(f"✅ Toplam: {results['total_count']} maç (Aynı: {len(results['exact'])}, Yakın: {len(results['similar'])})")
        
        conn.close()
        return results
    
    def _calculate_tolerance(self, odd):
        """
        Oran için tolerans hesapla
        
        GENİŞ TOLERANS - Daha fazla eşleşme için
        """
        if odd < 2.0:
            return 0.20  # Çok geniş
        elif odd < 4.0:
            return 0.30  # Çok geniş
        else:
            return 0.40  # Çok geniş

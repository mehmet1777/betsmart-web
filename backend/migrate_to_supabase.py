"""
SQLite'daki tarihi maçları Supabase'e yükle
"""
import sqlite3
import os
from supabase import create_client, Client

# Supabase credentials
SUPABASE_URL = "https://sbgcxautbonzwfppgvbd.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNiZ2N4YXV0Ym9uendmcHBndmJkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTQ0MTUxMjIsImV4cCI6MjEwOTk5MTEyMn0.JxHeI-Z85JG0Yx-4lHINrau2kbFbEloFvHudWy8JXqw"

# SQLite database path
DB_PATH = r"C:\Users\worda\Desktop\betsmart yedek\betsmart.db"

def migrate_matches():
    """Tarihi maçları Supabase'e yükle"""
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database bulunamadı: {DB_PATH}")
        return
    
    print("🔌 Supabase'e bağlanılıyor...")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("📂 SQLite veritabanı açılıyor...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Toplam maç sayısını öğren
    cursor.execute("SELECT COUNT(*) FROM matches WHERE score IS NOT NULL AND score != ''")
    total = cursor.fetchone()[0]
    print(f"📊 Toplam tarihi maç: {total:,}")
    
    # Batch olarak yükle (1000'er maç)
    BATCH_SIZE = 1000
    offset = 0
    uploaded = 0
    failed = 0
    
    while offset < total:
        cursor.execute("""
            SELECT 
                date, league, home_team, away_team, score, half_score,
                odd_1, odd_x, odd_2, gg_yes, gg_no
            FROM matches 
            WHERE score IS NOT NULL AND score != ''
            ORDER BY date DESC
            LIMIT ? OFFSET ?
        """, (BATCH_SIZE, offset))
        
        rows = cursor.fetchall()
        if not rows:
            break
        
        # Supabase formatına çevir
        batch = []
        for row in rows:
            batch.append({
                'date': row[0],
                'league': row[1],
                'home_team': row[2],
                'away_team': row[3],
                'score': row[4],
                'half_score': row[5] if row[5] else None,
                'odd_1': float(row[6]) if row[6] else None,
                'odd_x': float(row[7]) if row[7] else None,
                'odd_2': float(row[8]) if row[8] else None,
                'gg_yes': float(row[9]) if row[9] else None,
                'gg_no': float(row[10]) if row[10] else None
            })
        
        # Supabase'e yükle
        try:
            result = supabase.table('matches').upsert(batch, on_conflict='date,home_team,away_team').execute()
            uploaded += len(batch)
            print(f"✅ {uploaded:,} / {total:,} maç yüklendi ({(uploaded/total*100):.1f}%)")
        except Exception as e:
            failed += len(batch)
            print(f"❌ Batch yükleme hatası: {e}")
        
        offset += BATCH_SIZE
    
    conn.close()
    
    print(f"\n🎉 Migration tamamlandı!")
    print(f"   ✅ Başarılı: {uploaded:,}")
    print(f"   ❌ Başarısız: {failed:,}")

if __name__ == '__main__':
    print("=" * 50)
    print("  SUPABASE MIGRATION")
    print("=" * 50)
    print()
    
    response = input("⚠️  Bu işlem uzun sürebilir (5-10 dakika). Devam? (y/n): ")
    if response.lower() == 'y':
        migrate_matches()
    else:
        print("İptal edildi.")

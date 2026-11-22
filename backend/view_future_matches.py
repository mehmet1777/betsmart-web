"""View future matches from the database"""
import sqlite3
from datetime import datetime

def view_future_matches():
    """Display all future matches"""
    print("⚽ Gelecek Maçlar Veritabanı")
    print("=" * 80)
    
    try:
        conn = sqlite3.connect('betsmart.db')
        cursor = conn.cursor()
        
        # Count total matches
        cursor.execute('SELECT COUNT(*) FROM future_matches')
        total = cursor.fetchone()[0]
        print(f"\n📊 Toplam {total} gelecek maç bulundu\n")
        
        if total == 0:
            print("⚠️ Henüz hiç gelecek maç kaydedilmemiş.")
            print("💡 Mackolik Parser'dan 'Gelecek Maçları Çek ve Kaydet' butonunu kullan!")
            conn.close()
            return
        
        # Get all matches
        cursor.execute('''
            SELECT id, datetime, home_team, away_team, league, 
                   odd_1, odd_x, odd_2, over_25, under_25, created_at
            FROM future_matches 
            ORDER BY datetime, id
        ''')
        
        matches = cursor.fetchall()
        
        print("-" * 80)
        for match in matches:
            mid, dt, home, away, league, o1, ox, o2, over, under, created = match
            
            print(f"ID: {mid}")
            print(f"📅 Tarih/Saat: {dt}")
            print(f"🏆 Lig: {league}")
            print(f"⚽ Maç: {home} vs {away}")
            print(f"💰 Oranlar: 1={o1:.2f}  X={ox:.2f}  2={o2:.2f}")
            print(f"📊 2.5 Üst/Alt: {over:.2f} / {under:.2f}")
            print(f"🕐 Kaydedilme: {created}")
            print("-" * 80)
        
        conn.close()
        
    except sqlite3.OperationalError as e:
        if 'no such table' in str(e):
            print("❌ future_matches tablosu bulunamadı!")
            print("💡 İlk kullanımda Mackolik Parser'dan 'Gelecek Maçları Çek ve Kaydet' butonuna tıklayın.")
        else:
            print(f"❌ Veritabanı hatası: {e}")
    except Exception as e:
        print(f"❌ Hata: {e}")

def search_team(team_name):
    """Search for matches by team name"""
    print(f"\n🔍 '{team_name}' takımı aranıyor...")
    print("=" * 80)
    
    try:
        conn = sqlite3.connect('betsmart.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT datetime, home_team, away_team, league, 
                   odd_1, odd_x, odd_2
            FROM future_matches 
            WHERE home_team LIKE ? OR away_team LIKE ?
            ORDER BY datetime
        ''', (f'%{team_name}%', f'%{team_name}%'))
        
        matches = cursor.fetchall()
        
        if not matches:
            print(f"⚠️ '{team_name}' için gelecek maç bulunamadı.")
            conn.close()
            return
        
        print(f"✅ {len(matches)} maç bulundu:\n")
        print("-" * 80)
        for match in matches:
            dt, home, away, league, o1, ox, o2 = match
            print(f"📅 {dt}")
            print(f"🏆 {league}")
            print(f"⚽ {home} vs {away}")
            print(f"💰 {o1:.2f} / {ox:.2f} / {o2:.2f}")
            print("-" * 80)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Hata: {e}")

def delete_all_future_matches():
    """Delete all future matches (for testing)"""
    response = input("⚠️ Tüm gelecek maçları silmek istediğinize emin misiniz? (evet/hayır): ")
    
    if response.lower() != 'evet':
        print("❌ İşlem iptal edildi.")
        return
    
    try:
        conn = sqlite3.connect('betsmart.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM future_matches')
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"✅ {deleted} gelecek maç silindi.")
        
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'search' and len(sys.argv) > 2:
            search_team(' '.join(sys.argv[2:]))
        elif command == 'delete':
            delete_all_future_matches()
        else:
            print("Kullanım:")
            print("  python view_future_matches.py          - Tüm gelecek maçları göster")
            print("  python view_future_matches.py search <takım>  - Takım ara")
            print("  python view_future_matches.py delete   - Tüm gelecek maçları sil")
    else:
        view_future_matches()

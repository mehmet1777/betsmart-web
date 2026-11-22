"""
Veritabanı düzeltme scripti
"""

from database import Database

print("🔧 VERİTABANI DÜZELTİLİYOR...")
print("="*60)

db = Database()
conn = db.get_connection()
cursor = conn.cursor()

# Tüm maçları is_played = 1 yap (geçmiş maçlar olduğu için)
print("\n📝 Tüm maçlar is_played = 1 olarak işaretleniyor...")

cursor.execute("""
    UPDATE matches 
    SET is_played = 1
""")

affected = cursor.rowcount
conn.commit()

print(f"✅ {affected} maç güncellendi!")

# Kontrol
cursor.execute("SELECT COUNT(*) FROM matches WHERE is_played = 1")
played = cursor.fetchone()[0]
print(f"✅ Oynanmış maç sayısı: {played}")

# Test: 2.75/3.09/2.00 aralığında maç var mı?
print(f"\n🔍 ORAN ARAMA TESTİ:")
cursor.execute("""
    SELECT COUNT(*) FROM matches
    WHERE is_played = 1
    AND odd_1 BETWEEN 2.60 AND 2.90
    AND odd_x BETWEEN 2.94 AND 3.24
    AND odd_2 BETWEEN 1.90 AND 2.10
""")
match_count = cursor.fetchone()[0]
print(f"✅ Eşleşen maç sayısı: {match_count}")

if match_count > 0:
    cursor.execute("""
        SELECT home_team, away_team, odd_1, odd_x, odd_2, score
        FROM matches
        WHERE is_played = 1
        AND odd_1 BETWEEN 2.60 AND 2.90
        AND odd_x BETWEEN 2.94 AND 3.24
        AND odd_2 BETWEEN 1.90 AND 2.10
        ORDER BY ABS(odd_1 - 2.75) + ABS(odd_x - 3.09) + ABS(odd_2 - 2.00)
        LIMIT 5
    """)
    
    print(f"\n📋 EN BENZER 5 MAÇ:")
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f"\n{i}. {row[0]} vs {row[1]}")
        print(f"   Oranlar: {row[2]}/{row[3]}/{row[4]}")
        print(f"   Skor: {row[5]}")

conn.close()

print("\n" + "="*60)
print("✅ Düzeltme tamamlandı!")
print("\n🎯 Artık Telegram'da screenshot atın, sonuç bulacak!")

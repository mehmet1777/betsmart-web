import sqlite3

conn = sqlite3.connect('betsmart.db')
cursor = conn.cursor()

cursor.execute('DELETE FROM future_matches')
deleted = cursor.rowcount

conn.commit()
conn.close()

print(f"✅ {deleted} gelecek maç temizlendi")

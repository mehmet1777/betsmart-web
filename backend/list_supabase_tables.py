"""
Supabase'deki tüm tabloları listele
"""
from supabase_sync import get_supabase_client

client = get_supabase_client()

# Bilinen tablo isimlerini dene
test_tables = [
    'past_matches',
    'future_matches',
    'matches',
    'historical_matches',
    'completed_matches',
    'finished_matches'
]

print("=" * 70)
print("SUPABASE TABLO KONTROLÜ")
print("=" * 70)
print()

for table_name in test_tables:
    try:
        result = client.table(table_name).select('*').limit(1).execute()
        count_result = client.table(table_name).select('id').execute()
        
        print(f"✓ {table_name}")
        print(f"  Kayıt sayısı: {len(count_result.data)}")
        
        if result.data:
            first = result.data[0]
            print(f"  Columns: {list(first.keys())[:10]}...")  # İlk 10 column
        print()
    except Exception as e:
        error_msg = str(e)
        if 'PGRST205' in error_msg or 'not find' in error_msg:
            print(f"✗ {table_name} - TABLO YOK")
        else:
            print(f"✗ {table_name} - HATA: {error_msg[:100]}")
        print()

print("=" * 70)

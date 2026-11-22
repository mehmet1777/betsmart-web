"""
matches tablosunun kolonlarini kontrol et
"""

from supabase_sync import get_supabase_client

try:
    client = get_supabase_client()
    
    # İlk bir satırı çek, kolonları gör
    result = client.table('matches').select('*').limit(1).execute()
    
    if result.data and len(result.data) > 0:
        first_row = result.data[0]
        
        print("="*80)
        print("MATCHES TABLOSU KOLONLARI:")
        print("="*80)
        
        for col_name, col_value in first_row.items():
            value_str = str(col_value)[:50] if col_value else "NULL"
            print(f"{col_name:30s} = {value_str}")
        
        print("\n" + "="*80)
        print("TOPLAM SUTUN SAYISI:", len(first_row))
        
    else:
        print("matches tablosunda veri yok!")
        
except Exception as e:
    print(f"HATA: {e}")
    import traceback
    traceback.print_exc()

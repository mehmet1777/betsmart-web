"""
Supabase'de migration çalıştır
"""
from supabase_sync import get_supabase_client

def run_migration():
    """SQL migration dosyasını çalıştır"""
    client = get_supabase_client()
    
    # SQL dosyasını oku
    with open('create_match_details_table.sql', 'r', encoding='utf-8') as f:
        sql = f.read()
    
    print("SUPABASE MIGRATION")
    print("="*80)
    print("SQL çalıştırılıyor...")
    
    try:
        # Supabase SQL Editor'da çalıştırmak lazım
        # Python SDK direkt SQL execute etmiyor
        
        print("\n⚠️  SQL dosyasını manuel çalıştırmanız gerekiyor:")
        print("\n1. Supabase Dashboard'a gidin:")
        print("   https://supabase.com/dashboard/project/YOUR_PROJECT/editor")
        print("\n2. SQL Editor'ı açın")
        print("\n3. create_match_details_table.sql içeriğini yapıştırın")
        print("\n4. Run tuşuna basın")
        
        print("\n" + "="*80)
        print("SQL İÇERİĞİ:")
        print("="*80)
        print(sql)
        
        return False
        
    except Exception as e:
        print(f"Hata: {e}")
        return False

if __name__ == '__main__':
    run_migration()

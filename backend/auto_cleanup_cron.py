"""
Otomatik Temizlik - Her saat çalışır
Windows Task Scheduler veya Linux cron ile kullanılır
"""
from supabase_sync import clean_old_matches
from datetime import datetime

if __name__ == "__main__":
    print(f"\n{'='*50}")
    print(f"⏰ Otomatik Temizlik - {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print(f"{'='*50}")
    
    deleted_count = clean_old_matches()
    
    if deleted_count > 0:
        print(f"✅ {deleted_count} eski maç temizlendi")
    else:
        print(f"✅ Temizlenecek maç yok")
    
    print(f"{'='*50}\n")

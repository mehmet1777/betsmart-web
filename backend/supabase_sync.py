"""
Supabase Cloud Database Sync Module
Desktop uygulamasından Supabase'e maç verilerini senkronize eder
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv
from typing import List, Dict

# .env dosyasını yükle
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase_client() -> Client:
    """Supabase client oluştur"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL ve SUPABASE_KEY .env dosyasında tanımlı olmalı!")
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def clean_old_matches():
    """
    Bugünden önceki tüm maçları Supabase'den sil
    """
    try:
        from datetime import datetime
        supabase: Client = get_supabase_client()
        
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_str = today.strftime("%d.%m.%Y")
        
        print(f"\n🗑️  {today_str} öncesi eski maçlar temizleniyor...")
        
        # Tüm maçları çek
        all_matches = supabase.table('future_matches').select('id,datetime').execute()
        
        deleted_count = 0
        for match in all_matches.data:
            try:
                # datetime formatı: "21.11.2026 04:00" veya "14/11/2026 04:00"
                match_date_str = match['datetime'].split(' ')[0]
                
                # Slash formatını atla (bozuk veri)
                if '/' in match_date_str:
                    supabase.table('future_matches').delete().eq('id', match['id']).execute()
                    deleted_count += 1
                    continue
                
                # Nokta formatını parse et
                day, month, year = match_date_str.split('.')
                match_date = datetime(int(year), int(month), int(day))
                
                # Bugünden önceki maçları sil
                if match_date.date() < today.date():
                    supabase.table('future_matches').delete().eq('id', match['id']).execute()
                    deleted_count += 1
                    
            except Exception as e:
                # Parse edilemeyen maçları da sil (bozuk veri)
                try:
                    supabase.table('future_matches').delete().eq('id', match['id']).execute()
                    deleted_count += 1
                except:
                    pass
        
        print(f"✅ {deleted_count} eski/bozuk maç temizlendi")
        return deleted_count
        
    except Exception as e:
        print(f"⚠️  Temizlik hatası: {e}")
        return 0


def sync_matches_to_supabase(matches: List[Dict]) -> tuple:
    """
    Maçları Supabase'e senkronize et
    
    Args:
        matches: Maç listesi (dict formatında)
    
    Returns:
        (success_count, error_count) tuple
    """
    try:
        supabase: Client = get_supabase_client()
        success_count = 0
        error_count = 0
        
        # Önce eski maçları temizle
        clean_old_matches()
        
        print(f"\n🔄 Supabase'e {len(matches)} maç gönderiliyor...")
        print("=" * 50)
        
        # APPEND MODE: Eski maçları silme, sadece yeni ekle
        # Duplicate maçları önlemek için: datetime+home_team+away_team unique olmalı
        
        # Yeni maçları ekle (upsert kullan - varsa güncelle, yoksa ekle)
        for match in matches:
            try:
                data = {
                    'datetime': match['datetime'],
                    'home_team': match['home_team'],
                    'away_team': match['away_team'],
                    'league': match.get('league', ''),
                    'odd_1': float(match.get('odd_1') or 0),
                    'odd_x': float(match.get('odd_x') or 0),
                    'odd_2': float(match.get('odd_2') or 0),
                    'over_25': float(match.get('over_25') or 0),
                    'under_25': float(match.get('under_25') or 0)
                }
                
                # UPSERT: Aynı datetime+home_team+away_team varsa güncelle, yoksa ekle
                supabase.table('future_matches').upsert(data, on_conflict='datetime,home_team,away_team').execute()
                success_count += 1
                
                if success_count % 10 == 0:
                    print(f"   📤 {success_count} maç yüklendi...")
                
            except Exception as e:
                error_count += 1
                print(f"❌ Hata: {match['home_team']} vs {match['away_team']} - {e}")
        
        print("=" * 50)
        print(f"✅ Supabase senkronizasyonu tamamlandı!")
        print(f"   📊 Başarılı: {success_count} maç")
        print(f"   ❌ Hata: {error_count} maç")
        
        return (success_count, error_count)
        
    except Exception as e:
        print(f"❌ Supabase bağlantı hatası: {e}")
        import traceback
        traceback.print_exc()
        return (0, len(matches))

def test_supabase_connection() -> bool:
    """Supabase bağlantısını test et"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('future_matches').select("count", count='exact').execute()
        print(f"✅ Supabase bağlantısı başarılı! ({result.count} maç mevcut)")
        return True
    except Exception as e:
        print(f"❌ Supabase bağlantı hatası: {e}")
        return False

if __name__ == "__main__":
    # Test
    test_supabase_connection()

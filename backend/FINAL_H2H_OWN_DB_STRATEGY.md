# Kendi Database'den H2H Çekme - Final Strateji

## 🎉 KEŞIF: 393,000 Geçmiş Maç Datamız Var!

**Kaynaklar**:
- fetch_2020.py - 2025.py (yıl bazlı)
- fetch_bulk_past_matches.py (toplu)
- Mackolik LiveData API
- 2020-2026 arası maçlar

## 📊 Test Sonuçları

### ✅ Başarılı:
```python
# matches tablosunda 393k maç var
# Türkiye ligi maçları mevcut:
Amed SK 5-1 Eyüpspor
Trabzonspor 2-0 Gaziantep FK
Kasımpaşa 2-2 Beşiktaş
```

### ⚠️ Sorunlar:
1. **ILIKE timeout** - 393k maç, index yok, full table scan yapamıyor
2. **Exact match çalışıyor** - Ama takım isimleri tam eşleşmeli
3. **Galatasaray vs Fenerbahçe** - 0 maç (takım isimleri farklı yazılmış olabilir)

## 🔧 Çözüm Stratejisi

### ÇÖZÜM 1: Index Ekle (ÖNCELİKLİ) ⭐⭐⭐⭐⭐

**SQL** (`create_h2h_indexes.sql`):
```sql
-- pg_trgm extension
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- GIN index for ILIKE queries
CREATE INDEX idx_matches_home_team_pattern 
ON matches USING gin (home_team gin_trgm_ops);

CREATE INDEX idx_matches_away_team_pattern 
ON matches USING gin (away_team gin_trgm_ops);
```

**Avantajlar**:
- ✅ ILIKE sorguları hızlanır (10sn → 0.1sn)
- ✅ Fuzzy matching destekler
- ✅ Bir kere ekle, sürekli kullan

### ÇÖZÜM 2: Exact Match + Normalization ⭐⭐⭐⭐

**Python**:
```python
def normalize_team_name(name):
    """Takım ismini normalize et"""
    # SK, FC, gibi ekleri kaldır
    name = name.replace(' SK', '').replace(' FC', '')
    name = name.replace('İstanbul', '').strip()
    return name

# future_matches'ten takım isimleri
home_normalized = normalize_team_name(home_team)
away_normalized = normalize_team_name(away_team)

# matches'te ara
h2h = matches.eq('home_team', home_normalized).eq('away_team', away_normalized)
```

**Avantajlar**:
- ✅ Hızlı (exact match)
- ✅ Index gerekmez
- ⚠️ Normalization kuralları gerekir

### ÇÖZÜM 3: Fuzzy Matching ⭐⭐⭐

**Python** (fuzzywuzzy):
```python
from fuzzywuzzy import fuzz

# Tüm Türkiye liginden takımları çek (1000-2000 takım)
turkish_teams = get_all_turkish_teams()

# En yakın eşleşmeyi bul
best_match = max(turkish_teams, key=lambda t: fuzz.ratio(search_name, t))

if fuzz.ratio(search_name, best_match) > 85:
    # Yeterince yakın, kullan
    use_team_name = best_match
```

**Avantajlar**:
- ✅ Farklı yazımları bulur
- ✅ Typo-tolerant
- ⚠️ Yavaş (tüm takımlarla karşılaştır)

## 🎯 Önerilen Uygulama

### match_details_api.py'ye ekle:

```python
def fetch_match_details_with_fallback(match_uuid, home_team, away_team):
    """
    1. Sahadan API
    2. Kendi database (fallback)
    """
    
    # 1. Sahadan'dan dene
    success, data, error = fetch_from_sahadan(match_uuid)
    if success:
        return success, data, error
    
    # 2. Kendi database'den H2H çek
    if error and '502' in str(error):
        print(f"Sahadan 502, kendi DB'den deniyoruz...")
        
        success_db, data_db = fetch_h2h_from_own_db(home_team, away_team)
        if success_db:
            return True, data_db, None
    
    return False, None, "Hiçbir kaynaktan detay çekilemedi"


def fetch_h2h_from_own_db(home_team, away_team):
    """Kendi database'den H2H çek"""
    from supabase_sync import get_supabase_client
    
    client = get_supabase_client()
    
    # Normalize team names
    home_norm = normalize_team_name(home_team)
    away_norm = normalize_team_name(away_team)
    
    # H2H sorgusu
    h2h_1 = client.table('matches').select('*').eq(
        'home_team', home_norm
    ).eq('away_team', away_norm).limit(10).execute()
    
    h2h_2 = client.table('matches').select('*').eq(
        'home_team', away_norm
    ).eq('away_team', home_norm).limit(10).execute()
    
    all_h2h = h2h_1.data + h2h_2.data
    
    if len(all_h2h) > 0:
        # Sahadan format'ına çevir
        formatted_data = format_h2h_to_sahadan_format(all_h2h, home_norm, away_norm)
        return True, formatted_data
    
    return False, None
```

## 📈 Beklenen Coverage

| Kaynak | Başarı Oranı | Açıklama |
|--------|--------------|----------|
| Sahadan API | %40 (49/121) | Mevcut |
| Kendi DB (fallback) | +%35-40 | 393k maç, popüler takımlar |
| **TOPLAM** | **%75-80** | 🎉 |

## 🚀 Sonraki Adımlar

### Adım 1: Index Ekle (5 dakika)
```bash
# Supabase Dashboard → SQL Editor
# create_h2h_indexes.sql'i çalıştır
```

### Adım 2: Normalize Function (30 dakika)
```python
# match_details_api.py'ye ekle
def normalize_team_name(name):
    # Türkiye takımları için özel kurallar
    ...
```

### Adım 3: Fallback Logic (1 saat)
```python
# fetch_match_details_with_fallback() implement et
# Test et
```

### Adım 4: Test (30 dakika)
```bash
# Galatasaray vs Fenerbahçe
# Beşiktaş vs Trabzonspor
# vb. popüler maçlar
```

## 💡 Alternatif: H2H Cache Tablosu

Eğer performans kritikse:

```sql
CREATE TABLE h2h_cache (
    id SERIAL PRIMARY KEY,
    team1 TEXT NOT NULL,
    team2 TEXT NOT NULL,
    h2h_data JSONB,
    last_updated TIMESTAMP DEFAULT NOW(),
    UNIQUE(team1, team2)
);

CREATE INDEX idx_h2h_teams ON h2h_cache(team1, team2);
```

**Avantajlar**:
- ✅ Çok hızlı (pre-calculated)
- ✅ Index'li
- ⚠️ Ekstra maintenance
- ⚠️ Güncel tutmak gerekir

## 🎯 Karar

**ÖNERİM**: ÇÖZÜM 1 (Index) + ÇÖZÜM 2 (Normalization)

**Sebep**:
1. Index ile ILIKE hızlanır
2. Normalization ile exact match çalışır
3. 393k maç verisi kullanılır
4. %75-80 coverage elde edilir

**Zaman**: 2-3 saat
**Sonuç**: Production-ready H2H fallback sistemi

---

**Başlayalım mı?** 🚀

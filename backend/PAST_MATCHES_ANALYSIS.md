# Geçmiş Maç Çekme Sistemi - Analiz Raporu

## 📋 Mevcut Dosyalar

### 1. Yıl Bazlı Fetch Scriptleri
```
fetch_2020.py - 2020 yılı (01.01.2020 - 31.12.2020)
fetch_2021.py - 2021 yılı
fetch_2022.py - 2022 yılı
fetch_2023.py - 2023 yılı
fetch_2024.py - 2024 yılı
fetch_2025.py - 2025 yılı
```

**Çalışma Mantığı**:
- Mackolik LiveData API kullanıyor: `https://vd.mackolik.com/livedata?date={DD/MM/YYYY}`
- Her gün için tek tek çekiyor (365 gün)
- 0.00 oranlı maçları filtre ediyor (iddaa'da olmayan maçlar)
- Excel'e kaydediyor (Desktop'a)

### 2. Toplu Çekme Scriptleri
```
fetch_bulk_past_matches.py - Tarih aralığı ile toplu çekme
fetch_by_year.py - Yıl seçerek çekme
fetch_past_matches_to_excel.py - Excel export
```

### 3. Özel Çekme Scriptleri
```
fetch_turkey_matches.py - Sadece Türkiye ligleri
fetch_daily_matches.py - Günlük maçlar
```

## 🔍 Kritik Kod Analizi

### Oran Filtresi (0.00 oranları atma)
```python
# 0.00 oranlı maçları filtrele (iddaa'da yok)
if odd_1 == 0 or odd_1 == "0" or odd_1 == "0.00":
    continue
```

**Sebep**: İddaa'da olmayan maçların oranı 0.00 geliyor.

### Mackolik API Response Format
```python
match[2]  = home_team
match[4]  = away_team
match[7]  = halftime_score (İY)
match[12] = home_score
match[13] = away_score
match[16] = match_time
match[18] = odd_1 (MS 1)
match[19] = odd_x (MS X)
match[20] = odd_2 (MS 2)
match[21] = under_25
match[22] = over_25
match[35] = match_date
match[36] = league_data
```

### Excel Format
```
Saat | BOŞ_B | Lig | Mbs | Ev Sahibi | MS | Deplasman | İY | 1 | X | 2 | Alt 2.5 | Üst 2.5
```

**Özel Özellikler**:
- B sütunu boş (BOŞ_B)
- Mbs sabit 3
- Oranlar 0 ise 1.01 olarak kaydediliyor

## 📊 Veri Akışı

```
1. Mackolik LiveData API → Günlük maç datası
2. Parse et → Match bilgileri + oranlar
3. Filtrele → 0.00 oranlı maçları at
4. Format → Excel yapısına uygun düzenle
5. Kaydet → Desktop'a Excel dosyası
```

## 🎯 Kullanım Durumları

### Durum 1: Yıl bazında çekme
```bash
python fetch_2020.py  # 2020 yılının tamamı
```

### Durum 2: Tarih aralığı
```bash
python fetch_bulk_past_matches.py
# Start: 01.01.2026
# End: 10.11.2026
```

### Durum 3: Sadece Türkiye
```bash
python fetch_turkey_matches.py
```

## 🔄 Supabase Entegrasyonu

### Mevcut Sistem:
- Excel'e kayıt yapılıyor
- Manuel olarak `import_excel_to_db.py` ile Supabase'e aktarılıyor

### Tablolar:
```
matches - Geçmiş maçlar (is_played=1)
past_matches - Alternatif geçmiş maç tablosu
future_matches - Gelecek maçlar (is_played=0)
```

## ⚠️ Sorunlar ve Çözümler

### Sorun 1: 0.00 Oranlı Maçlar
**Problem**: İddaa'da olmayan maçlar API'den 0.00 ile geliyor
**Çözüm**: Filtre ile atılıyor ✅

### Sorun 2: API Rate Limiting
**Problem**: Çok hızlı istek atılırsa block olabilir
**Çözüm**: Her istekte 0.3-0.5 saniye bekleniyor ✅

### Sorun 3: Tarih Formatı
**Problem**: API DD/MM/YYYY, Python DD.MM.YYYY kullanıyor
**Çözüm**: Format conversion yapılıyor ✅

## 📈 İstatistikler (Tahmin)

**2020-2025 (6 yıl)**:
- ~365 gün x 6 yıl = 2190 gün
- Ortalama 150 maç/gün
- **Toplam: ~328,500 maç**

**Dosya Boyutu**:
- Excel: ~50-100 MB/yıl
- Database: ~200-300 MB toplam

## 🚀 Öneriler

### Öneri 1: Otomatik Supabase Sync
```python
# fetch_bulk_past_matches.py'ye ekle:
from supabase_sync import sync_matches_to_supabase

if all_matches:
    # Excel'e kaydet
    save_to_excel(all_matches, filename)
    
    # Supabase'e de direkt kaydet
    sync_matches_to_supabase(all_matches, is_played=True)
```

### Öneri 2: Incremental Update
```python
# Son çekilen tarihi kaydet
# Sadece yeni günleri çek
# Daha hızlı ve verimli
```

### Öneri 3: Background Job
```python
# Her gece 02:00'de otomatik çalış
# Dünün maçlarını çek
# Supabase'e kaydet
```

## 🧪 Test Komutları

```bash
# Tek bir tarihi test et
python -c "from fetch_bulk_past_matches import fetch_past_matches; print(len(fetch_past_matches('23.11.2026')))"

# 0.00 oran kontrolü
python -c "from fetch_2020 import fetch_past_matches; matches = fetch_past_matches('01.01.2020'); print('0.00 var mi:', any(m['MS 1'] == 0 for m in matches))"

# Excel format kontrolü
python fetch_bulk_past_matches.py  # Script çalıştır, Excel'i kontrol et
```

## 📝 Sonuç

**Sistem durumu**: ✅ Çalışıyor ve production-ready

**Özellikler**:
- ✅ Mackolik LiveData API entegrasyonu
- ✅ 0.00 oran filtresi
- ✅ Excel export
- ✅ Yıl ve tarih aralığı desteği
- ⚠️ Manuel Supabase sync (otomasyon eklenebilir)

**Kullanım**:
- Geçmiş maç analizi için
- Model eğitimi için
- İstatistiksel analizler için

**Sonraki adımlar**:
1. Otomatik Supabase sync ekle
2. Incremental update yap
3. Background job olarak çalıştır
4. API rate limiting monitoring ekle

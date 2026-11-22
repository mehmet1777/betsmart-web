# Alternatif H2H API Siteleri

## 🎯 Test Edilecek Siteler

### 1. **API-Football** (api-football.com)
```
Endpoint: https://api-football-v1.p.rapidapi.com/v3/fixtures/headtohead
Features:
  - H2H data
  - Form data
  - Standings
  
ARTILARI:
  ✅ Resmi API
  ✅ JSON response
  ✅ Dokümantasyon var
  
EKSILERI:
  ❌ Ücretli (free tier: 100 requests/day)
  ❌ RapidAPI key gerekiyor
```

### 2. **Football-Data.org**
```
Endpoint: https://api.football-data.org/v4/matches/{id}/head2head
Features:
  - H2H data
  - European ligler (Premier League, La Liga, vb.)
  
ARTILARI:
  ✅ Ücretsiz tier var (10 requests/min)
  ✅ JSON API
  ✅ Güvenilir
  
EKSILERI:
  ❌ Sadece Avrupa ligleri
  ❌ API key gerekiyor
```

### 3. **SofaScore** (sofascore.com)
```
Endpoint: https://api.sofascore.com/api/v1/event/{eventId}/h2h
Features:
  - H2H data
  - Form data
  - Live scores
  
ARTILARI:
  ✅ Ücretsiz (unofficial)
  ✅ Geniş kapsam (tüm dünya)
  ✅ JSON API
  
EKSILERI:
  ⚠️ Unofficial API (her an değişebilir)
  ⚠️ Rate limiting
```

### 4. **FlashScore** (flashscore.com)
```
Endpoint: HTML scraping
Features:
  - H2H data
  - Form data
  - Tüm dünya ligleri
  
ARTILARI:
  ✅ Çok geniş kapsam
  ✅ Güvenilir data
  
EKSILERI:
  ❌ API yok (scraping gerekiyor)
  ❌ HTML parse karmaşık
```

### 5. **FotMob** (fotmob.com)
```
Endpoint: https://www.fotmob.com/api/matchDetails?matchId={id}
Features:
  - H2H data
  - Form data
  - Stats
  
ARTILARI:
  ✅ Ücretsiz
  ✅ JSON API
  ✅ Mobile-friendly
  
EKSILERI:
  ⚠️ Unofficial
  ⚠️ Match ID bulmak zor
```

### 6. **LiveScore** (livescore.com)
```
Features:
  - H2H data
  - Form data
  
EKSILERI:
  ❌ API yok
  ❌ Heavy JavaScript rendering
```

## 🧪 Test Planı

### Öncelik 1: SofaScore
**Sebep**: Ücretsiz, JSON API, geniş kapsam

**Test adımları**:
1. SofaScore match ID bul
2. H2H API test et
3. Match ID'yi otomatik bulabilir miyiz?

### Öncelik 2: FotMob
**Sebep**: Ücretsiz, JSON API, mobile-first

**Test adımları**:
1. FotMob API dokümantasyonu ara
2. Match ID pattern'i bul
3. H2H endpoint test et

### Öncelik 3: API-Football (ücretli ama güvenilir)
**Sebep**: Resmi API, dokümante

**Test adımları**:
1. Free tier signup
2. API key al
3. 100 requests/day yeterli mi hesapla

## 📊 Karşılaştırma

| Site | API | Ücretsiz | JSON | Match ID | Coverage | Öncelik |
|------|-----|----------|------|----------|----------|---------|
| Nesine | ✅ | ✅ | ✅ | ❓ | 🇹🇷 | ⭐⭐⭐ |
| SofaScore | ✅ | ✅ | ✅ | ❓ | 🌍 | ⭐⭐⭐⭐ |
| FotMob | ✅ | ✅ | ✅ | ❓ | 🌍 | ⭐⭐⭐ |
| API-Football | ✅ | 💰 | ✅ | ✅ | 🌍 | ⭐⭐ |
| Football-Data | ✅ | ⚠️ | ✅ | ✅ | 🇪🇺 | ⭐⭐ |
| Mackolik | ❌ | ✅ | ❌ | ❌ | 🇹🇷 | ⭐ |
| Sahadan | ✅ | ✅ | ✅ | ✅ | 🇹🇷 | ⭐⭐⭐⭐⭐ |

## 🎯 Önerilen Strateji

**Primary**: Sahadan (mevcut, %40 başarı)
**Fallback 1**: SofaScore (ücretsiz, geniş)
**Fallback 2**: FotMob (ücretsiz, kolay)
**Fallback 3**: API-Football (100/day limit)

## 📝 Sonraki Adımlar

1. **SofaScore test et** (30 dakika)
2. **FotMob test et** (30 dakika)
3. **En iyisi ile fallback implement et** (2 saat)

---

**NOT**: Şu an Sahadan %40 başarı var. Fallback ekleyerek %70-80'e çıkartabiliriz!

# Sahadan API Analiz Raporu

**Tarih:** 21.11.2026  
**Hazırlayan:** BetSmart Backend Team

---

## 📋 Özet

Sahadan.com API'si **stabil** ve **güvenilir** bir endpoint kullanıyor. API URL'si değişmiyor, sadece `date` parametresi değişiyor.

---

## ✅ API Özellikleri

### Endpoint (Sabit)
```
https://www.sahadan.com/api/index/betting-service-bulletin-soccer
```

### Parametreler (TÜM PARAMETRELERİ GEREKLİ)
```
?a=bs
&e=bsbp
&u=soccer
&application=mackolik.com
&language=tr
&country=tr
&date=YYYY-MM-DD
```

### Örnek Tam URL
```
https://www.sahadan.com/api/index/betting-service-bulletin-soccer?a=bs&e=bsbp&u=soccer&application=mackolik.com&language=tr&country=tr&date=2026-11-22
```

---

## 🧪 Test Sonuçları

### 1. Tarih Stabilitesi (5 Gün Test)
| Tarih | Status | Ligler | Maçlar | Sonuç |
|-------|--------|--------|--------|-------|
| 21.11.2026 (Bugün) | 200 OK | 353 | 688 | ✅ Çalışıyor |
| 22.11.2026 (Yarın) | 200 OK | 264 | 415 | ✅ Çalışıyor |
| 23.11.2026 (+2) | 200 OK | 65 | 72 | ✅ Çalışıyor |
| 24.11.2026 (+3) | 200 OK | 11 | 13 | ✅ Çalışıyor |
| 25.11.2026 (+4) | 200 OK | 5 | 5 | ✅ Çalışıyor |

**SONUÇ:** ✅ API tüm tarihler için çalışıyor, endpoint değişmiyor!

### 2. Endpoint Alternatifleri
| Endpoint | Status | Sonuç |
|----------|--------|-------|
| `/api/index/betting-service-bulletin-soccer` (mevcut) | 200 OK | ✅ Çalışıyor |
| `/api/iddaa-program/soccer` | 404 | ❌ Çalışmıyor |
| `/api/iddaa-program/soccer/tomorrow` | 404 | ❌ Çalışmıyor |

**SONUÇ:** ✅ Sadece mevcut endpoint çalışıyor, alternatif yok

### 3. Parametre Gereksinimleri
| Parametre Seti | Status | Sonuç |
|----------------|--------|-------|
| Tam set (tüm params) | 200 OK | ✅ Çalışıyor |
| Sadece date | 502 | ❌ Yetersiz |
| date + application | 502 | ❌ Yetersiz |
| date + language + country | 502 | ❌ Yetersiz |
| a,e,u + date | 502 | ❌ Yetersiz |
| Parametresiz | 502 | ❌ Yetersiz |

**SONUÇ:** ⚠️ TÜM PARAMETRELER ZORUNLU - eksik parametre = 502 hatası

---

## 🔒 API Güvenilirliği

### ✅ AVANTAJLAR
1. **Sabit Endpoint:** URL hiç değişmiyor, sadece date parametresi değişiyor
2. **Tahmin Edilebilir:** Tarih formatı sabit (YYYY-MM-DD)
3. **İleriye Dönük:** 5+ gün sonrasına kadar çalışıyor
4. **Tutarlı Veri:** Her tarih için doğru league time değerleri dönüyor
5. **Hızlı Yanıt:** Timeout problemi yok (~1-2 saniye)

### ⚠️ DİKKAT EDİLMESİ GEREKENLER
1. **Tüm Parametreler Zorunlu:** Eksik parametre gönderilirse 502 hatası
2. **Headers Önemli:** User-Agent ve Referer gerekli
3. **Rate Limit:** Çok hızlı istek atılırsa 403 olabilir (şimdilik görülmedi)

---

## 💡 ÖNERİLER

### Backend Kullanımı
```python
# ✅ DOĞRU KULLANIM
url = (
    f"https://www.sahadan.com/api/index/betting-service-bulletin-soccer"
    f"?a=bs"
    f"&e=bsbp"
    f"&u=soccer"
    f"&application=mackolik.com"
    f"&language=tr"
    f"&country=tr"
    f"&date={date_iso}"  # YYYY-MM-DD format
)
```

### Tarih Döngüsü
```python
# Her gün için ayrı API çağrısı
for days in range(days_ahead):
    target_date = today + timedelta(days=days)
    date_iso = target_date.strftime('%Y-%m-%d')
    
    # API çağrısı yap...
```

### Retry Mekanizması
- ✅ Mevcut: 3 retry, 2 saniye bekleme
- ✅ Timeout: 30 saniye (yeterli)
- ✅ Error handling: Var

---

## 📊 SONUÇ

### API Durumu: ✅ STABİL VE GÜVENİLİR

1. **URL değişmiyor** ✅
2. **Sadece date parametresi değişiyor** ✅  
3. **5+ gün ileriye çalışıyor** ✅
4. **Doğru time değerleri dönüyor** ✅
5. **Timeout/error sorunu yok** ✅

### Kod Değişikliği Gereği: ❌ YOK

Mevcut implementasyon doğru ve yeterli. Gelecekte API bozulma riski düşük.

---

## 🔍 Test Komutları

```bash
# API stabilite testi
python test_sahadan_api_stability.py

# Endpoint alternatifleri
python test_sahadan_api_endpoints.py

# Parametre gereksinimleri
python test_sahadan_api_params.py
```

---

**Rapor Sonu**

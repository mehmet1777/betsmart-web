'use client';

import { useState, useEffect } from 'react';
import MobileHeader from '@/components/MobileHeader';
import LeagueFilters from '@/components/LeagueFilters';
import SectionHeader from '@/components/SectionHeader';
import MatchCard from '@/components/MatchCard';
import CouponBar from '@/components/CouponBar';
import CouponSheet from '@/components/CouponSheet';
import BottomNav from '@/components/BottomNav';
import SavedCoupons from '@/components/SavedCoupons';
import Settings from '@/components/Settings';
import SmartCouponModal from '@/components/SmartCouponModal';
import NotificationDropdown from '@/components/NotificationDropdown';
import PWAInstallPrompt from '@/components/PWAInstallPrompt';
import SearchModal from '@/components/SearchModal';
import OddsAnalysisModal from '@/components/OddsAnalysisModal';
import { BetSelection, Match, getLeagueName } from '@/types';

const LEAGUE_ICONS: Record<number, string> = {
  1000001862: '⚽',
  1000001750: '⚽',
  943230: '🏆',
  943229: '🏆',
  943231: '🏆',
  1000001457: '👦',
};

export default function Home() {
  const [matches, setMatches] = useState<Match[]>([]);
  const [allMatches, setAllMatches] = useState<Match[]>([]); // Tüm maçları sakla
  const [betSlip, setBetSlip] = useState<BetSelection[]>([]);
  const [selectedLeague, setSelectedLeague] = useState<number | 'all'>('all');
  const [selectedLeagueIds, setSelectedLeagueIds] = useState<number[]>([]); // Aynı lig adına ait tüm ID'ler
  const [selectedDate, setSelectedDate] = useState<string>(() => {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  });
  const [filterMode, setFilterMode] = useState<'single' | 'popular' | 'favorites'>('single');
  const [sortBy, setSortBy] = useState<'time' | 'league' | 'recommended'>('time');
  const [activeTab, setActiveTab] = useState('home');
  const [isCouponSheetOpen, setIsCouponSheetOpen] = useState(false);
  const [isCouponMinimized, setIsCouponMinimized] = useState(false);
  const [loading, setLoading] = useState(true);
  const [isLeagueModalOpen, setIsLeagueModalOpen] = useState(false);
  const [isSmartCouponOpen, setIsSmartCouponOpen] = useState(false);
  const [isNotificationOpen, setIsNotificationOpen] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [smartRecommendations, setSmartRecommendations] = useState<any[]>([]);
  const [analyzedCount, setAnalyzedCount] = useState(0);
  const [isSearchModalOpen, setIsSearchModalOpen] = useState(false);
  const [selectedMatchForAnalysis, setSelectedMatchForAnalysis] = useState<Match | null>(null);

  useEffect(() => {
    // İlk yükleme - loader göster
    loadMatches(true);
    
    // AUTO-REFRESH KALDIRILDI - Vercel limiti için
    // Kullanıcı manuel yenileyebilir (pull-to-refresh veya yenile butonu)
    
    // Ayarlar sekmesine yönlendirme event listener
    const handleNavigateToSettings = () => {
      setActiveTab('settings');
    };
    
    // Yeniden analiz event listener (Ayarlar kaydedildiğinde)
    const handleReAnalyze = () => {
      console.log('🔄 Ayarlar değişti, yeniden analiz başlatılıyor...');
      // Cache'i temizle ve yeniden analiz tetikle
      setSmartRecommendations([]);
      setAnalyzedCount(0);
      // useEffect dependency'leri değişmediği için manuel tetikleme lazım
      // Sayfa yenilendiğinde otomatik tetiklenecek
      window.location.reload();
    };
    
    window.addEventListener('navigateToSettings', handleNavigateToSettings);
    window.addEventListener('reAnalyzeMatches', handleReAnalyze);
    
    return () => {
      window.removeEventListener('navigateToSettings', handleNavigateToSettings);
      window.removeEventListener('reAnalyzeMatches', handleReAnalyze);
    };
  }, []);

  const loadMatches = async (showLoader = true) => {
    if (showLoader) setLoading(true);
    try {
      // Cache 60 dakika - Dengeli: Vercel limiti korunur + Oranlar yeterince güncel
      const response = await fetch(`/api/matches`, {
        next: { revalidate: 3600 } // 60 dakika cache (60 × 60 = 3600 saniye)
      });
      if (response.ok) {
        const data = await response.json();
        
        // Sadece matches data'sını güncelle, scroll ve modal state'i koru
        setAllMatches(data.matches || []);
        setMatches(data.matches || []);
        console.log(`Loaded ${data.matches?.length || 0} matches, mock: ${data.mock || false}`);
      }
    } catch (error) {
      console.error('Error loading matches:', error);
    } finally {
      if (showLoader) setLoading(false);
    }
  };

  // Tarih değiştiğinde maçları filtrele VE cache'i temizle
  useEffect(() => {
    console.log(`🔍 Filtering for date: ${selectedDate}`);
    console.log(`📦 Total matches in allMatches: ${allMatches.length}`);
    
    // Tarih değişince cache'i temizle
    if (typeof window !== 'undefined') {
      localStorage.removeItem('lastAnalysisTime');
      localStorage.removeItem('cachedAnalysisResults');
      console.log('🗑️ Tarih değişti, cache temizlendi');
      
      // Önerileri sıfırla
      setSmartRecommendations([]);
      setAnalyzedCount(0);
    }
    
    const now = new Date();
    console.log(`⏰ Current time: ${now.toLocaleString('tr-TR')}`);
    
    const filtered = allMatches.filter(match => {
      // match.time formatı: "DD.MM.YYYY HH:MM"
      const matchDate = match.time.split(' ')[0]; // "DD.MM.YYYY"
      const [day, month, year] = matchDate.split('.');
      const matchDateKey = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
      
      // Tarih kontrolü
      if (matchDateKey !== selectedDate) {
        return false;
      }
      
      // Saat kontrolü - Maç saati geçmişse gizle
      try {
        const timeStr = match.time?.trim(); // Boşlukları temizle
        
        if (!timeStr) {
          console.warn('⚠️ No time:', match.time);
          return true; // Saat yoksa göster
        }
        
        const parts = timeStr.split(' ');
        if (parts.length < 2) {
          console.warn('⚠️ Invalid time format:', timeStr);
          return true;
        }
        
        const datePart = parts[0];
        const timePart = parts[1];
        
        const dateParts = datePart.split('.');
        const timeParts = timePart.split(':');
        
        if (dateParts.length !== 3 || timeParts.length !== 2) {
          console.warn('⚠️ Invalid date/time parts:', datePart, timePart);
          return true;
        }
        
        const d = parseInt(dateParts[0]);
        const m = parseInt(dateParts[1]);
        const y = parseInt(dateParts[2]);
        const h = parseInt(timeParts[0]);
        const min = parseInt(timeParts[1]);
        
        if (isNaN(d) || isNaN(m) || isNaN(y) || isNaN(h) || isNaN(min)) {
          console.warn('⚠️ Invalid numbers:', d, m, y, h, min);
          return true;
        }
        
        const matchDateTime = new Date(y, m - 1, d, h, min);
        
        // Şu andan büyükse (gelecekteyse) göster
        return matchDateTime > now;
        
      } catch (e) {
        console.error('❌ Match time parse error:', match.time, e);
        return true; // Parse hatası varsa göster (güvenli taraf)
      }
    });
    
    console.log(`✅ Filtered ${filtered.length} upcoming matches for ${selectedDate}`);
    setMatches(filtered);
  }, [selectedDate, allMatches]);

  const addToBetSlip = (selection: BetSelection) => {
    const existingIndex = betSlip.findIndex(s => s.matchId === selection.matchId);
    if (existingIndex >= 0) {
      if (betSlip[existingIndex].prediction === selection.prediction) {
        // Remove if same selection clicked again
        setBetSlip(betSlip.filter((_, i) => i !== existingIndex));
      } else {
        // Update selection
        const newSlip = [...betSlip];
        newSlip[existingIndex] = selection;
        setBetSlip(newSlip);
      }
    } else {
      setBetSlip([...betSlip, selection]);
    }
  };

  const removeFromBetSlip = (matchId: number) => {
    setBetSlip(betSlip.filter(s => s.matchId !== matchId));
  };

  const clearBetSlip = () => {
    setBetSlip([]);
    setIsCouponSheetOpen(false);
    setIsCouponMinimized(false);
  };

  const handleMinimizeCoupon = () => {
    setIsCouponSheetOpen(false);
    setIsCouponMinimized(true);
  };

  const handleExpandCoupon = () => {
    setIsCouponMinimized(false);
    setIsCouponSheetOpen(true);
  };

  const handleSmartCouponAdd = (recommendations: any[]) => {
    console.log('🎯 handleSmartCouponAdd çağrıldı, öneri sayısı:', recommendations.length);
    console.log('📊 Öneriler:', recommendations.map(r => ({ type: r.recommendation, odds: r.recommended_odds })));
    
    // Akıllı kupon önerilerini bet slip'e ekle
    const newSelections: BetSelection[] = recommendations.map(rec => {
      // Önce mevcut matches array'inde ara
      let match = matches.find(m => m.id === rec.match.id);
      
      // Bulamazsa (farklı gün seçiliyse), allMatches'ten ara
      if (!match) {
        match = allMatches.find(m => m.id === rec.match.id);
      }
      
      // Hala bulamazsa, recommendation'daki match'i kullan
      if (!match) {
        console.warn('⚠️ Maç matches/allMatches\'te bulunamadı, recommendation\'daki match kullanılıyor:', rec.match.id);
        match = rec.match;
      }

      // Öneri tipine göre prediction belirle
      let prediction = '1'; // varsayılan
      
      // Maç Sonucu
      if (rec.recommendation === 'MS1') prediction = '1';
      else if (rec.recommendation === 'MSX') prediction = 'X';
      else if (rec.recommendation === 'MS2') prediction = '2';
      // Karşılıklı Gol
      else if (rec.recommendation === 'GG_YES') prediction = 'GG';
      else if (rec.recommendation === 'GG_NO') prediction = 'GG_NO';
      // Alt/Üst
      else if (rec.recommendation === 'OVER_25') prediction = 'OVER_25';
      else if (rec.recommendation === 'UNDER_25') prediction = 'UNDER_25';
      else if (rec.recommendation === 'OVER_35') prediction = 'OVER_35';
      else if (rec.recommendation === 'UNDER_35') prediction = 'UNDER_35';
      // İlk Yarı
      else if (rec.recommendation === 'HT_OVER_05') prediction = 'HT_OVER_05';
      else if (rec.recommendation === 'HT_UNDER_05') prediction = 'HT_UNDER_05';
      else if (rec.recommendation === 'HT_OVER_15') prediction = 'HT_OVER_15';
      else if (rec.recommendation === 'HT_UNDER_15') prediction = 'HT_UNDER_15';
      else if (rec.recommendation === 'HT_GG_YES') prediction = 'HT_GG_YES';
      else if (rec.recommendation === 'HT_GG_NO') prediction = 'HT_GG_NO';

      // Match yoksa null dön (filter ile temizlenecek)
      if (!match) {
        console.error('❌ Match bulunamadı ve oluşturulamadı:', rec.match);
        return null;
      }

      return {
        matchId: match.id,
        match: match,
        prediction: prediction,
        customOdds: rec.recommended_odds // Özel oran bilgisini ekle
      };
    }).filter(Boolean) as BetSelection[];

    console.log('✅ Kupona eklenecek maçlar:', newSelections.length);
    
    // Önce kuponu doldur
    setBetSlip(newSelections);
    
    // Kısa bir gecikme ile kupon sheet'i aç (state update için)
    setTimeout(() => {
      console.log('📋 Kupon Sheet açılıyor...');
      setIsCouponSheetOpen(true);
    }, 100);
  };

  const filteredMatches = selectedLeague === 'all' 
    ? matches 
    : filterMode === 'popular'
    ? matches.filter(m => {
        // Popüler ligleri kontrol et
        const POPULAR_LEAGUES = [
          "TÜRKİYE Süper Lig",
          "İNGİLTERE Premier Lig",
          "İSPANYA LaLiga",
          "İTALYA Serie A",
          "ALMANYA Bundesliga",
          "FRANSA Ligue 1",
          "PORTEKİZ Premier Lig",
          "HOLLANDA Eredivisie",
          "UEFA ŞAMPİYONLAR LİGİ Lig Aşaması",
          "UEFA AVRUPA LİGİ Lig Aşaması",
          "UEFA KONFERANS LİGİ Lig Aşaması",
          "BREZİLYA Serie A",
          "ARJANTİN Ulusal Primera Lig",
          "JAPONYA J1 Lig",
          "GÜNEY KORE K Lig 1",
          "ABD MLS",
          "MEKSİKA Liga MX Apertura",
          "İNGİLTERE Championship",
          "İSPANYA 2.Lig",
          "ALMANYA 2. Bundesliga",
        ];
        const isPopular = POPULAR_LEAGUES.includes(m.leagueName || '');
        if (isPopular) {
          console.log('✅ Popüler lig bulundu:', m.leagueName, m.home.name, 'vs', m.away.name);
        }
        return isPopular;
      })
    : filterMode === 'favorites'
    ? matches.filter(m => {
        // Favorileri localStorage'dan al
        if (typeof window !== 'undefined') {
          const stored = localStorage.getItem('favoriteLeagues');
          if (stored) {
            const favorites = JSON.parse(stored);
            return favorites.includes(m.leagueName);
          }
        }
        return false;
      })
    : matches.filter(m => {
        // Eğer selectedLeagueIds varsa, onları kullan (aynı lig adına sahip tüm ID'ler)
        // Yoksa sadece selectedLeague'yi kullan (geriye dönük uyumluluk)
        if (selectedLeagueIds.length > 0) {
          return selectedLeagueIds.includes(m.leagueId);
        }
        return m.leagueId === selectedLeague;
      });

  // Otomatik analiz - tarih veya maçlar değiştiğinde
  useEffect(() => {
    const analyzeInBackground = async () => {
      if (filteredMatches.length === 0 || analyzing) return;

      // Kullanıcının tolerans ayarını al
      const smartCouponTolerance = typeof window !== 'undefined'
        ? parseFloat(localStorage.getItem('smartCouponTolerance') || '0.05')
        : 0.05;

      // Cache key: Tarih + Tolerans bazlı
      const cacheKey = `smartAnalysis_${selectedDate}_${smartCouponTolerance}`;
      
      // Cache kontrolü - 90 dakika (backend ile senkron)
      const CACHE_DURATION = 90 * 60 * 1000; // 90 dakika
      const now = Date.now();
      
      if (typeof window !== 'undefined') {
        const cachedData = localStorage.getItem(cacheKey);
        const lastAnalysisTime = localStorage.getItem(`${cacheKey}_time`);
        
        // Cache varsa ve 90 dakika geçmemişse, cache'den yükle
        if (lastAnalysisTime && cachedData) {
          const elapsed = now - parseInt(lastAnalysisTime);
          
          if (elapsed < CACHE_DURATION) {
            console.log(`♻️ Cache'den yükleniyor: ${selectedDate} (Tolerans: ±${smartCouponTolerance}) - ${Math.round(elapsed / 1000 / 60)} dakika önce`);
            
            try {
              const cached = JSON.parse(cachedData);
              setSmartRecommendations(cached.recommendations || []);
              setAnalyzedCount(cached.analyzed_count || 0);
              
              // Öneri varsa bildirim göster
              if (cached.recommendations?.length > 0 && !isNotificationOpen) {
                setIsNotificationOpen(true);
              }
              
              return; // Cache'den yüklendi, analiz yapma
            } catch (e) {
              console.warn('⚠️ Cache parse hatası, yeniden analiz yapılıyor');
            }
          } else {
            console.log(`🔄 Cache süresi doldu (${Math.round(elapsed / 1000 / 60)} dakika), yeniden analiz ediliyor`);
          }
        }
      }

      // Cache yoksa veya süresi dolmuşsa, yeni analiz yap
      setAnalyzing(true);
      console.log('🤖 Yeni analiz başlatılıyor:', filteredMatches.length, 'maç (Tolerans: ±' + smartCouponTolerance + ')');

      try {
        const matchData = filteredMatches.map(m => ({
          id: m.id,
          home_team: m.home.name,
          away_team: m.away.name,
          odd_1: parseFloat(m.odds?.home || '0'),
          odd_x: parseFloat(m.odds?.draw || '0'),
          odd_2: parseFloat(m.odds?.away || '0'),
          league: m.leagueName,
          time: m.time
        }));

        console.log(`🎚️ Kupon toleransı: ±${smartCouponTolerance}`);

        const response = await fetch('/api/smart-coupon', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            matches: matchData,
            smartCouponTolerance 
          })
        });

        if (response.ok) {
          const data = await response.json();
          console.log('✅ Analiz tamamlandı:', data.recommended_count, 'öneri');
          
          setSmartRecommendations(data.recommendations || []);
          setAnalyzedCount(data.analyzed_count || 0);

          // Cache'e kaydet (Tarih + Tolerans bazlı)
          if (typeof window !== 'undefined') {
            localStorage.setItem(cacheKey, JSON.stringify({
              recommendations: data.recommendations,
              analyzed_count: data.analyzed_count,
              timestamp: now
            }));
            localStorage.setItem(`${cacheKey}_time`, now.toString());
            console.log(`💾 Cache kaydedildi: ${cacheKey} (90 dakika)`);
          }

          // Eğer öneri varsa ve bildirim açık değilse, otomatik aç
          if (data.recommended_count > 0 && !isNotificationOpen) {
            setIsNotificationOpen(true);
          }
        }
      } catch (error) {
        console.error('❌ Analiz hatası:', error);
      } finally {
        setAnalyzing(false);
      }
    };

    // Debounce: 1 saniye bekle, sonra analiz et (veya cache'den yükle)
    const timer = setTimeout(() => {
      analyzeInBackground();
    }, 1000);

    return () => clearTimeout(timer);
  }, [selectedDate, filteredMatches.length]);
  
  console.log('🔍 Filter mode:', filterMode);
  console.log('📊 Total matches:', matches.length);
  console.log('✅ Filtered matches:', filteredMatches.length);

  // Canlı maçları filtrele (activeTab === 'live' ise)
  const displayMatches = activeTab === 'live'
    ? filteredMatches.filter(m => m.status.started && !m.status.finished)
    : filteredMatches.filter(m => {
        // Frontend'de maçın başlayıp başlamadığını kontrol et
        try {
          const [datePart, timePart] = m.time.split(' ');
          const [day, month, year] = datePart.split('.');
          const [hour, minute] = timePart.split(':');
          const matchDateTime = new Date(
            parseInt(year),
            parseInt(month) - 1,
            parseInt(day),
            parseInt(hour),
            parseInt(minute)
          );
          const now = new Date();
          // Maç henüz başlamamışsa göster (gelecekteki maçlar)
          return matchDateTime > now;
        } catch (e) {
          // Parse hatası varsa API'nin status'unu kullan
          return !m.status.started;
        }
      });

  // Maçları akıllı sırala: 1) Önerilen önce (eğer seçiliyse), 2) Canlı olanlar önce, 3) Saate göre
  const sortedMatches = [...displayMatches].sort((a, b) => {
    // Eğer "Önerilen Önce" seçiliyse
    if (sortBy === 'recommended') {
      const aRecommended = smartRecommendations.some(r => r.match.id === a.id);
      const bRecommended = smartRecommendations.some(r => r.match.id === b.id);
      
      if (aRecommended && !bRecommended) return -1;
      if (!aRecommended && bRecommended) return 1;
      
      // İkisi de önerilen veya değilse, başarı oranına göre sırala
      if (aRecommended && bRecommended) {
        const aRate = smartRecommendations.find(r => r.match.id === a.id)?.win_rate || 0;
        const bRate = smartRecommendations.find(r => r.match.id === b.id)?.win_rate || 0;
        return bRate - aRate; // Yüksekten düşüğe
      }
    }

    // Canlı maçlar önce
    const aLive = a.status.started && !a.status.finished;
    const bLive = b.status.started && !b.status.finished;
    
    if (aLive && !bLive) return -1;
    if (!aLive && bLive) return 1;
    
    // Tarih-saat karşılaştırması
    // time formatı: "DD.MM.YYYY HH:MM"
    const parseDateTime = (timeStr: string) => {
      const [datePart, timePart] = timeStr.split(' ');
      const [day, month, year] = datePart.split('.');
      const [hour, minute] = timePart.split(':');
      return new Date(
        parseInt(year),
        parseInt(month) - 1,
        parseInt(day),
        parseInt(hour),
        parseInt(minute)
      ).getTime();
    };
    
    const aTime = parseDateTime(a.time);
    const bTime = parseDateTime(b.time);
    
    return aTime - bTime; // Eskiden yeniye
  });

  const uniqueLeagues = Array.from(new Set(matches.map(m => m.leagueId)));

  const totalOdds = betSlip.reduce((acc, selection) => {
    // Önce customOdds varsa onu kullan (akıllı kupondan gelen alternatifler)
    if (selection.customOdds) {
      return acc * selection.customOdds;
    }

    // Gerçek oranları match objesinden al (sadece MS1/MSX/MS2 için)
    let oddValue = 0;
    if (selection.prediction === '1') {
      oddValue = parseFloat(selection.match.odds?.home || '0');
    } else if (selection.prediction === 'X') {
      oddValue = parseFloat(selection.match.odds?.draw || '0');
    } else if (selection.prediction === '2') {
      oddValue = parseFloat(selection.match.odds?.away || '0');
    }
    
    return acc * (oddValue || 1);
  }, 1);

  // Group matches by league
  const groupedMatches = sortedMatches.reduce((acc, match) => {
    if (!acc[match.leagueId]) {
      acc[match.leagueId] = [];
    }
    acc[match.leagueId].push(match);
    return acc;
  }, {} as Record<number, Match[]>);

  // Her lig grubunu kendi içinde de sırala
  Object.keys(groupedMatches).forEach(leagueId => {
    groupedMatches[Number(leagueId)].sort((a, b) => {
      // Canlı maçlar önce
      const aLive = a.status.started && !a.status.finished;
      const bLive = b.status.started && !b.status.finished;
      
      if (aLive && !bLive) return -1;
      if (!aLive && bLive) return 1;
      
      // Tarih-saat karşılaştırması
      const parseDateTime = (timeStr: string) => {
        const [datePart, timePart] = timeStr.split(' ');
        const [day, month, year] = datePart.split('.');
        const [hour, minute] = timePart.split(':');
        return new Date(
          parseInt(year),
          parseInt(month) - 1,
          parseInt(day),
          parseInt(hour),
          parseInt(minute)
        ).getTime();
      };
      
      return parseDateTime(a.time) - parseDateTime(b.time);
    });
  });

  return (
    <div className="min-h-screen bg-bg-app pb-32">
      {/* PWA Install Prompt - Premium 2026 Experience */}
      <PWAInstallPrompt />

      {/* Mobile Header */}
      <div className="relative">
        <MobileHeader 
          onNotificationClick={() => setIsNotificationOpen(!isNotificationOpen)}
          onSearchClick={() => setIsSearchModalOpen(true)}
          notificationCount={smartRecommendations.length}
        />
        
        {/* Subtle Loading Bar */}
        {analyzing && (
          <div className="fixed top-[60px] left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-[#8B5CF6] to-transparent z-50 animate-pulse">
            <div className="h-full bg-[#8B5CF6] animate-[shimmer_1.5s_ease-in-out_infinite]" 
                 style={{
                   background: 'linear-gradient(90deg, transparent 0%, #8B5CF6 50%, transparent 100%)',
                   backgroundSize: '200% 100%',
                   animation: 'shimmer 1.5s ease-in-out infinite'
                 }}
            />
          </div>
        )}
        
        {/* Notification Dropdown */}
        <div className="fixed top-14 right-4 z-50">
          <NotificationDropdown
            isOpen={isNotificationOpen}
            totalMatches={filteredMatches.length}
            recommendedCount={smartRecommendations.length}
            selectedDate={selectedDate}
            onViewRecommendations={() => {
              setIsNotificationOpen(false);
              setIsSmartCouponOpen(true);
            }}
            onClose={() => setIsNotificationOpen(false)}
          />

          {/* Search Modal */}
          <SearchModal
            isOpen={isSearchModalOpen}
            onClose={() => setIsSearchModalOpen(false)}
            matches={matches}
            onAnalyze={(match) => setSelectedMatchForAnalysis(match)}
          />

          {/* Analysis Modal from Search */}
          {selectedMatchForAnalysis && (
            <OddsAnalysisModal
              isOpen={true}
              match={selectedMatchForAnalysis}
              onClose={() => setSelectedMatchForAnalysis(null)}
            />
          )}
        </div>
      </div>

      {/* Sidebar - Kaldırıldı */}

      {/* Smart Coupon Modal */}
      <SmartCouponModal
        isOpen={isSmartCouponOpen}
        onClose={() => setIsSmartCouponOpen(false)}
        recommendations={smartRecommendations}
        analyzedCount={analyzedCount}
        onAddToCoupon={handleSmartCouponAdd}
      />

      {/* Kuponlarım Sekmesi */}
      {activeTab === 'coupons' ? (
        <SavedCoupons />
      ) : activeTab === 'settings' ? (
        <Settings />
      ) : (
        <>
          {/* Main Content */}
          <main className="pt-16">{/* Normal padding */}
            {/* League Filters */}
            <LeagueFilters
          selectedLeague={selectedLeague}
          onSelectLeague={(leagueId, leagueIds) => {
            setSelectedLeague(leagueId);
            setSelectedLeagueIds(leagueIds || []); // Aynı lig adına sahip tüm ID'leri sakla
            setFilterMode('single');
          }}
          leagues={uniqueLeagues}
          matches={matches}
          onModalStateChange={setIsLeagueModalOpen}
          onFilterModeChange={setFilterMode}
        />

        {/* Section Header with Date Selector */}
        <SectionHeader 
          title={activeTab === 'live' ? 'Canlı Maçlar' : 'Günün Maçları'} 
          matchCount={displayMatches.length}
          selectedDate={selectedDate}
          onDateChange={setSelectedDate}
          sortBy={sortBy}
          onSortChange={setSortBy}
          matches={allMatches}
        />

        {/* Matches */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-2 border-accent-primary border-t-transparent"></div>
          </div>
        ) : sortBy === 'time' || sortBy === 'recommended' ? (
          // Saate göre veya önerilen önce sıralama - lig ayrımı yok
          <div className="pb-4">
            {sortedMatches.map(match => {
              const selection = betSlip.find(s => s.matchId === match.id);
              
              // Önerilen maç mı kontrol et
              const recommendation = smartRecommendations.find(r => r.match.id === match.id);
              const isRecommended = !!recommendation;
              const recommendedWinRate = recommendation?.win_rate;
              
              // Akıllı canlı tespiti: API'den gelen status VEYA saat kontrolü
              let isLive = match.status.started && !match.status.finished;
              
              // Eğer API status yanlışsa, saat bazlı kontrol yap
              if (!isLive && !match.status.finished) {
                const now = new Date();
                const parseDateTime = (timeStr: string) => {
                  const [datePart, timePart] = timeStr.split(' ');
                  const [day, month, year] = datePart.split('.');
                  const [hour, minute] = timePart.split(':');
                  return new Date(
                    parseInt(year),
                    parseInt(month) - 1,
                    parseInt(day),
                    parseInt(hour),
                    parseInt(minute)
                  );
                };
                
                const matchTime = parseDateTime(match.time);
                const diffMinutes = (now.getTime() - matchTime.getTime()) / (1000 * 60);
                
                // Maç saatinden sonra 0-120 dakika arasındaysa (2 saat), muhtemelen canlı
                if (diffMinutes > 0 && diffMinutes < 120) {
                  isLive = true;
                }
              }
              
              return (
                <MatchCard
                  key={match.id}
                  match={match}
                  leagueName={getLeagueName(match.leagueId, match.leagueName)}
                  leagueIcon={LEAGUE_ICONS[match.leagueId]}
                  onSelect={addToBetSlip}
                  selectedPrediction={selection?.prediction}
                  isLive={isLive}
                  isRecommended={isRecommended}
                  recommendedWinRate={recommendedWinRate}
                  recommendation={recommendation}
                />
              );
            })}
          </div>
        ) : (
          // Lige göre sıralama - gruplu
          <div className="pb-4">
            {Object.entries(groupedMatches).map(([leagueId, leagueMatches]) => (
              <div key={leagueId}>
                {leagueMatches.map(match => {
                  const selection = betSlip.find(s => s.matchId === match.id);
                  
                  // Önerilen maç mı kontrol et
                  const recommendation = smartRecommendations.find(r => r.match.id === match.id);
                  const isRecommended = !!recommendation;
                  const recommendedWinRate = recommendation?.win_rate;
                  
                  // Akıllı canlı tespiti: API'den gelen status VEYA saat kontrolü
                  let isLive = match.status.started && !match.status.finished;
                  
                  // Eğer API status yanlışsa, saat bazlı kontrol yap
                  if (!isLive && !match.status.finished) {
                    const now = new Date();
                    const parseDateTime = (timeStr: string) => {
                      const [datePart, timePart] = timeStr.split(' ');
                      const [day, month, year] = datePart.split('.');
                      const [hour, minute] = timePart.split(':');
                      return new Date(
                        parseInt(year),
                        parseInt(month) - 1,
                        parseInt(day),
                        parseInt(hour),
                        parseInt(minute)
                      );
                    };
                    
                    const matchTime = parseDateTime(match.time);
                    const diffMinutes = (now.getTime() - matchTime.getTime()) / (1000 * 60);
                    
                    // Maç saatinden sonra 0-120 dakika arasındaysa (2 saat), muhtemelen canlı
                    if (diffMinutes > 0 && diffMinutes < 120) {
                      isLive = true;
                    }
                  }
                  
                  return (
                    <MatchCard
                      key={match.id}
                      match={match}
                      leagueName={getLeagueName(match.leagueId, match.leagueName)}
                      leagueIcon={LEAGUE_ICONS[match.leagueId]}
                      onSelect={addToBetSlip}
                      selectedPrediction={selection?.prediction}
                      isLive={isLive}
                      isRecommended={isRecommended}
                      recommendedWinRate={recommendedWinRate}
                      recommendation={recommendation}
                    />
                  );
                })}
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Coupon Bar */}
      {betSlip.length > 0 && (
        <CouponBar
          selectionCount={betSlip.length}
          totalOdds={totalOdds}
          onOpenCoupon={() => setIsCouponSheetOpen(true)}
        />
      )}

      {/* Coupon Detail Sheet */}
      <CouponSheet
        isOpen={isCouponSheetOpen}
        onClose={() => setIsCouponSheetOpen(false)}
        selections={betSlip}
        totalOdds={totalOdds}
        onRemove={removeFromBetSlip}
        onClear={clearBetSlip}
        onMinimize={handleMinimizeCoupon}
        onExpand={handleExpandCoupon}
      />
      </>
      )}

      {/* Bottom Navigation */}
      {!isLeagueModalOpen && !isSmartCouponOpen && <BottomNav activeTab={activeTab} onTabChange={setActiveTab} />}
    </div>
  );
}

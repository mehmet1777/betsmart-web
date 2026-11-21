'use client';

import { useState, useEffect } from 'react';
import MobileHeader from '@/components/MobileHeader';
import LeagueFilters from '@/components/LeagueFilters';
import SectionHeader from '@/components/SectionHeader';
import MatchCard from '@/components/MatchCard';
import CouponBar from '@/components/CouponBar';
import CouponSheet from '@/components/CouponSheet';
import BottomNav from '@/components/BottomNav';
import Sidebar from '@/components/Sidebar';
import SavedCoupons from '@/components/SavedCoupons';
import SmartCouponModal from '@/components/SmartCouponModal';
import NotificationDropdown from '@/components/NotificationDropdown';
import PWAInstallPrompt from '@/components/PWAInstallPrompt';
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
  const [sortBy, setSortBy] = useState<'time' | 'league'>('league');
  const [activeTab, setActiveTab] = useState('home');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isCouponSheetOpen, setIsCouponSheetOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [isLeagueModalOpen, setIsLeagueModalOpen] = useState(false);
  const [isSmartCouponOpen, setIsSmartCouponOpen] = useState(false);
  const [isNotificationOpen, setIsNotificationOpen] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [smartRecommendations, setSmartRecommendations] = useState<any[]>([]);
  const [analyzedCount, setAnalyzedCount] = useState(0);

  useEffect(() => {
    loadMatches();
  }, []);

  const loadMatches = async () => {
    setLoading(true);
    try {
      // Cache bypass için timestamp ekle
      const response = await fetch(`/api/matches?t=${Date.now()}`);
      if (response.ok) {
        const data = await response.json();
        setAllMatches(data.matches || []);
        setMatches(data.matches || []);
        console.log(`Loaded ${data.matches?.length || 0} matches, mock: ${data.mock || false}`);
      }
    } catch (error) {
      console.error('Error loading matches:', error);
    } finally {
      setLoading(false);
    }
  };

  // Tarih değiştiğinde maçları filtrele
  useEffect(() => {
    console.log(`🔍 Filtering for date: ${selectedDate}`);
    console.log(`📦 Total matches in allMatches: ${allMatches.length}`);
    
    // İlk 5 maçın tarihlerini debug için yazdır
    if (allMatches.length > 0) {
      console.log('🔎 Sample match dates:');
      allMatches.slice(0, 5).forEach(m => {
        const matchDate = m.time.split(' ')[0];
        const [day, month, year] = matchDate.split('.');
        const matchDateKey = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
        console.log(`  ${m.home.name} vs ${m.away.name}: ${m.time} -> ${matchDateKey}`);
      });
    }
    
    const now = new Date();
    
    const filtered = allMatches.filter(match => {
      // match.time formatı: "DD.MM.YYYY HH:MM"
      const matchDate = match.time.split(' ')[0]; // "DD.MM.YYYY"
      const [day, month, year] = matchDate.split('.');
      const matchDateKey = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
      
      // Tarih kontrolü
      const isMatchingDate = matchDateKey === selectedDate;
      
      if (!isMatchingDate) return false;
      
      // Saat kontrolü - 2 saatten eski maçları gizle
      try {
        const [datePart, timePart] = match.time.split(' ');
        const [d, m, y] = datePart.split('.');
        const [h, min] = timePart.split(':');
        const matchDateTime = new Date(parseInt(y), parseInt(m) - 1, parseInt(d), parseInt(h), parseInt(min));
        
        const hoursDiff = (now.getTime() - matchDateTime.getTime()) / (1000 * 60 * 60);
        
        // 2 saatten eski maçları gizle
        if (hoursDiff > 2) {
          return false;
        }
      } catch (e) {
        // Parse hatası varsa göster
      }
      
      return true;
    });
    
    console.log(`✅ Filtered ${filtered.length} matches for ${selectedDate}`);
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
  };

  const handleSmartCouponAdd = (recommendations: any[]) => {
    console.log('🎯 handleSmartCouponAdd çağrıldı, öneri sayısı:', recommendations.length);
    
    // Akıllı kupon önerilerini bet slip'e ekle
    const newSelections: BetSelection[] = recommendations.map(rec => {
      // Maç objesini matches array'inden bul
      const match = matches.find(m => m.id === rec.match.id);
      
      if (!match) {
        console.warn('⚠️ Maç bulunamadı:', rec.match.id);
        return null;
      }

      return {
        matchId: match.id,
        match: match,
        prediction: rec.recommendation === 'MS1' ? '1' : rec.recommendation === 'MSX' ? 'X' : '2'
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

      setAnalyzing(true);
      console.log('🤖 Arka planda analiz başlatılıyor:', filteredMatches.length, 'maç');

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

        const response = await fetch('/api/smart-coupon', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ matches: matchData })
        });

        if (response.ok) {
          const data = await response.json();
          console.log('✅ Arka plan analizi tamamlandı:', data.recommended_count, 'öneri');
          
          setSmartRecommendations(data.recommendations || []);
          setAnalyzedCount(data.analyzed_count || 0);

          // Eğer öneri varsa ve bildirim açık değilse, otomatik aç
          if (data.recommended_count > 0 && !isNotificationOpen) {
            setIsNotificationOpen(true);
          }
        }
      } catch (error) {
        console.error('❌ Arka plan analiz hatası:', error);
      } finally {
        setAnalyzing(false);
      }
    };

    // Debounce: 1 saniye bekle, sonra analiz et
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
    : filteredMatches;

  // Maçları akıllı sırala: 1) Canlı olanlar önce, 2) Saate göre yakın olanlar
  const sortedMatches = [...displayMatches].sort((a, b) => {
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
    // Gerçek oranları match objesinden al
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
          onMenuClick={() => setIsSidebarOpen(true)}
          onNotificationClick={() => setIsNotificationOpen(!isNotificationOpen)}
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
        </div>
      </div>

      {/* Sidebar */}
      <Sidebar 
        isMobileOpen={isSidebarOpen}
        onMobileClose={() => setIsSidebarOpen(false)}
      />

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
      ) : (
        <>
          {/* Main Content */}
          <main className="pt-16">
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
        ) : sortBy === 'time' ? (
          // Saate göre sıralama - lig ayrımı yok
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
      />
      </>
      )}

      {/* Bottom Navigation */}
      {!isLeagueModalOpen && !isSmartCouponOpen && <BottomNav activeTab={activeTab} onTabChange={setActiveTab} />}
    </div>
  );
}

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
    
    const filtered = allMatches.filter(match => {
      // match.time formatı: "DD.MM.YYYY HH:MM"
      const matchDate = match.time.split(' ')[0]; // "DD.MM.YYYY"
      const [day, month, year] = matchDate.split('.');
      const matchDateKey = `${year}-${month}-${day}`;
      
      const isMatch = matchDateKey === selectedDate;
      if (isMatch) {
        console.log(`✅ Match found: ${match.home.name} vs ${match.away.name} at ${match.time}`);
      }
      
      return isMatch;
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
    : matches.filter(m => m.leagueId === selectedLeague);
  
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
      {/* Mobile Header */}
      <MobileHeader onMenuClick={() => setIsSidebarOpen(true)} />

      {/* Sidebar */}
      <Sidebar 
        isMobileOpen={isSidebarOpen}
        onMobileClose={() => setIsSidebarOpen(false)}
      />

      {/* Main Content */}
      <main className="pt-16">
        {/* League Filters */}
        <LeagueFilters
          selectedLeague={selectedLeague}
          onSelectLeague={(leagueId) => {
            setSelectedLeague(leagueId);
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

      {/* Bottom Navigation */}
      {!isLeagueModalOpen && <BottomNav activeTab={activeTab} onTabChange={setActiveTab} />}
    </div>
  );
}

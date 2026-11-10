'use client';

import { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';
import { getLeagueName } from '@/types';
import AllLeaguesModal from './AllLeaguesModal';
import FavoritesPopup from './FavoritesPopup';
import PopularPopup from './PopularPopup';
import { POPULAR_LEAGUES } from '@/config/leagues';

interface LeagueFiltersProps {
  selectedLeague: number | 'all';
  onSelectLeague: (leagueId: number | 'all') => void;
  leagues: number[];
  matches?: any[];  // Match objeleri - gerçek lig kodları için
  onModalStateChange?: (isOpen: boolean) => void;
  onFilterModeChange?: (mode: 'single' | 'popular' | 'favorites') => void;
}

// Majör ligler - öncelikli sıralama
const MAJOR_LEAGUES = [
  1000001862, // 🇹🇷 Süper Lig
  943230,     // 🏆 Şampiyonlar Ligi
  943229,     // 🏆 Avrupa Ligi
  8,          // 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier Lig
  87,         // 🇪🇸 La Liga
  135,        // 🇮🇹 Serie A
  35,         // 🇩🇪 Bundesliga
  34,         // 🇫🇷 Ligue 1
  63,         // 🇵🇹 Portekiz Ligi
  37,         // 🇳🇱 Hollanda Ligi
];

function extractFlag(leagueName: string): string {
  // Bayrak veya emoji çıkar (ilk 2 karakter genelde emoji)
  const match = leagueName.match(/^([\u{1F1E6}-\u{1F1FF}]{2}|[\u{1F3C6}\u{26BD}\u{1F451}\u{1F476}])/u);
  return match ? match[0] : '⚽';
}

function extractName(leagueName: string): string {
  // Emoji ve boşlukları temizle, sadece lig ismini al
  return leagueName
    .replace(/^[\u{1F1E6}-\u{1F1FF}]{2}\s*/u, '')  // Bayrak kaldır
    .replace(/^[\u{1F3C6}\u{26BD}\u{1F451}\u{1F476}]\s*/u, '') // Diğer emojiler
    .trim();
}

export default function LeagueFilters({ selectedLeague, onSelectLeague, leagues, matches = [], onModalStateChange, onFilterModeChange }: LeagueFiltersProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalInitialTab, setModalInitialTab] = useState<'all' | 'selected' | 'favorites' | 'popular'>('all');
  const [isFavoritesOpen, setIsFavoritesOpen] = useState(false);
  const [isPopularOpen, setIsPopularOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const favoritesButtonRef = useRef<HTMLButtonElement>(null);
  const popularButtonRef = useRef<HTMLButtonElement>(null);

  // Dışarı tıklandığında kapat
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Ligleri sırala: önce majör ligler, sonra diğerleri
  const sortedLeagues = [...leagues].sort((a, b) => {
    const aIndex = MAJOR_LEAGUES.indexOf(a);
    const bIndex = MAJOR_LEAGUES.indexOf(b);
    
    // Her ikisi de majör ligde
    if (aIndex !== -1 && bIndex !== -1) {
      return aIndex - bIndex;
    }
    
    // Sadece a majör ligde
    if (aIndex !== -1) return -1;
    
    // Sadece b majör ligde
    if (bIndex !== -1) return 1;
    
    // Her ikisi de majör değil - ID'ye göre sırala
    return a - b;
  });

  const getSelectedLeagueName = () => {
    if (selectedLeague === 'all') return 'Tümü';
    
    // Matches array'inden gerçek lig kodunu bul
    const match = matches.find(m => m.leagueId === selectedLeague);
    if (match && match.leagueName) {
      return match.leagueName; // Mackolik'ten gelen kod (PRD, COC, J-C)
    }
    
    const fullName = getLeagueName(selectedLeague);
    return extractName(fullName);
  };

  const getSelectedLeagueFlag = () => {
    if (selectedLeague === 'all') return '⚽';
    
    const fullName = getLeagueName(selectedLeague);
    return extractFlag(fullName);
  };

  const getLeagueDisplayName = (leagueId: number) => {
    // Matches array'inden gerçek lig kodunu bul
    const match = matches.find(m => m.leagueId === leagueId);
    if (match && match.leagueName) {
      return match.leagueName; // Mackolik'ten gelen kod (PRD, COC, J-C)
    }
    
    const fullName = getLeagueName(leagueId);
    return extractName(fullName);
  };

  const handleSelect = (leagueId: number | 'all') => {
    onSelectLeague(leagueId);
    setIsOpen(false);
  };

  return (
    <div className="px-4 py-3 relative" ref={dropdownRef}>
      <div className="grid grid-cols-4 gap-2">
        {/* Dropdown Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center justify-center gap-1.5 px-2 py-2.5 bg-bg-elevated border-2 border-accent-primary/30 rounded-xl hover:border-accent-primary transition-all"
        >
          <span className="text-base">⚽</span>
          <span className="text-text-primary font-bold text-xs">Ligler</span>
          <ChevronDown className={`w-3 h-3 text-text-secondary transition-transform ${isOpen ? 'rotate-180' : ''}`} />
        </button>

        {/* Favoriler */}
        <button 
          ref={favoritesButtonRef}
          onClick={() => {
            setIsOpen(false);
            setIsPopularOpen(false);
            setIsFavoritesOpen(!isFavoritesOpen);
            // Favorilere geç
            if (!isFavoritesOpen) {
              onFilterModeChange?.('favorites');
            }
          }}
          className="flex items-center justify-center gap-1.5 px-2 py-2.5 bg-bg-elevated border border-border-color rounded-xl hover:border-accent-primary transition-all"
        >
          <span className="text-base">⭐</span>
          <span className="text-text-secondary font-semibold text-xs">Favoriler</span>
        </button>

        {/* Popüler */}
        <button 
          ref={popularButtonRef}
          onClick={() => {
            setIsOpen(false);
            setIsFavoritesOpen(false);
            setIsPopularOpen(!isPopularOpen);
            // Popülere geç
            if (!isPopularOpen) {
              onFilterModeChange?.('popular');
            }
          }}
          className="flex items-center justify-center gap-1.5 px-2 py-2.5 bg-bg-elevated border border-border-color rounded-xl hover:border-accent-primary transition-all"
        >
          <span className="text-base">🔥</span>
          <span className="text-text-secondary font-semibold text-xs">Popüler</span>
        </button>

        {/* Diğer */}
        <button className="flex items-center justify-center gap-1.5 px-2 py-2.5 bg-bg-elevated border border-border-color rounded-xl hover:border-accent-primary transition-all">
          <span className="text-base">🌍</span>
          <span className="text-text-secondary font-semibold text-xs">Diğer</span>
        </button>
      </div>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute top-full left-4 mt-2 w-72 bg-bg-elevated border border-border-color rounded-2xl shadow-2xl z-50 overflow-hidden">
          {/* Tümü - Seçili lig gösterimi */}
          <div className="px-4 py-3 border-b border-border-color bg-bg-card">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-accent-primary/10 rounded-lg flex items-center justify-center border border-accent-primary/30">
                <span className="text-lg">{getSelectedLeagueFlag()}</span>
              </div>
              <div>
                <div className="text-xs text-text-muted">Seçili Lig</div>
                <div className="text-sm font-bold text-text-primary">{getSelectedLeagueName()}</div>
              </div>
            </div>
          </div>

          {/* Liste */}
          <div className="max-h-96 overflow-y-auto">
            {/* Tümü */}
            <button
              onClick={() => handleSelect('all')}
              className={`w-full px-4 py-3 flex items-center justify-between hover:bg-bg-card transition-colors ${
                selectedLeague === 'all' ? 'bg-accent-primary/5' : ''
              }`}
            >
              <div className="flex items-center gap-3">
                <span className="text-base">⚽</span>
                <span className="text-sm font-semibold text-text-primary">Tümü</span>
              </div>
              {selectedLeague === 'all' && (
                <Check className="w-5 h-5 text-accent-primary" />
              )}
            </button>

            {/* Ligler */}
            {sortedLeagues.map(leagueId => {
              const displayName = getLeagueDisplayName(leagueId);
              const fullName = getLeagueName(leagueId);
              const flag = extractFlag(fullName);
              
              return (
                <button
                  key={leagueId}
                  onClick={() => handleSelect(leagueId)}
                  className={`w-full px-4 py-3 flex items-center justify-between hover:bg-bg-card transition-colors ${
                    selectedLeague === leagueId ? 'bg-accent-primary/5' : ''
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-base">{flag}</span>
                    <span className="text-sm font-semibold text-text-primary">{displayName}</span>
                  </div>
                  {selectedLeague === leagueId && (
                    <Check className="w-5 h-5 text-accent-primary" />
                  )}
                </button>
              );
            })}
          </div>

          {/* Tüm Ligleri Gör Footer */}
          <div className="px-4 py-3 border-t border-border-color bg-bg-card">
            <button 
              onClick={() => {
                setIsOpen(false);
                setModalInitialTab('all');
                setIsModalOpen(true);
                onModalStateChange?.(true);
              }}
              className="w-full text-center text-sm font-semibold text-accent-primary hover:text-accent-hover transition-colors"
            >
              Tüm Ligleri Gör →
            </button>
          </div>
        </div>
      )}

      {/* All Leagues Modal */}
      <AllLeaguesModal
        isOpen={isModalOpen}
        onClose={() => {
          setIsModalOpen(false);
          onModalStateChange?.(false);
        }}
        onSelectLeagues={(leagueNames) => {
          // Seçilen liglere ait maçları göster
          // Şimdilik ilk ligi seç (çoklu filtre için page.tsx'te değişiklik gerekir)
          if (leagueNames.length > 0) {
            const firstMatch = matches.find(m => leagueNames.includes(m.leagueName));
            if (firstMatch) {
              onSelectLeague(firstMatch.leagueId);
            }
          }
        }}
        currentMatches={matches}
        initialTab={modalInitialTab}
      />

      {/* Favorites Popup */}
      <FavoritesPopup
        isOpen={isFavoritesOpen}
        onClose={() => setIsFavoritesOpen(false)}
        onSelectLeague={onSelectLeague}
        matches={matches}
        triggerButtonRef={favoritesButtonRef}
      />

      {/* Popular Popup */}
      <PopularPopup
        isOpen={isPopularOpen}
        onClose={() => setIsPopularOpen(false)}
        onSelectLeague={(leagueId) => {
          onSelectLeague(leagueId);
          setIsPopularOpen(false);
        }}
        matches={matches}
        triggerButtonRef={popularButtonRef}
      />
    </div>
  );
}

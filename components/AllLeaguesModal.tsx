'use client';

import { useState, useEffect } from 'react';
import { Search, Check, X, Sparkles } from 'lucide-react';
import { ALL_LEAGUES, POPULAR_LEAGUES, getLeagueFlag } from '@/config/leagues';

interface AllLeaguesModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectLeagues: (leagueNames: string[]) => void;
  currentMatches: any[];
  initialTab?: 'all' | 'selected' | 'favorites' | 'popular';
}

export default function AllLeaguesModal({ isOpen, onClose, onSelectLeagues, currentMatches, initialTab = 'all' }: AllLeaguesModalProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLeagues, setSelectedLeagues] = useState<string[]>([]);
  const [filterTab, setFilterTab] = useState<'all' | 'selected' | 'favorites' | 'popular'>(initialTab);
  const [showSuccess, setShowSuccess] = useState(false);
  const [favoriteLeagues, setFavoriteLeagues] = useState<string[]>([]);

  // Load favorites from localStorage
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('favoriteLeagues');
      if (stored) {
        setFavoriteLeagues(JSON.parse(stored));
      }
    }
  }, []);

  // Update tab when modal opens
  useEffect(() => {
    if (isOpen) {
      setFilterTab(initialTab);
    }
  }, [isOpen, initialTab]);

  if (!isOpen) return null;

  // Arama filtresi
  const filteredLeagues = ALL_LEAGUES.filter(league =>
    league.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Tab filtresi
  const displayLeagues = filterTab === 'selected' 
    ? filteredLeagues.filter(l => selectedLeagues.includes(l))
    : filterTab === 'favorites'
    ? filteredLeagues.filter(l => favoriteLeagues.includes(l))
    : filterTab === 'popular'
    ? filteredLeagues.filter(l => POPULAR_LEAGUES.includes(l))
    : filteredLeagues;

  const toggleLeague = (leagueName: string) => {
    setSelectedLeagues(prev => 
      prev.includes(leagueName) 
        ? prev.filter(l => l !== leagueName)
        : [...prev, leagueName]
    );
  };

  // Tümünü seç/kaldır
  const toggleSelectAll = () => {
    if (selectedLeagues.length === displayLeagues.length && displayLeagues.length > 0) {
      setSelectedLeagues([]);
    } else {
      setSelectedLeagues(displayLeagues);
    }
  };

  const handleApply = () => {
    // Seçili ligleri favorilere ekle
    if (typeof window !== 'undefined') {
      const updatedFavorites = Array.from(new Set([...favoriteLeagues, ...selectedLeagues]));
      setFavoriteLeagues(updatedFavorites);
      localStorage.setItem('favoriteLeagues', JSON.stringify(updatedFavorites));
    }
    
    onSelectLeagues(selectedLeagues);
    setShowSuccess(true);
    setTimeout(() => {
      setShowSuccess(false);
      onClose();
      setSelectedLeagues([]);
    }, 2000);
  };

  return (
    <>
      {/* Backdrop with blur */}
      <div 
        className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 transition-all duration-300 animate-in fade-in"
        onClick={onClose}
      />

      {/* Modal - Bottom Sheet on Mobile, Center on Desktop */}
      <div 
        className="fixed inset-x-0 bottom-0 md:inset-0 z-50 md:flex md:items-center md:justify-center p-0 md:p-4 animate-in slide-in-from-bottom md:zoom-in-95 duration-300"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="relative bg-gradient-to-br from-[#0F1419] via-[#0D1117] to-[#0A0E13] w-full h-[85vh] md:h-auto md:max-h-[90vh] md:w-full md:max-w-lg rounded-t-3xl md:rounded-3xl flex flex-col shadow-2xl border-t border-gray-800/50 md:border overflow-hidden">
          
          {/* Glassmorphism Header */}
          <div className="relative bg-gradient-to-r from-accent-primary/10 to-purple-500/10 backdrop-blur-xl border-b border-gray-800/50">
            {/* Close Button */}
            <button
              onClick={onClose}
              className="absolute top-4 right-4 z-10 p-2 rounded-full bg-gray-900/50 hover:bg-gray-800 transition-all"
            >
              <X className="w-5 h-5 text-gray-400" />
            </button>

            {/* Title */}
            <div className="px-6 pt-6 pb-4">
              <div className="flex items-center gap-3 mb-4">
                <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-accent-primary to-purple-500 flex items-center justify-center">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white">Tüm Ligler</h2>
                  <p className="text-xs text-gray-400">{displayLeagues.length} lig listelendi</p>
                </div>
              </div>

              {/* Search Bar */}
              <div className="relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
                <input
                  type="text"
                  placeholder="Lig ara..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 bg-gray-900/50 backdrop-blur-sm border border-gray-800/50 rounded-2xl text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-accent-primary/50 focus:border-accent-primary transition-all"
                />
              </div>
            </div>

            {/* Filter Tabs - Scrollable */}
            <div className="px-6 pb-4">
              <div className="flex items-center gap-2 overflow-x-auto scrollbar-hide">
                <button
                  onClick={() => setFilterTab('all')}
                  className={`flex-shrink-0 px-4 py-2 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                    filterTab === 'all'
                      ? 'bg-gradient-to-r from-accent-primary to-green-400 text-black shadow-lg shadow-accent-primary/30'
                      : 'bg-gray-900/50 text-gray-400 hover:bg-gray-800/50'
                  }`}
                >
                  🌍 Tümü
                </button>
                <button
                  onClick={() => setFilterTab('selected')}
                  className={`flex-shrink-0 px-4 py-2 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                    filterTab === 'selected'
                      ? 'bg-gradient-to-r from-accent-primary to-green-400 text-black shadow-lg shadow-accent-primary/30'
                      : 'bg-gray-900/50 text-gray-400 hover:bg-gray-800/50'
                  }`}
                >
                  ✓ Seçililer ({selectedLeagues.length})
                </button>
                <button
                  onClick={() => setFilterTab('favorites')}
                  className={`flex-shrink-0 px-4 py-2 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                    filterTab === 'favorites'
                      ? 'bg-gradient-to-r from-accent-primary to-green-400 text-black shadow-lg shadow-accent-primary/30'
                      : 'bg-gray-900/50 text-gray-400 hover:bg-gray-800/50'
                  }`}
                >
                  ⭐ Favoriler ({favoriteLeagues.length})
                </button>
                <button
                  onClick={() => setFilterTab('popular')}
                  className={`flex-shrink-0 px-4 py-2 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                    filterTab === 'popular'
                      ? 'bg-gradient-to-r from-accent-primary to-green-400 text-black shadow-lg shadow-accent-primary/30'
                      : 'bg-gray-900/50 text-gray-400 hover:bg-gray-800/50'
                  }`}
                >
                  🔥 Popüler
                </button>
              </div>
            </div>
          </div>

          {/* Leagues List */}
          <div className="flex-1 overflow-y-auto px-4 py-4">
            <div className="space-y-2">
              {displayLeagues.map((league, index) => {
                const isSelected = selectedLeagues.includes(league);
                
                return (
                  <button
                    key={index}
                    onClick={() => toggleLeague(league)}
                    className={`group w-full flex items-center gap-3 px-4 py-4 rounded-2xl transition-all duration-200 ${
                      isSelected
                        ? 'bg-gradient-to-r from-accent-primary/20 to-green-500/20 border-2 border-accent-primary scale-[1.02] shadow-lg shadow-accent-primary/20'
                        : 'bg-gray-900/30 hover:bg-gray-800/50 border border-gray-800/50'
                    }`}
                  >
                    {/* Animated Checkbox */}
                    <div className={`relative flex-shrink-0 w-6 h-6 rounded-lg border-2 flex items-center justify-center transition-all duration-300 ${
                      isSelected
                        ? 'bg-gradient-to-br from-accent-primary to-green-400 border-accent-primary rotate-12 scale-110'
                        : 'border-gray-700 group-hover:border-accent-primary/50'
                    }`}>
                      {isSelected && (
                        <Check className="w-4 h-4 text-black animate-in zoom-in-50 duration-200" />
                      )}
                    </div>
                    
                    {/* League Icon & Name */}
                    <span className="text-2xl flex-shrink-0 transform group-hover:scale-110 transition-transform duration-200">
                      {getLeagueFlag(league)}
                    </span>
                    <span className={`text-sm font-semibold text-left flex-1 truncate transition-colors ${
                      isSelected ? 'text-white' : 'text-gray-300 group-hover:text-white'
                    }`}>
                      {league}
                    </span>

                    {/* Success Badge */}
                    {isSelected && (
                      <div className="flex-shrink-0 px-2 py-1 rounded-lg bg-accent-primary/20 text-accent-primary text-xs font-bold animate-in zoom-in-50 duration-200">
                        Seçildi
                      </div>
                    )}
                  </button>
                );
              })}
            </div>

            {displayLeagues.length === 0 && (
              <div className="text-center py-20">
                <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gray-900/50 flex items-center justify-center">
                  <Search className="w-10 h-10 text-gray-700" />
                </div>
                <p className="text-gray-500 font-medium">Lig bulunamadı</p>
                <p className="text-gray-600 text-sm mt-1">Farklı anahtar kelimeler deneyin</p>
              </div>
            )}
          </div>

          {/* Bottom Action Bar - Fixed to modal bottom */}
          <div className="flex-shrink-0 p-4 bg-gradient-to-t from-[#0D1117] via-[#0D1117]/95 to-transparent border-t border-gray-800/50">
            <div className="flex items-center gap-3">
              {/* Quick Select All */}
              <button
                onClick={toggleSelectAll}
                className="flex-1 py-3 px-4 rounded-xl bg-gray-900/50 hover:bg-gray-800/50 border border-gray-800 text-gray-400 font-bold text-sm transition-all active:scale-95"
              >
                {selectedLeagues.length === displayLeagues.length && displayLeagues.length > 0 ? (
                  <>✓ Temizle</>
                ) : (
                  <>+ Tümünü Seç</>
                )}
              </button>

              {/* Apply Button */}
              <button
                onClick={handleApply}
                disabled={selectedLeagues.length === 0}
                className={`flex-[2] py-3 px-6 rounded-xl font-bold text-sm transition-all duration-200 flex items-center justify-center gap-2 ${
                  selectedLeagues.length > 0
                    ? 'bg-gradient-to-r from-accent-primary to-green-400 text-black shadow-lg shadow-accent-primary/30 hover:shadow-accent-primary/50 active:scale-95'
                    : 'bg-gray-900/50 text-gray-600 cursor-not-allowed border border-gray-800'
                }`}
              >
                <Check className="w-5 h-5" />
                Uygula ({selectedLeagues.length})
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Success Toast - Modern */}
      {showSuccess && (
        <div className="fixed top-20 left-1/2 -translate-x-1/2 z-[60] px-4 w-full max-w-sm animate-in slide-in-from-top duration-300">
          <div className="bg-gradient-to-r from-accent-primary to-green-400 rounded-2xl px-6 py-4 shadow-2xl shadow-accent-primary/50">
            <div className="flex items-center gap-4">
              <div className="w-10 h-10 bg-black/20 rounded-xl flex items-center justify-center flex-shrink-0">
                <Check className="w-6 h-6 text-black" />
              </div>
              <div className="flex-1">
                <div className="text-black font-bold text-base">Harika!</div>
                <div className="text-black/80 text-sm">{selectedLeagues.length} lig eklendi</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

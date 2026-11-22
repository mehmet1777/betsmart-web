'use client';

import { useEffect, useRef } from 'react';
import { Flame, X } from 'lucide-react';
import { POPULAR_LEAGUES, getLeagueFlag } from '@/config/leagues';

interface PopularPopupProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectLeague: (leagueId: number, leagueIds?: number[]) => void;
  matches: any[];
  triggerButtonRef: React.RefObject<HTMLButtonElement>;
}

export default function PopularPopup({ isOpen, onClose, onSelectLeague, matches, triggerButtonRef }: PopularPopupProps) {
  const popupRef = useRef<HTMLDivElement>(null);

  // Close on outside click
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      const target = event.target as Node;
      const clickedTrigger = triggerButtonRef.current?.contains(target);
      const clickedPopup = popupRef.current?.contains(target);
      
      if (!clickedTrigger && !clickedPopup) {
        onClose();
      }
    };

    // Close on ESC key
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    if (isOpen) {
      // Delay to prevent immediate close
      setTimeout(() => {
        document.addEventListener('mousedown', handleClickOutside);
        document.addEventListener('keydown', handleEscKey);
      }, 100);
    }
    
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscKey);
    };
  }, [isOpen, onClose, triggerButtonRef]);

  // Fuzzy matching fonksiyonu - lig isimlerini normalize et
  const normalizeLeagueName = (name: string): string => {
    return name
      .toLowerCase()
      .replace(/[^\w\s]/g, '') // Özel karakterleri kaldır
      .replace(/\s+/g, ' ')     // Çoklu boşlukları tek boşluğa çevir
      .trim();
  };

  // Kesin eşleştirme - popüler lig ile match'i karşılaştır
  const isExactMatch = (popularLeague: string, matchLeague: string): boolean => {
    const popNorm = normalizeLeagueName(popularLeague);
    const matchNorm = normalizeLeagueName(matchLeague);
    
    // Anahtar kelimeler çıkar - BÜYÜK harfler önemli (A, B, C ayırımı için)
    const popWords = popularLeague.toLowerCase().split(' ');
    const matchWords = matchLeague.toLowerCase().split(' ');
    
    // Her popüler lig kelimesi match'te olmalı
    for (const popWord of popWords) {
      if (popWord.length <= 2) continue; // Kısa kelimeleri atla
      if (!matchNorm.includes(normalizeLeagueName(popWord))) {
        return false;
      }
    }
    
    // Ek kontroller - İstenmeyen kelimeleri reddet
    const unwantedPatterns = [
      { pop: 'serie a', match: ['serie b', 'serie c', 'kadınlar', 'women', 'kadın'] },
      { pop: 'premier lig', match: ['2. lig', '1. lig', 'kadınlar', 'women', 'championship'] },
      { pop: 'bundesliga', match: ['2. bundesliga', '3. liga', 'kadınlar', 'women'] },
      { pop: 'ligue 1', match: ['ligue 2', 'ligue 3', 'kadınlar', 'women'] },
      { pop: 'süper lig', match: ['1. lig', '2. lig', '3. lig', 'kadınlar', 'women', 'tff'] },
      { pop: 'laliga', match: ['laliga 2', '2.lig', 'kadınlar', 'women', 'segunda'] },
      { pop: 'la liga', match: ['la liga 2', '2.lig', 'kadınlar', 'women', 'segunda'] },
      { pop: 'eredivisie', match: ['eerste divisie', 'tweede', 'kadınlar', 'women'] },
      { pop: 'j1 lig', match: ['j2', 'j3', 'kadınlar', 'women'] },
      { pop: 'k lig 1', match: ['k lig 2', 'kadınlar', 'women'] },
    ];
    
    // Pattern kontrolü
    for (const pattern of unwantedPatterns) {
      if (popNorm.includes(normalizeLeagueName(pattern.pop))) {
        // Bu popüler lig için istenmeyen kelimeler var mı?
        for (const unwanted of pattern.match) {
          if (matchNorm.includes(normalizeLeagueName(unwanted))) {
            return false; // İstenmeyen kelime bulundu, eşleşme yok
          }
        }
      }
    }
    
    return true;
  };

  // Popüler lig adını match'lerle eşleştir
  const findMatchingLeague = (popularLeague: string) => {
    return matches.find(m => {
      if (!m.leagueName) return false;
      return isExactMatch(popularLeague, m.leagueName);
    });
  };

  // Aynı lige ait tüm leagueId'leri bul
  const findAllLeagueIds = (popularLeague: string): number[] => {
    const matchingMatches = matches.filter(m => {
      if (!m.leagueName) return false;
      return isExactMatch(popularLeague, m.leagueName);
    });
    
    // Unique leagueId'leri çıkar
    const uniqueIds = [...new Set(matchingMatches.map(m => m.leagueId))];
    return uniqueIds;
  };

  const handleSelectLeague = (leagueName: string) => {
    const match = findMatchingLeague(leagueName);
    const allLeagueIds = findAllLeagueIds(leagueName);
    
    if (match && allLeagueIds.length > 0) {
      onSelectLeague(match.leagueId, allLeagueIds);
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div
      ref={popupRef}
      className="absolute top-full left-4 mt-2 w-80 bg-[#0D1117] border border-gray-800 rounded-2xl shadow-2xl z-50 overflow-hidden"
    >
      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-800 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Flame className="w-4 h-4 text-orange-500 fill-orange-500" />
          <span className="text-sm font-bold text-white">Popüler Ligler</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400">{POPULAR_LEAGUES.length} lig</span>
          <button
            onClick={onClose}
            className="p-1 text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* List */}
      <div className="max-h-96 overflow-y-auto p-2">
        {POPULAR_LEAGUES.map((league, index) => {
          const match = findMatchingLeague(league);
          const matchCount = match ? matches.filter(m => {
            if (!m.leagueName) return false;
            return isExactMatch(league, m.leagueName);
          }).length : 0;
          
          return (
            <button
              key={index}
              onClick={() => {
                if (match) {
                  handleSelectLeague(league);
                }
              }}
              className="w-full flex items-center justify-between px-3 py-2.5 rounded-xl hover:bg-accent-primary/10 hover:border hover:border-accent-primary transition-all cursor-pointer"
            >
              <div className="flex items-center gap-3">
                <span className="text-lg">{getLeagueFlag(league)}</span>
                <div className="text-left">
                  <div className="text-sm font-semibold text-white">{league}</div>
                  <div className={`text-xs ${matchCount > 0 ? 'text-accent-primary' : 'text-gray-500'}`}>
                    {matchCount > 0 ? `${matchCount} maç bugün` : 'Bugün maç yok'}
                  </div>
                </div>
              </div>
              
              {matchCount > 0 && (
                <div className="text-accent-primary text-xs font-semibold">
                  Göster →
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}

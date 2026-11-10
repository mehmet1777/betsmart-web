'use client';

import { useEffect, useRef } from 'react';
import { Flame, X } from 'lucide-react';
import { POPULAR_LEAGUES, getLeagueFlag } from '@/config/leagues';

interface PopularPopupProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectLeague: (leagueId: number) => void;
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

  const handleSelectLeague = (leagueName: string) => {
    const match = matches.find(m => m.leagueName === leagueName);
    if (match) {
      onSelectLeague(match.leagueId);
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
          const matchCount = matches.filter(m => m.leagueName === league).length;
          const match = matches.find(m => m.leagueName === league);
          
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

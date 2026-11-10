'use client';

import { useState, useEffect, useRef } from 'react';
import { Check, Star, X } from 'lucide-react';
import { getLeagueFlag } from '@/config/leagues';

interface FavoritesPopupProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectLeague: (leagueId: number) => void;
  matches: any[];
  triggerButtonRef: React.RefObject<HTMLButtonElement>;
}

export default function FavoritesPopup({ isOpen, onClose, onSelectLeague, matches, triggerButtonRef }: FavoritesPopupProps) {
  const [favoriteLeagues, setFavoriteLeagues] = useState<string[]>([]);
  const popupRef = useRef<HTMLDivElement>(null);

  // Load favorites from localStorage
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('favoriteLeagues');
      if (stored) {
        setFavoriteLeagues(JSON.parse(stored));
      }
    }
  }, [isOpen]);

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

  const removeFavorite = (leagueName: string) => {
    const updated = favoriteLeagues.filter(l => l !== leagueName);
    setFavoriteLeagues(updated);
    localStorage.setItem('favoriteLeagues', JSON.stringify(updated));
  };

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
          <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
          <span className="text-sm font-bold text-white">Favori Liglerim</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-400">{favoriteLeagues.length} lig</span>
          <button
            onClick={onClose}
            className="p-1 text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* List */}
      <div className="max-h-96 overflow-y-auto">
        {favoriteLeagues.length === 0 ? (
          <div className="px-4 py-8 text-center">
            <Star className="w-12 h-12 text-gray-700 mx-auto mb-2" />
            <p className="text-sm text-gray-500">Henüz favori lig eklemediniz</p>
            <p className="text-xs text-gray-600 mt-1">Ligler menüsünden ekleyin</p>
          </div>
        ) : (
          <div className="p-2">
            {favoriteLeagues.map((league, index) => {
              const match = matches.find(m => m.leagueName === league);
              const matchCount = matches.filter(m => m.leagueName === league).length;
              
              return (
                <button
                  key={index}
                  onClick={() => handleSelectLeague(league)}
                  className="w-full flex items-center justify-between px-3 py-2.5 rounded-xl hover:bg-accent-primary/10 hover:border hover:border-accent-primary transition-all group"
                >
                  <div className="flex items-center gap-3">
                    <span className="text-lg">{getLeagueFlag(league)}</span>
                    <div className="text-left">
                      <div className="text-sm font-semibold text-white">{league}</div>
                      <div className="text-xs text-gray-500">{matchCount} maç</div>
                    </div>
                  </div>
                  
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFavorite(league);
                    }}
                    className="opacity-0 group-hover:opacity-100 p-1 text-gray-500 hover:text-red-500 transition-all"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </button>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

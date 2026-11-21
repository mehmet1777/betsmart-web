'use client';

import { useState, useEffect } from 'react';
import { X, Search } from 'lucide-react';
import { Match } from '@/types';

interface SearchModalProps {
  isOpen: boolean;
  onClose: () => void;
  matches: Match[];
}

export default function SearchModal({ isOpen, onClose, matches }: SearchModalProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [filteredMatches, setFilteredMatches] = useState<Match[]>([]);

  useEffect(() => {
    if (searchQuery.trim() === '') {
      setFilteredMatches([]);
      return;
    }

    const query = searchQuery.toLowerCase().trim();
    const results = matches.filter(match => 
      match.home.name.toLowerCase().includes(query) ||
      match.away.name.toLowerCase().includes(query)
    );

    setFilteredMatches(results);
  }, [searchQuery, matches]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-start justify-center pt-20 px-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative w-full max-w-2xl bg-bg-secondary rounded-xl shadow-2xl max-h-[80vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center gap-3 p-4 border-b border-border-color">
          <Search className="w-5 h-5 text-text-secondary" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Takım adı ile ara..."
            className="flex-1 bg-transparent text-text-primary placeholder-text-secondary outline-none text-base"
            autoFocus
          />
          <button
            onClick={onClose}
            className="p-1 text-text-secondary hover:text-text-primary transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Results */}
        <div className="flex-1 overflow-y-auto p-4">
          {searchQuery.trim() === '' ? (
            <div className="text-center py-12 text-text-secondary">
              Takım adı yazın...
            </div>
          ) : filteredMatches.length === 0 ? (
            <div className="text-center py-12 text-text-secondary">
              "{searchQuery}" için sonuç bulunamadı
            </div>
          ) : (
            <div className="space-y-2">
              <div className="text-sm text-text-secondary mb-3">
                {filteredMatches.length} sonuç bulundu
              </div>
              {filteredMatches.map((match) => (
                <div
                  key={match.id}
                  className="bg-bg-card rounded-lg p-4 border border-border-color hover:border-accent-primary/30 transition-colors"
                >
                  {/* Date & League */}
                  <div className="flex items-center gap-2 mb-2 text-xs text-text-secondary">
                    <span>{match.time}</span>
                    <span>•</span>
                    <span>{match.leagueName || `Lig ${match.leagueId}`}</span>
                  </div>

                  {/* Teams */}
                  <div className="mb-3">
                    <div className="text-text-primary font-medium">{match.home.name}</div>
                    <div className="text-text-primary font-medium">{match.away.name}</div>
                  </div>

                  {/* Odds */}
                  {match.odds && (
                    <div className="flex gap-2">
                      <div className="flex-1 bg-bg-app rounded px-3 py-2 text-center">
                        <div className="text-xs text-text-secondary mb-1">MS1</div>
                        <div className="text-sm font-bold text-accent-primary">{match.odds.home}</div>
                      </div>
                      <div className="flex-1 bg-bg-app rounded px-3 py-2 text-center">
                        <div className="text-xs text-text-secondary mb-1">MSX</div>
                        <div className="text-sm font-bold text-accent-primary">{match.odds.draw}</div>
                      </div>
                      <div className="flex-1 bg-bg-app rounded px-3 py-2 text-center">
                        <div className="text-xs text-text-secondary mb-1">MS2</div>
                        <div className="text-sm font-bold text-accent-primary">{match.odds.away}</div>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

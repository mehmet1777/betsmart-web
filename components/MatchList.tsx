'use client';

import { useState, useEffect } from 'react';
import { Match, BetSelection, LEAGUE_NAMES } from '@/types';
import MatchCard from './MatchCard';
import { Search, Calendar, Filter } from 'lucide-react';

interface MatchListProps {
  onSelectMatch: (selection: BetSelection) => void;
  selectedMatches: BetSelection[];
}

export default function MatchList({ onSelectMatch, selectedMatches }: MatchListProps) {
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedLeague, setSelectedLeague] = useState<number | 'all'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    loadMatches();
  }, []);

  const loadMatches = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/matches');
      if (response.ok) {
        const data = await response.json();
        setMatches(data.matches || []);
      }
    } catch (error) {
      console.error('Maç yükleme hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredMatches = matches.filter(match => {
    const matchesLeague = selectedLeague === 'all' || match.leagueId === selectedLeague;
    const matchesSearch = searchQuery === '' || 
      match.home.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      match.away.name.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesLeague && matchesSearch;
  });

  const uniqueLeagues = Array.from(new Set(matches.map(m => m.leagueId)));

  const groupedMatches = filteredMatches.reduce((acc, match) => {
    if (!acc[match.leagueId]) {
      acc[match.leagueId] = [];
    }
    acc[match.leagueId].push(match);
    return acc;
  }, {} as Record<number, Match[]>);

  return (
    <div className="section-spacing">
      {/* Editorial Header */}
      <div className="mb-6 md:mb-8">
        <div className="flex items-start justify-between mb-6">
          <div className="flex-1">
            <h1 className="text-3xl md:text-4xl font-bold tracking-tight text-text-primary mb-2">
              Günün Maçları
            </h1>
            <p className="text-sm md:text-base font-medium text-text-tertiary">
              {filteredMatches.length} maç bulundu
            </p>
          </div>
          <button className="hidden md:flex items-center gap-2 px-4 py-2.5 bg-bg-tertiary editorial-border rounded-lg text-text-secondary hover:text-text-primary premium-hover">
            <Calendar className="w-4 h-4" />
            <span className="body-md">Bugün</span>
          </button>
        </div>
        <div className="editorial-divider"></div>
      </div>

      {/* Search & Filters */}
      <div className="mb-5">
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
          <input
            type="text"
            placeholder="Takım ara..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-11 pr-4 py-3.5 bg-bg-tertiary editorial-border rounded-xl text-text-primary placeholder:text-text-muted focus:outline-none focus:border-border-accent premium-hover text-[15px]"
          />
        </div>
      </div>

      {/* League Pills */}
      <div className="overflow-x-auto -mx-4 md:mx-0 mb-8">
        <div className="flex gap-2 px-4 md:px-0 pb-1 md:flex-wrap">
          <button
            onClick={() => setSelectedLeague('all')}
            className={`flex-shrink-0 px-4 py-2.5 rounded-xl text-sm font-medium premium-hover whitespace-nowrap ${
              selectedLeague === 'all'
                ? 'bg-active-overlay text-accent-primary border border-border-accent'
                : 'bg-bg-tertiary text-text-secondary editorial-border'
            }`}
          >
            Tümü
          </button>
          {uniqueLeagues.map(leagueId => (
            <button
              key={leagueId}
              onClick={() => setSelectedLeague(leagueId)}
              className={`flex-shrink-0 px-4 py-2.5 rounded-xl text-sm font-medium premium-hover whitespace-nowrap ${
                selectedLeague === leagueId
                  ? 'bg-active-overlay text-accent-primary border border-border-accent'
                  : 'bg-bg-tertiary text-text-secondary editorial-border'
              }`}
            >
              {LEAGUE_NAMES[leagueId] || `Lig ${leagueId}`}
            </button>
          ))}
        </div>
      </div>

      {/* Matches */}
      {loading ? (
        <div className="flex items-center justify-center py-32">
          <div className="relative">
            <div className="animate-spin rounded-full h-12 w-12 border-2 border-bg-elevated border-t-accent-primary"></div>
          </div>
        </div>
      ) : filteredMatches.length === 0 ? (
        <div className="bg-bg-tertiary editorial-border rounded-xl p-16 text-center">
          <div className="w-16 h-16 bg-bg-elevated rounded-2xl flex items-center justify-center mx-auto mb-4 editorial-border">
            <Search className="w-7 h-7 text-text-muted" />
          </div>
          <h3 className="heading-md mb-2">Maç Bulunamadı</h3>
          <p className="body-md text-text-tertiary">
            Arama kriterlerinize uygun maç bulunamadı
          </p>
        </div>
      ) : (
        <div className="space-y-10">
          {Object.entries(groupedMatches).map(([leagueId, leagueMatches]) => (
            <div key={leagueId}>
              {/* League Header */}
              <div className="mb-4">
                <h2 className="text-text-secondary font-bold uppercase tracking-wide text-xs px-1">
                  {LEAGUE_NAMES[Number(leagueId)] || `Lig ${leagueId}`}
                </h2>
              </div>

              {/* Matches */}
              <div className="space-y-3">
                {leagueMatches.map(match => {
                  const selection = selectedMatches.find(s => s.matchId === match.id);
                  return (
                    <MatchCard
                      key={match.id}
                      match={match}
                      onSelect={onSelectMatch}
                      selectedPrediction={selection?.prediction}
                    />
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

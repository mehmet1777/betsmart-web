'use client';

import { Match, BetSelection } from '@/types';

interface MatchCardProps {
  match: Match;
  leagueName: string;
  leagueIcon?: string;
  onSelect: (selection: BetSelection) => void;
  selectedPrediction?: '1' | 'X' | '2';
  isLive?: boolean;
}

export default function MatchCard({ match, leagueName, leagueIcon, onSelect, selectedPrediction, isLive }: MatchCardProps) {
  const handleOddClick = (prediction: '1' | 'X' | '2') => {
    onSelect({
      matchId: match.id,
      match,
      prediction
    });
  };

  return (
    <div className="bg-bg-card rounded-2xl p-4 mx-4 mb-3">
      {/* League Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-lg">{leagueIcon || '🏆'}</span>
          <span className="text-text-secondary text-sm font-medium">{leagueName}</span>
        </div>
        <div className="flex items-center gap-2">
          {isLive && (
            <span className="flex items-center gap-1 text-accent-primary text-xs font-semibold">
              <span className="w-1.5 h-1.5 bg-accent-primary rounded-full animate-pulse"></span>
              Canlı
            </span>
          )}
          <span className="text-text-secondary text-sm">{match.time.split(' ')[1]}</span>
        </div>
      </div>

      {/* Teams */}
      <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-2 mb-4">
        {/* Home Team */}
        <div className="flex items-center gap-2 min-w-0">
          <div className="w-8 h-8 bg-bg-elevated rounded-full flex items-center justify-center flex-shrink-0">
            <span className="text-lg">🏠</span>
          </div>
          <span className="text-text-primary font-semibold text-xs truncate block">{match.home.name}</span>
        </div>

        {/* Time */}
        <div className="text-center flex-shrink-0 px-2">
          <span className="text-text-secondary text-xs font-medium whitespace-nowrap">
            {match.time.split(' ')[1]}
          </span>
          <div className="text-text-muted text-[10px]">Bugün</div>
        </div>

        {/* Away Team */}
        <div className="flex items-center gap-2 justify-end min-w-0">
          <span className="text-text-primary font-semibold text-xs truncate block text-right">{match.away.name}</span>
          <div className="w-8 h-8 bg-bg-elevated rounded-full flex items-center justify-center flex-shrink-0">
            <span className="text-lg">✈️</span>
          </div>
        </div>
      </div>

      {/* Odds */}
      <div className="grid grid-cols-3 gap-2">
        {[
          { id: '1', label: '1', odds: match.odds?.home },
          { id: 'X', label: 'X', odds: match.odds?.draw },
          { id: '2', label: '2', odds: match.odds?.away }
        ].map((odd) => {
          const isDisabled = !odd.odds || odd.odds === '-' || odd.odds === 'null';
          
          return (
            <button
              key={odd.id}
              onClick={() => !isDisabled && handleOddClick(odd.id as '1' | 'X' | '2')}
              disabled={isDisabled}
              className={`py-3 rounded-xl transition-all ${
                isDisabled
                  ? 'bg-bg-elevated border border-border-color opacity-40 cursor-not-allowed'
                  : selectedPrediction === odd.id
                  ? 'bg-accent-primary'
                  : 'bg-bg-elevated border border-border-color hover:border-accent-primary'
              }`}
            >
              <div className={`text-xs font-medium mb-1 ${
                isDisabled
                  ? 'text-text-muted'
                  : selectedPrediction === odd.id 
                  ? 'text-bg-app' 
                  : 'text-text-muted'
              }`}>
                {odd.label}
              </div>
              <div className={`text-base font-bold ${
                isDisabled
                  ? 'text-text-muted'
                  : selectedPrediction === odd.id 
                  ? 'text-bg-app' 
                  : 'text-accent-primary'
              }`}>
                {isDisabled ? '-' : odd.odds}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

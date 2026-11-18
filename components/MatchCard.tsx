'use client';

import { useState } from 'react';
import { Match, BetSelection } from '@/types';
import OddsAnalysisModal from './OddsAnalysisModal';

interface MatchCardProps {
  match: Match;
  leagueName: string;
  leagueIcon?: string;
  onSelect: (selection: BetSelection) => void;
  selectedPrediction?: '1' | 'X' | '2';
  isLive?: boolean;
  isRecommended?: boolean;
  recommendedWinRate?: number;
}

export default function MatchCard({ match, leagueName, leagueIcon, onSelect, selectedPrediction, isLive, isRecommended, recommendedWinRate }: MatchCardProps) {
  const [showAnalysis, setShowAnalysis] = useState(false);

  const handleOddClick = (prediction: '1' | 'X' | '2') => {
    onSelect({
      matchId: match.id,
      match,
      prediction
    });
  };

  // Oranların geçerli olup olmadığını kontrol et
  const hasValidOdds = () => {
    const home = match.odds?.home;
    const draw = match.odds?.draw;
    const away = match.odds?.away;
    
    if (!home || !draw || !away) return false;
    if (home === '-' || draw === '-' || away === '-') return false;
    
    const homeNum = parseFloat(home);
    const drawNum = parseFloat(draw);
    const awayNum = parseFloat(away);
    
    return homeNum > 1.01 && drawNum > 1.01 && awayNum > 1.01;
  };

  const oddsAvailable = hasValidOdds();

  return (
    <>
      <div className="bg-bg-card rounded-2xl p-4 mx-4 mb-3 relative">
        {/* Önerilen Badge */}
        {isRecommended && (
          <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 z-10">
            <div className="bg-gradient-to-r from-[#8B5CF6] to-[#6366F1] text-white px-3 py-1 rounded-full text-xs font-bold shadow-lg flex items-center gap-1">
              <span>⭐</span>
              <span>Önerilen</span>
              {recommendedWinRate && <span className="text-[#FFD700]">%{recommendedWinRate}</span>}
            </div>
          </div>
        )}
        
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
            {/* Analiz Butonu - Saat yerine */}
            {oddsAvailable ? (
              <button
                onClick={() => setShowAnalysis(true)}
                className="bg-accent-primary/10 hover:bg-accent-primary/20 text-accent-primary px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors"
              >
                📊 Analiz
              </button>
            ) : (
              <span className="bg-bg-elevated/50 text-text-muted/60 px-3 py-1.5 rounded-lg text-base border border-border-color/30">
                🚫
              </span>
            )}
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

    {/* Analiz Modal */}
    <OddsAnalysisModal
      isOpen={showAnalysis}
      onClose={() => setShowAnalysis(false)}
      match={match}
    />
    </>
  );
}

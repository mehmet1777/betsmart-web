'use client';

import { useState, useEffect, useRef } from 'react';
import { Match, BetSelection } from '@/types';
import OddsAnalysisModal from './OddsAnalysisModal';

interface OddsChange {
  change_1: number;
  change_x: number;
  change_2: number;
  detected_at: string;
}

interface MatchCardProps {
  match: Match;
  leagueName: string;
  leagueIcon?: string;
  onSelect: (selection: BetSelection) => void;
  selectedPrediction?: BetSelection['prediction'];
  isLive?: boolean;
  isRecommended?: boolean;
  recommendedWinRate?: number;
  recommendation?: any; // Tam recommendation objesi
}

export default function MatchCard({ match, leagueName, leagueIcon, onSelect, selectedPrediction, isLive, isRecommended, recommendedWinRate, recommendation }: MatchCardProps) {
  const [showAnalysis, setShowAnalysis] = useState(false);
  const [latestChange, setLatestChange] = useState<OddsChange | null>(null);
  const [showRecommendationTooltip, setShowRecommendationTooltip] = useState(false);
  const [tooltipPosition, setTooltipPosition] = useState({ top: 0, left: 0 });
  const badgeRef = useRef<HTMLButtonElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const [hasMatchDetails, setHasMatchDetails] = useState(false);

  useEffect(() => {
    // Oran değişikliklerini fetch et
    const fetchOddsChanges = async () => {
      try {
        const response = await fetch('/api/odds-changes', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            home_team: match.home.name,
            away_team: match.away.name,
          })
        });

        if (response.ok) {
          const data = await response.json();
          if (data.success && data.changes && data.changes.length > 0) {
            // En son değişikliği al
            setLatestChange(data.changes[0]);
          }
        }
      } catch (err) {
        // Sessizce başarısız ol
      }
    };

    // Sahadan match details kontrolü
    const checkMatchDetails = async () => {
      if (!match.match_uuid) {
        setHasMatchDetails(false);
        return;
      }

      try {
        const response = await fetch('/api/match-details', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ match_uuid: match.match_uuid })
        });

        if (response.ok) {
          const data = await response.json();
          setHasMatchDetails(data.success && data.details !== null);
        }
      } catch (err) {
        setHasMatchDetails(false);
      }
    };

    fetchOddsChanges();
    checkMatchDetails();
  }, [match.home.name, match.away.name, match.match_uuid]);

  // Tooltip pozisyonunu hesapla
  useEffect(() => {
    if (showRecommendationTooltip && badgeRef.current && tooltipRef.current) {
      const badgeRect = badgeRef.current.getBoundingClientRect();
      const tooltipRect = tooltipRef.current.getBoundingClientRect();
      
      let top = badgeRect.bottom + 8;
      let left = badgeRect.left + badgeRect.width / 2;
      
      // Viewport kontrolü - sağdan taşma
      if (left + tooltipRect.width / 2 > window.innerWidth - 16) {
        left = window.innerWidth - tooltipRect.width / 2 - 16;
      }
      
      // Viewport kontrolü - soldan taşma
      if (left - tooltipRect.width / 2 < 16) {
        left = tooltipRect.width / 2 + 16;
      }
      
      // Viewport kontrolü - alttan taşma
      if (top + tooltipRect.height > window.innerHeight - 16) {
        top = badgeRect.top - tooltipRect.height - 8;
      }
      
      setTooltipPosition({ top, left });
    }
  }, [showRecommendationTooltip]);

  // Backdrop click handler - dışarıya tıklamayı yakala
  useEffect(() => {
    if (showRecommendationTooltip) {
      const handleClickOutside = (e: MouseEvent) => {
        const target = e.target as HTMLElement;
        
        // Tooltip veya badge'e tıklanmadıysa kapat
        if (
          tooltipRef.current && 
          !tooltipRef.current.contains(target) &&
          badgeRef.current &&
          !badgeRef.current.contains(target)
        ) {
          setShowRecommendationTooltip(false);
        }
      };

      // Kısa bir gecikme ile ekle (tooltip render olsun diye)
      setTimeout(() => {
        document.addEventListener('click', handleClickOutside);
      }, 0);

      return () => {
        document.removeEventListener('click', handleClickOutside);
      };
    }
  }, [showRecommendationTooltip]);

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
      {/* Tooltip Backdrop ve Content - Kartın dışında */}
      {showRecommendationTooltip && (
        <>
          {/* Backdrop - Tam ekran, transparent */}
          <div 
            className="fixed inset-0 z-[60]" 
          />
          
          {/* Tooltip Content - Portal gibi */}
          <div 
            ref={tooltipRef}
            className="fixed z-[70]"
            style={{
              top: `${tooltipPosition.top}px`,
              left: `${tooltipPosition.left}px`,
              transform: 'translateX(-50%)'
            }}
          >
            <div className="w-72 bg-[#1a1a2e] border-2 border-[#8B5CF6] rounded-xl shadow-2xl p-4 animate-in fade-in slide-in-from-top-2 duration-200">
              {/* Arrow */}
              <div className="absolute -top-2 left-1/2 transform -translate-x-1/2 w-4 h-4 bg-[#8B5CF6] rotate-45"></div>
              
              <div className="relative z-10">
                {/* Header */}
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-white font-bold text-sm flex items-center gap-1">
                    ⭐ Akıllı Kupon Önerisi
                  </h4>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setShowRecommendationTooltip(false);
                    }}
                    className="text-gray-400 hover:text-white transition-colors"
                  >
                    ✕
                  </button>
                </div>
                
                {/* Ana Öneri */}
                <div className="bg-[#0f0f1e] rounded-lg p-3 mb-3 border border-[#8B5CF6]/30">
                  <p className="text-[#A5A5C5] text-[10px] mb-1">📌 Ana Öneri</p>
                  <div className="flex items-center justify-between">
                    <span className="text-white font-bold">
                      {recommendation?.recommendation === 'MS1' ? 'Ev Sahibi' : 
                       recommendation?.recommendation === 'MSX' ? 'Beraberlik' : 
                       recommendation?.recommendation === 'MS2' ? 'Deplasman' : 
                       recommendation?.recommendation}
                    </span>
                    <span className="text-[#00E99A] text-xl font-black">%{recommendation?.win_rate}</span>
                  </div>
                  <div className="text-[#A5A5C5] text-[10px] mt-1">
                    Oran: {recommendation?.recommended_odds?.toFixed(2)}
                  </div>
                </div>
                
                {/* İstatistikler */}
                <div className="bg-[#0f0f1e] rounded-lg p-2.5 mb-3 border border-[#8B5CF6]/20">
                  <p className="text-[#A5A5C5] text-[10px] mb-2">📊 {recommendation?.exact_matches} benzer maç</p>
                  <div className="flex items-center justify-between text-[10px]">
                    <div className="flex gap-2">
                      <span className="text-[#00E99A]">🏠 {recommendation?.statistics.home_wins}</span>
                      <span className="text-[#F59E0B]">🤝 {recommendation?.statistics.draws}</span>
                      <span className="text-[#3B82F6]">✈️ {recommendation?.statistics.away_wins}</span>
                    </div>
                  </div>
                </div>
                
                {/* Alternatifler */}
                {recommendation?.additional_insights && recommendation.additional_insights.length > 0 && (
                  <div>
                    <p className="text-[#A5A5C5] text-[10px] mb-2">💡 Ek Öneriler</p>
                    <div className="space-y-1.5">
                      {recommendation.additional_insights.slice(0, 3).map((alt: any, idx: number) => (
                        <div key={idx} className="flex items-center justify-between text-[10px] bg-[#0f0f1e] rounded p-2">
                          <span className="text-white">{alt.label}</span>
                          <span className="text-[#00E99A] font-bold">%{alt.rate}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </>
      )}
      
      <div className="bg-bg-card rounded-2xl p-4 mx-4 mb-3 relative">
        {/* Önerilen Badge */}
        {isRecommended && recommendation && (
          <div 
            className="absolute -top-2 left-1/2 transform -translate-x-1/2 z-10"
          >
            <button
              ref={badgeRef}
              onClick={(e) => {
                e.stopPropagation();
                setShowRecommendationTooltip(!showRecommendationTooltip);
              }}
              className="bg-gradient-to-r from-[#8B5CF6] to-[#6366F1] text-white px-3 py-1 rounded-full text-xs font-bold shadow-lg flex items-center gap-1 hover:shadow-xl transition-all cursor-pointer"
            >
              <span>⭐</span>
              <span>Önerilen</span>
              {recommendedWinRate && <span className="text-[#FFD700]">%{recommendedWinRate}</span>}
            </button>
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
                className="bg-accent-primary/10 hover:bg-accent-primary/20 text-accent-primary px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1"
              >
                📊 Analiz
                {hasMatchDetails && (
                  <span className="text-sm" title="Detaylı H2H ve form verileri mevcut">✨</span>
                )}
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
          { id: '1', label: '1', odds: match.odds?.home, change: latestChange?.change_1 },
          { id: 'X', label: 'X', odds: match.odds?.draw, change: latestChange?.change_x },
          { id: '2', label: '2', odds: match.odds?.away, change: latestChange?.change_2 }
        ].map((odd) => {
          const isDisabled = !odd.odds || odd.odds === '-' || odd.odds === 'null';
          const hasChange = odd.change !== undefined && odd.change !== null && Math.abs(odd.change) > 0.01;
          const isIncrease = hasChange && odd.change! > 0;
          
          return (
            <button
              key={odd.id}
              onClick={() => !isDisabled && handleOddClick(odd.id as '1' | 'X' | '2')}
              disabled={isDisabled}
              className={`py-3 rounded-xl transition-all relative ${
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
              <div className={`text-base font-bold flex items-center justify-center gap-1 ${
                isDisabled
                  ? 'text-text-muted'
                  : selectedPrediction === odd.id 
                  ? 'text-bg-app' 
                  : 'text-accent-primary'
              }`}>
                <span>{isDisabled ? '-' : odd.odds}</span>
                {hasChange && (
                  <span className={`text-xs ${isIncrease ? 'text-green-400' : 'text-red-400'}`}>
                    {isIncrease ? '↑' : '↓'}
                  </span>
                )}
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

'use client';

import { useState, useEffect } from 'react';
import { X, Sparkles, BarChart3, Ticket, TrendingUp, RefreshCw } from 'lucide-react';
import OddsAnalysisModal from './OddsAnalysisModal';

interface SmartCouponRecommendation {
  match: any;
  exact_matches: number;
  total_analyzed: number;
  win_rate: number;
  recommendation: 'MS1' | 'MSX' | 'MS2';
  recommended_odds: number;
  statistics: {
    home_wins: number;
    draws: number;
    away_wins: number;
    gg_yes: number;
    gg_no: number;
    over_25?: number;
    over_35?: number;
  };
  additional_insights?: Array<{
    type: string;
    label: string;
    rate: number;
    count: number;
    total: number;
  }>;
}

interface SmartCouponModalProps {
  isOpen: boolean;
  onClose: () => void;
  recommendations: SmartCouponRecommendation[];
  analyzedCount: number;
  onAddToCoupon: (recommendations: SmartCouponRecommendation[]) => void;
}

export default function SmartCouponModal({ isOpen, onClose, recommendations: initialRecommendations, analyzedCount, onAddToCoupon }: SmartCouponModalProps) {
  const [selectedMatchForAnalysis, setSelectedMatchForAnalysis] = useState<any | null>(null);
  
  const getRecommendationLabel = (type: string) => {
    if (type === 'MS1') return 'Ev Sahibi';
    if (type === 'MSX') return 'Beraberlik';
    if (type === 'MS2') return 'Deplasman';
    return type;
  };

  // Alternatif tiplerine standart oran ataması
  const getStandardOdds = (type: string): number => {
    const oddsMap: Record<string, number> = {
      // Karşılıklı Gol
      'GG_YES': 1.75,
      'GG_NO': 2.00,
      
      // Alt/Üst (Maç)
      'OVER_25': 1.65,
      'UNDER_25': 2.20,
      'OVER_35': 2.40,
      'UNDER_35': 1.55,
      
      // İlk Yarı Alt/Üst
      'HT_OVER_05': 1.30,
      'HT_UNDER_05': 1.85,
      'HT_OVER_15': 1.85,
      'HT_UNDER_15': 1.45,
      
      // İlk Yarı KG
      'HT_GG_YES': 2.80,
      'HT_GG_NO': 1.40
    };
    
    return oddsMap[type] || 1.50; // Varsayılan
  };

  // Her maç için seçilen seçeneği tut - ilk değer direkt hesaplanıyor
  const [matchSelections, setMatchSelections] = useState<Record<number, {
    main: any;
    alternatives: any[];
  }>>(() => {
    const selections: Record<number, any> = {};
    initialRecommendations.forEach((rec, idx) => {
      selections[idx] = {
        main: {
          type: rec.recommendation,
          label: getRecommendationLabel(rec.recommendation),
          odds: rec.recommended_odds,
          rate: rec.win_rate,
          count: null,
          total: null
        },
        alternatives: (rec.additional_insights || []).map(alt => ({
          ...alt,
          odds: getStandardOdds(alt.type) // Standart oran ekle
        }))
      };
    });
    return selections;
  });

  // Recommendations değiştiğinde state'i güncelle
  useEffect(() => {
    const selections: Record<number, any> = {};
    initialRecommendations.forEach((rec, idx) => {
      selections[idx] = {
        main: {
          type: rec.recommendation,
          label: getRecommendationLabel(rec.recommendation),
          odds: rec.recommended_odds,
          rate: rec.win_rate,
          count: null,
          total: null
        },
        alternatives: (rec.additional_insights || []).map(alt => ({
          ...alt,
          odds: getStandardOdds(alt.type) // Standart oran ekle
        }))
      };
    });
    setMatchSelections(selections);
  }, [initialRecommendations]);
  
  if (!isOpen) return null;

  const getRecommendationColor = (type: string) => {
    if (type === 'MS1') return 'bg-[#00E99A]/20 text-[#00E99A] border-[#00E99A]/40';
    if (type === 'MSX') return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40';
    if (type === 'MS2') return 'bg-blue-500/20 text-blue-400 border-blue-500/40';
    return 'bg-gray-500/20 text-gray-400 border-gray-500/40';
  };

  // Seçenek değiştir (animasyonlu)
  const handleSwapOption = (matchIndex: number, clickedAlternative: any) => {
    setMatchSelections(prev => {
      const current = prev[matchIndex];
      if (!current) return prev;

      // Eski ana, alternatiflere gitsin
      const newAlternatives = [
        current.main,
        ...current.alternatives.filter(a => a.type !== clickedAlternative.type)
      ];

      return {
        ...prev,
        [matchIndex]: {
          main: clickedAlternative,
          alternatives: newAlternatives
        }
      };
    });
  };

  const totalOdds = Object.values(matchSelections).reduce((acc, selection) => {
    return acc * (selection?.main?.odds || 1);
  }, 1);

  const handleAddAll = () => {
    // Seçili ana önerileri kupona ekle
    const updatedRecommendations = initialRecommendations.map((rec, idx) => {
      const selection = matchSelections[idx];
      if (!selection) return rec;

      return {
        ...rec,
        recommendation: selection.main.type,
        recommended_odds: selection.main.odds,
        win_rate: selection.main.rate
      };
    });

    onClose();
    setTimeout(() => onAddToCoupon(updatedRecommendations), 200);
  };

  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-[60] flex items-end sm:items-center justify-center p-0 sm:p-4">
      <div className="bg-[#101027] rounded-t-3xl sm:rounded-3xl w-full sm:max-w-2xl max-h-[90vh] shadow-[0_0_60px_rgba(129,59,255,0.35)] border-t sm:border border-[rgba(139,76,255,0.30)] flex flex-col">
        
        <div className="relative bg-gradient-to-r from-[#813BFF] to-[#A04BFF] p-4 flex-shrink-0">
          <button onClick={onClose} className="absolute top-3 right-3 text-white/70 hover:text-white p-1 rounded-lg">
            <X size={20} />
          </button>
          <div className="flex items-center gap-2.5">
            <div className="bg-white/20 p-2 rounded-lg">
              <Sparkles size={20} className="text-white" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Akıllı Kupon Önerileri</h2>
              <p className="text-white/80 text-xs">{analyzedCount} maç analiz edildi</p>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4">
          {initialRecommendations.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-5xl mb-3">😔</div>
              <h3 className="text-lg font-bold text-white mb-2">Öneri Bulunamadı</h3>
              <p className="text-[#A5A5C5] text-sm">%75+ başarı oranına sahip maç bulunamadı</p>
            </div>
          ) : (
            <div className="space-y-3">
              {initialRecommendations.map((rec, i) => {
                const selection = matchSelections[i];
                const mainOption = selection?.main || {
                  type: rec.recommendation,
                  label: getRecommendationLabel(rec.recommendation),
                  odds: rec.recommended_odds,
                  rate: rec.win_rate
                };
                const alternatives = selection?.alternatives || rec.additional_insights || [];

                return (
                  <div key={i} className="bg-[#171633] border border-[rgba(139,76,255,0.25)] rounded-xl p-4">
                    <div className="flex justify-between gap-2 mb-3">
                      <div className="flex-1">
                        <p className="text-[#A5A5C5] text-[10px] mb-1">{rec.match.league}</p>
                        <p className="text-white font-bold text-sm">{rec.match.home_team} - {rec.match.away_team}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-[#A5A5C5] text-[10px]">Başarı</p>
                        <p className="text-[#00E99A] text-3xl font-black">%{mainOption.rate}</p>
                      </div>
                    </div>

                    {/* ANA ÖNERİ */}
                    <div className="mb-3">
                      <p className="text-[#A5A5C5] text-[10px] mb-2">📌 Ana Öneri:</p>
                      <div className="bg-[#101027] rounded-lg p-3 border border-[rgba(139,76,255,0.2)] transition-all duration-300 ease-in-out">
                        <div className="flex gap-2 items-center">
                          <div className={`px-3 py-1.5 rounded-lg border text-xs font-bold flex-1 transition-all duration-300 ${getRecommendationColor(mainOption.type)}`}>
                            {mainOption.label}
                          </div>
                          <div className="bg-[#813BFF]/20 border border-[#813BFF]/40 text-[#813BFF] font-black px-3 py-1.5 rounded-lg text-xs transition-all duration-300">
                            {mainOption.odds?.toFixed(2) || 'N/A'}
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* ALTERNATİFLER */}
                    {alternatives.length > 0 && (
                      <div>
                        <p className="text-[#A5A5C5] text-[10px] mb-2">💡 Bu Maçlarda Ayrıca:</p>
                        <div className="space-y-2">
                          {alternatives.map((alt, idx) => (
                            <div key={`${alt.type}-${idx}`} className="bg-[#101027]/50 rounded-lg p-2.5 border border-white/[0.05] flex items-center justify-between gap-2 group hover:border-[#813BFF]/30 transition-all duration-200">
                              <div className="flex-1">
                                <div className="flex items-center gap-2">
                                  <p className="text-white text-xs font-semibold">{alt.label}</p>
                                  {alt.odds && (
                                    <span className="bg-[#813BFF]/20 border border-[#813BFF]/30 text-[#813BFF] font-bold px-1.5 py-0.5 rounded text-[10px]">
                                      {alt.odds.toFixed(2)}
                                    </span>
                                  )}
                                </div>
                                <p className="text-[#00E99A] text-[10px] font-bold">
                                  %{alt.rate} ({alt.count}/{alt.total})
                                </p>
                              </div>
                              <button
                                onClick={() => handleSwapOption(i, alt)}
                                className="flex items-center gap-1 px-2.5 py-1.5 bg-[#813BFF]/10 hover:bg-[#813BFF]/20 text-[#813BFF] rounded-lg text-[10px] font-bold transition-all duration-200 border border-[#813BFF]/20 hover:border-[#813BFF]/40 active:scale-95"
                              >
                                <RefreshCw size={12} className="transition-transform duration-300 group-hover:rotate-180" />
                                <span>Değiştir</span>
                              </button>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* İSTATİSTİKLER */}
                    <div className="bg-[#101027] rounded-lg p-2.5 border border-[rgba(139,76,255,0.15)] mt-3">
                      <div className="flex items-center gap-1.5 mb-2">
                        <BarChart3 size={12} className="text-[#A5A5C5]" />
                        <p className="text-[#A5A5C5] text-[10px]">{rec.exact_matches} benzer maç</p>
                      </div>
                      
                      <div className="flex items-center justify-between text-xs">
                        <div className="flex gap-3">
                          <span className="text-[#00E99A] font-semibold">🏠 {rec.statistics.home_wins}</span>
                          <span className="text-[#F59E0B] font-semibold">🤝 {rec.statistics.draws}</span>
                          <span className="text-[#3B82F6] font-semibold">✈️ {rec.statistics.away_wins}</span>
                        </div>
                        
                        <span className="text-[#A5A5C5]">|</span>
                        
                        <div className="flex gap-2">
                          <span className="text-[#22C55E] font-semibold">⚽ Var: {rec.statistics.gg_yes}</span>
                          <span className="text-[#EF4444] font-semibold">⚽ Yok: {rec.statistics.gg_no}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <div className="bg-[#101027] border-t border-[rgba(139,76,255,0.25)] p-4 flex-shrink-0">
          <button
            onClick={handleAddAll}
            disabled={initialRecommendations.length === 0}
            className="w-full bg-gradient-to-r from-[#813BFF] to-[#A04BFF] text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <Ticket size={18} />
            <span>Kupona Ekle ({initialRecommendations.length} Maç)</span>
          </button>
        </div>

      </div>
    </div>
  );
}

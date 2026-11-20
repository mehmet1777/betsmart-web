'use client';

import { useState } from 'react';
import { X, Sparkles, BarChart3, Ticket, TrendingUp } from 'lucide-react';
import OddsAnalysisModal from './OddsAnalysisModal';

interface SmartCouponRecommendation {
  match: any;
  exact_matches: number;
  total_analyzed: number;
  win_rate: number;
  recommendation: string;
  recommendation_label?: string;
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
}

interface SmartCouponModalProps {
  isOpen: boolean;
  onClose: () => void;
  recommendations: SmartCouponRecommendation[];
  analyzedCount: number;
  onAddToCoupon: (recommendations: SmartCouponRecommendation[]) => void;
}

export default function SmartCouponModal({ isOpen, onClose, recommendations, analyzedCount, onAddToCoupon }: SmartCouponModalProps) {
  const [selectedMatchForAnalysis, setSelectedMatchForAnalysis] = useState<any | null>(null);
  
  if (!isOpen) return null;

  const getRecommendationLabel = (type: string) => {
    const labels: Record<string, string> = {
      'MS1': 'Ev Sahibi',
      'MSX': 'Beraberlik',
      'MS2': 'Deplasman',
      'GG_YES': '⚽ Karşılıklı Gol Var',
      'GG_NO': '🚫 Karşılıklı Gol Yok',
      'OVER_15': '📈 1.5 Üst',
      'OVER_25': '📈 2.5 Üst',
      'OVER_35': '📈 3.5 Üst',
      'HT_OVER_05': '🕐 İlk Yarı 0.5 Üst',
      'HT_OVER_15': '🕐 İlk Yarı 1.5 Üst',
      'HT_GG_YES': '🕐⚽ İlk Yarı KG Var'
    };
    return labels[type] || type;
  };

  const getRecommendationColor = (type: string) => {
    // Maç Sonucu
    if (type === 'MS1') return 'bg-[#00E99A]/20 text-[#00E99A] border-[#00E99A]/40';
    if (type === 'MSX') return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/40';
    if (type === 'MS2') return 'bg-blue-500/20 text-blue-400 border-blue-500/40';
    
    // KG
    if (type === 'GG_YES') return 'bg-green-500/20 text-green-400 border-green-500/40';
    if (type === 'GG_NO') return 'bg-red-500/20 text-red-400 border-red-500/40';
    
    // Alt/Üst
    if (type.startsWith('OVER_')) return 'bg-purple-500/20 text-purple-400 border-purple-500/40';
    
    // İlk Yarı
    if (type.startsWith('HT_')) return 'bg-orange-500/20 text-orange-400 border-orange-500/40';
    
    return 'bg-gray-500/20 text-gray-400 border-gray-500/40';
  };

  const totalOdds = recommendations.reduce((acc, rec) => acc * rec.recommended_odds, 1);

  const handleAddAll = () => {
    onClose();
    setTimeout(() => onAddToCoupon(recommendations), 200);
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
          {recommendations.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-5xl mb-3">😔</div>
              <h3 className="text-lg font-bold text-white mb-2">Öneri Bulunamadı</h3>
              <p className="text-[#A5A5C5] text-sm">%75+ başarı oranına sahip maç bulunamadı</p>
            </div>
          ) : (
            <div className="space-y-3">
              {recommendations.map((rec, i) => (
                <div key={i} className="bg-[#171633] border border-[rgba(139,76,255,0.25)] rounded-xl p-4">
                  <div className="flex justify-between gap-2 mb-3">
                    <div className="flex-1">
                      <p className="text-[#A5A5C5] text-[10px] mb-1">{rec.match.league}</p>
                      <p className="text-white font-bold text-sm">{rec.match.home_team} - {rec.match.away_team}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-[#A5A5C5] text-[10px]">Başarı</p>
                      <p className="text-[#00E99A] text-3xl font-black">%{rec.win_rate}</p>
                    </div>
                  </div>
                  <div className="flex gap-2 mb-3">
                    <div className={`px-3 py-1.5 rounded-lg border text-xs font-bold ${getRecommendationColor(rec.recommendation)}`}>
                      {getRecommendationLabel(rec.recommendation)}
                    </div>
                    {rec.recommended_odds > 0 && (
                      <div className="bg-[#813BFF]/20 border border-[#813BFF]/40 text-[#813BFF] font-black px-3 py-1.5 rounded-lg text-xs">
                        {rec.recommended_odds.toFixed(2)}
                      </div>
                    )}
                  </div>
                  <div className="bg-[#101027] rounded-lg p-2.5 border border-[rgba(139,76,255,0.15)]">
                    <div className="flex items-center gap-1.5 mb-2">
                      <BarChart3 size={12} className="text-[#A5A5C5]" />
                      <p className="text-[#A5A5C5] text-[10px]">{rec.exact_matches} benzer maç</p>
                    </div>
                    
                    <div className="flex items-center justify-between text-xs">
                      {/* Maç Sonuçları */}
                      <div className="flex gap-3">
                        <span className="text-[#00E99A] font-semibold">🏠 {rec.statistics.home_wins}</span>
                        <span className="text-[#F59E0B] font-semibold">🤝 {rec.statistics.draws}</span>
                        <span className="text-[#3B82F6] font-semibold">✈️ {rec.statistics.away_wins}</span>
                      </div>
                      
                      {/* Ayırıcı */}
                      <span className="text-[#A5A5C5]">|</span>
                      
                      {/* KG */}
                      <div className="flex gap-2">
                        <span className="text-[#22C55E] font-semibold">⚽ Var: {rec.statistics.gg_yes}</span>
                        <span className="text-[#EF4444] font-semibold">⚽ Yok: {rec.statistics.gg_no}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="bg-[#101027] border-t border-[rgba(139,76,255,0.25)] p-4 flex-shrink-0">
          <button
            onClick={handleAddAll}
            disabled={recommendations.length === 0}
            className="w-full bg-gradient-to-r from-[#813BFF] to-[#A04BFF] text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50"
          >
            <Ticket size={18} />
            <span>Kupona Ekle ({recommendations.length} Maç)</span>
          </button>
        </div>

      </div>
    </div>
  );
}

'use client';

import { useState, useEffect } from 'react';
import { X, ChevronRight } from 'lucide-react';
import { Match } from '@/types';

interface AnalysisResult {
  success: boolean;
  total_count: number;
  exact: any[];
  similar: any[];
  statistics: {
    home_wins: number;
    draws: number;
    away_wins: number;
    gg_yes: number;
    gg_no: number;
    total_valid: number;
  };
  recommendation?: {
    type: string;
    odds: number;
    confidence: string;
    reason: string;
    percentage: number;
  };
  message?: string;
}

interface OddsChange {
  detected_at: string;
  old_odd_1: number;
  new_odd_1: number;
  change_1: number;
  old_odd_x: number;
  new_odd_x: number;
  change_x: number;
  old_odd_2: number;
  new_odd_2: number;
  change_2: number;
  total_change: number;
}

interface OddsAnalysisModalProps {
  isOpen: boolean;
  onClose: () => void;
  match: Match;
}

export default function OddsAnalysisModal({ isOpen, onClose, match }: OddsAnalysisModalProps) {
  const [loading, setLoading] = useState(false);
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [oddsChanges, setOddsChanges] = useState<OddsChange[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [detailsModal, setDetailsModal] = useState<'exact' | 'similar' | null>(null);

  useEffect(() => {
    if (isOpen) {
      fetchAnalysis();
      setDetailsModal(null);
    }
  }, [isOpen]);

  const fetchAnalysis = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Oranları parse et - '-' stringi veya geçersiz değerler için 0 döndür
      const parseOdd = (oddStr: string | undefined) => {
        if (!oddStr || oddStr === '-' || oddStr === 'null') return 0;
        const parsed = parseFloat(oddStr);
        return isNaN(parsed) ? 0 : parsed;
      };

      const odd_1 = parseOdd(match.odds?.home);
      const odd_x = parseOdd(match.odds?.draw);
      const odd_2 = parseOdd(match.odds?.away);

      console.log('📊 Analiz isteği:', {
        odd_1,
        odd_x,
        odd_2,
        home_team: match.home.name,
        away_team: match.away.name,
        raw_odds: match.odds
      });

      // Validasyon - Frontend'de kontrol et
      if (odd_1 <= 0 || odd_x <= 0 || odd_2 <= 0 || isNaN(odd_1) || isNaN(odd_x) || isNaN(odd_2)) {
        setError('Bu maç için oranlar mevcut değil');
        setLoading(false);
        return;
      }

      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          odd_1,
          odd_x,
          odd_2,
          home_team: match.home.name,
          away_team: match.away.name
        })
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        console.error('❌ API Hatası:', errorData);
        throw new Error(errorData.error || 'Analiz yüklenemedi');
      }

      const data = await response.json();
      console.log('✅ Analiz sonucu:', data);
      setAnalysis(data);

      // Oran değişikliklerini de çek
      fetchOddsChanges();
      
    } catch (err) {
      console.error('❌ Fetch hatası:', err);
      setError(err instanceof Error ? err.message : 'Bir hata oluştu');
    } finally {
      setLoading(false);
    }
  };

  const fetchOddsChanges = async () => {
    try {
      const response = await fetch('/api/odds-changes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          home_team: match.home.name,
          away_team: match.away.name,
          // match_datetime opsiyonel, göndermeyelim
        })
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success && data.changes) {
          setOddsChanges(data.changes);
          console.log(`✅ ${data.changes.length} oran değişikliği bulundu`);
        }
      }
    } catch (err) {
      console.log('⚠️ Oran değişiklikleri alınamadı:', err);
    }
  };

  const calculateStats = (matches: any[]) => {
    const stats = { 
      home: 0, draw: 0, away: 0, total: 0,
      ht_home: 0, ht_draw: 0, ht_away: 0, ht_total: 0
    };
    
    matches.forEach(m => {
      const score = m.score?.trim();
      if (score && score.includes('-')) {
        try {
          const parts = score.split('-');
          const h = parseInt(parts[0].trim());
          const a = parseInt(parts[1].trim());
          if (!isNaN(h) && !isNaN(a)) {
            stats.total++;
            if (h > a) stats.home++;
            else if (h === a) stats.draw++;
            else stats.away++;
          }
        } catch (e) {
          // ignore
        }
      }

      const halfScore = m.half_score?.trim();
      if (halfScore && halfScore.includes('-')) {
        try {
          const parts = halfScore.split('-');
          const h = parseInt(parts[0].trim());
          const a = parseInt(parts[1].trim());
          if (!isNaN(h) && !isNaN(a)) {
            stats.ht_total++;
            if (h > a) stats.ht_home++;
            else if (h === a) stats.ht_draw++;
            else stats.ht_away++;
          }
        } catch (e) {
          // ignore
        }
      }
    });
    
    return stats;
  };

  const getStars = (percentage: number) => {
    if (percentage >= 60) return '⭐⭐⭐⭐⭐';
    if (percentage >= 50) return '⭐⭐⭐⭐';
    if (percentage >= 40) return '⭐⭐⭐';
    return '⭐⭐';
  };

  if (!isOpen) return null;

  const exactStats = analysis ? calculateStats(analysis.exact) : null;
  const similarStats = analysis ? calculateStats(analysis.similar) : null;

  return (
    <div>
      {/* MAIN MODAL */}
      <div className="fixed inset-0 z-[9999] flex items-center justify-center p-3 sm:p-4">
        <div 
          className="absolute inset-0 bg-[#080A18]/95 backdrop-blur-xl"
          onClick={onClose}
        />

        <div className="relative w-full max-w-md bg-gradient-to-b from-[#15152D] to-[#0D0E1F] rounded-[20px] shadow-2xl shadow-purple-900/20 max-h-[90vh] sm:max-h-[85vh] overflow-hidden flex flex-col border border-white/[0.08]">
          {/* Header */}
          <div className="flex-shrink-0 bg-gradient-to-r from-[#1a1a35]/90 to-[#15152D]/90 backdrop-blur-xl border-b border-white/[0.06] px-4 sm:px-6 py-4 sm:py-5 flex items-center justify-between">
            <div className="flex-1">
              <h3 className="text-base font-semibold text-[#F8FAFC] truncate">
                {match.home.name} - {match.away.name}
              </h3>
              <div className="flex items-center gap-2 mt-1.5 text-xs text-[#9295AC]">
                <span className="text-[#8B5CF6]">{match.odds?.home}</span>
                <span className="text-[#4a4b5c]">•</span>
                <span className="text-[#8B5CF6]">{match.odds?.draw}</span>
                <span className="text-[#4a4b5c]">•</span>
                <span className="text-[#8B5CF6]">{match.odds?.away}</span>
              </div>
            </div>
            <button
              onClick={onClose}
              className="w-9 h-9 rounded-xl bg-white/[0.05] flex items-center justify-center hover:bg-white/[0.1] transition-all ml-3 flex-shrink-0 border border-white/[0.06]"
            >
              <X className="w-4 h-4 text-[#9295AC]" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto px-4 sm:px-5 py-4 sm:py-5 bg-gradient-to-b from-transparent to-[#080A18]/30">
            {loading && (
              <div className="flex flex-col items-center justify-center py-20">
                <div className="relative">
                  <div className="animate-spin rounded-full h-16 w-16 border-[3px] border-[#8B5CF6]/20 border-t-[#8B5CF6]"></div>
                  <div className="absolute inset-0 rounded-full bg-[#8B5CF6]/10 blur-xl"></div>
                </div>
                <p className="text-[#9295AC] text-sm mt-5 font-medium">Analiz ediliyor...</p>
              </div>
            )}

            {error && (
              <div className="bg-gradient-to-br from-red-500/10 to-red-600/5 border border-red-500/20 rounded-[16px] p-4 shadow-lg shadow-red-900/10">
                <div className="flex items-start gap-3">
                  <div className="w-9 h-9 rounded-xl bg-red-500/10 flex items-center justify-center flex-shrink-0 border border-red-500/20">
                    <span className="text-red-400 text-lg">⚠</span>
                  </div>
                  <div className="flex-1">
                    <p className="text-red-400 font-semibold text-sm mb-1">Analiz Yapılamadı</p>
                    <p className="text-[#9295AC] text-xs leading-relaxed">{error}</p>
                    
                    {error.includes('oranlar mevcut değil') && (
                      <div className="mt-3 p-3 bg-[#15152D]/50 rounded-lg border border-white/[0.04]">
                        <p className="text-[#9295AC] text-xs">
                          💡 Bu maç için bahis oranları henüz açılmamış olabilir.
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {analysis && !loading && (
              <div className="space-y-3">
                {analysis.total_count > 0 ? (
                  <div className="space-y-3">
                    {/* EXACT MATCHES */}
                    {analysis.exact.length > 0 && exactStats && exactStats.total > 0 && (
                      <div className="relative bg-gradient-to-br from-[#8B5CF6]/10 via-[#6366F1]/5 to-transparent border border-[#8B5CF6]/20 rounded-[18px] p-4 sm:p-5 shadow-lg shadow-purple-900/10">
                        <div className="absolute inset-0 bg-gradient-to-br from-[#8B5CF6]/5 to-transparent rounded-[18px] opacity-50"></div>
                        
                        <div className="relative flex items-center justify-between mb-4">
                          <div className="flex items-center gap-2.5">
                            <div className="w-1.5 h-1.5 bg-[#8B5CF6] rounded-full shadow-lg shadow-purple-500/50"></div>
                            <h4 className="text-xs font-bold text-[#8B5CF6] uppercase tracking-wider">
                              Aynı Oranlar ({analysis.exact.length})
                            </h4>
                          </div>
                          <button
                            onClick={() => setDetailsModal('exact')}
                            className="flex items-center gap-1.5 px-3 py-1.5 bg-[#8B5CF6]/10 hover:bg-[#8B5CF6]/20 text-[#8B5CF6] rounded-lg transition-colors group border border-[#8B5CF6]/20"
                          >
                            <span className="text-xs font-semibold">📊 İstatistikler</span>
                            <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                          </button>
                        </div>

                        {(() => {
                          const results = [
                            { type: 'home', count: exactStats.home, label: 'Ev Sahibi', odds: match.odds?.home },
                            { type: 'draw', count: exactStats.draw, label: 'Beraberlik', odds: match.odds?.draw },
                            { type: 'away', count: exactStats.away, label: 'Deplasman', odds: match.odds?.away }
                          ];

                          // En yüksek olanı bul (öneri için)
                          const sortedResults = [...results].sort((a, b) => b.count - a.count);
                          const best = sortedResults[0];
                          const percentage = ((best.count / exactStats.total) * 100).toFixed(0);
                          
                          return (
                            <div className="relative bg-gradient-to-br from-[#1a1a35] to-[#15152D] rounded-[14px] p-5 mb-4 border border-white/[0.08] shadow-xl">
                              <div className="absolute inset-0 bg-gradient-to-br from-[#8B5CF6]/5 to-transparent rounded-[14px]"></div>
                              
                              <div className="relative flex items-center justify-between mb-3">
                                <div className="flex items-center gap-3">
                                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#8B5CF6]/20 to-[#6366F1]/10 flex items-center justify-center border border-[#8B5CF6]/20">
                                    <span className="text-2xl">{best.type === 'home' ? '🏠' : best.type === 'draw' ? '🤝' : '✈️'}</span>
                                  </div>
                                  <div>
                                    <p className="text-[#F8FAFC] font-bold text-base">{best.label}</p>
                                    <p className="text-[#9295AC] text-xs mt-0.5">{best.odds}</p>
                                  </div>
                                </div>
                                <div className="text-right">
                                  <p className="text-[#22C55E] font-bold text-2xl sm:text-3xl">{percentage}%</p>
                                  <p className="text-xs text-[#9295AC] mt-0.5">{getStars(parseInt(percentage))}</p>
                                </div>
                              </div>
                              
                              <p className="text-[#9295AC] text-xs mb-3">
                                {exactStats.total} maçta {best.count} kez gerçekleşti
                              </p>

                              <div className="grid grid-cols-3 gap-3">
                                {results.map((r) => (
                                  <div key={r.type} className="bg-[#080A18]/40 rounded-xl p-3 text-center border border-white/[0.04]">
                                    <p className="text-xl mb-1.5">{r.type === 'home' ? '🏠' : r.type === 'draw' ? '🤝' : '✈️'}</p>
                                    <p className="text-[#F8FAFC] font-bold text-lg">{r.count}</p>
                                    <p className="text-xs text-[#9295AC] mt-1">
                                      {((r.count / exactStats.total) * 100).toFixed(0)}%
                                    </p>
                                  </div>
                                ))}
                              </div>
                            </div>
                          );
                        })()}
                      </div>
                    )}

                    {/* SIMILAR MATCHES */}
                    {analysis.similar.length > 0 && similarStats && similarStats.total > 0 && (
                      <div className="relative bg-gradient-to-br from-[#6366F1]/10 via-[#8B5CF6]/5 to-transparent border border-[#6366F1]/20 rounded-[18px] p-4 sm:p-5 shadow-lg shadow-indigo-900/10">
                        <div className="absolute inset-0 bg-gradient-to-br from-[#6366F1]/5 to-transparent rounded-[18px] opacity-50"></div>
                        
                        <div className="relative flex items-center justify-between mb-4">
                          <div className="flex items-center gap-2.5">
                            <div className="w-1.5 h-1.5 bg-[#6366F1] rounded-full shadow-lg shadow-indigo-500/50"></div>
                            <h4 className="text-xs font-bold text-[#6366F1] uppercase tracking-wider">
                              Yakın Oranlar ({analysis.similar.length})
                            </h4>
                          </div>
                          <button
                            onClick={() => setDetailsModal('similar')}
                            className="flex items-center gap-1.5 px-3 py-1.5 bg-[#6366F1]/10 hover:bg-[#6366F1]/20 text-[#6366F1] rounded-lg transition-colors group border border-[#6366F1]/20"
                          >
                            <span className="text-xs font-semibold">📊 İstatistikler</span>
                            <ChevronRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 transition-transform" />
                          </button>
                        </div>

                        <div className="relative space-y-2">
                          {[
                            { label: 'Ev Sahibi', count: similarStats.home, icon: '🏠' },
                            { label: 'Beraberlik', count: similarStats.draw, icon: '🤝' },
                            { label: 'Deplasman', count: similarStats.away, icon: '✈️' }
                          ].map((item, idx) => (
                              <div key={idx} className="flex items-center justify-between text-sm bg-[#1a1a35]/50 rounded-xl p-2.5 border border-white/[0.04]">
                                <div className="flex items-center gap-2.5">
                                  <span className="text-base">{item.icon}</span>
                                  <span className="text-[#F8FAFC] font-medium">{item.label}</span>
                                </div>
                                <span className="text-[#F8FAFC] font-bold">
                                  {item.count} <span className="text-xs text-[#9295AC] font-normal">({((item.count/similarStats.total)*100).toFixed(0)}%)</span>
                                </span>
                              </div>
                            ))}
                        </div>
                      </div>
                    )}

                    {/* Summary */}
                    <div className="relative bg-gradient-to-r from-[#15152D]/80 to-[#1a1a35]/60 rounded-[16px] p-4 text-center border border-white/[0.06] backdrop-blur-sm">
                      <p className="text-xs text-[#9295AC]">
                        Toplam <span className="text-[#8B5CF6] font-bold">{(analysis.exact?.length || 0) + (analysis.similar?.length || 0)}</span> maç analiz edildi
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="relative bg-gradient-to-br from-[#15152D] to-[#1a1a35] rounded-[18px] p-8 text-center border border-white/[0.08] shadow-xl">
                    <div className="w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br from-[#8B5CF6]/10 to-[#6366F1]/5 flex items-center justify-center border border-[#8B5CF6]/20">
                      <span className="text-4xl">🔍</span>
                    </div>
                    <h3 className="text-[#F8FAFC] font-bold mb-2">Benzer Maç Bulunamadı</h3>
                    <p className="text-[#9295AC] text-sm mb-4">Bu oran kombinasyonu nadir görülüyor.</p>
                    <div className="bg-[#080A18]/50 rounded-xl p-3 text-left border border-white/[0.04]">
                      <p className="text-[#9295AC] text-xs leading-relaxed">
                        Sistem ±0.01 ve ±0.02 toleransla arama yaptı.
                      </p>
                    </div>
                  </div>
                )}

                {analysis.message && (
                  <div className="bg-gradient-to-br from-yellow-500/10 to-yellow-600/5 border border-yellow-500/20 rounded-[16px] p-4 shadow-lg shadow-yellow-900/10">
                    <p className="text-yellow-400 text-xs">{analysis.message}</p>
                  </div>
                )}

                {/* ORAN DEĞİŞİKLİKLERİ */}
                {oddsChanges.length > 0 && (
                  <div className="relative bg-gradient-to-br from-[#F59E0B]/10 via-[#EF4444]/5 to-transparent border border-[#F59E0B]/20 rounded-[18px] p-4 sm:p-5 shadow-lg shadow-orange-900/10">
                    <div className="absolute inset-0 bg-gradient-to-br from-[#F59E0B]/5 to-transparent rounded-[18px] opacity-50"></div>
                    
                    <div className="relative flex items-center gap-2.5 mb-4">
                      <div className="w-1.5 h-1.5 bg-[#F59E0B] rounded-full shadow-lg shadow-orange-500/50"></div>
                      <h4 className="text-xs font-bold text-[#F59E0B] uppercase tracking-wider">
                        Oran Değişiklik Geçmişi ({oddsChanges.length})
                      </h4>
                    </div>

                    <div className="relative space-y-3 max-h-80 overflow-y-auto pr-2 custom-scrollbar">
                      {oddsChanges.map((change, idx) => {
                        const date = new Date(change.detected_at);
                        const formattedDate = date.toLocaleDateString('tr-TR', { 
                          day: '2-digit', 
                          month: '2-digit',
                          year: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        });

                        return (
                          <div key={idx} className="bg-[#1a1a35]/50 rounded-xl p-3 border border-white/[0.04]">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-xs text-[#9295AC]">{formattedDate}</span>
                              <span className="text-xs font-bold text-[#F59E0B]">
                                Toplam: {change.total_change.toFixed(1)}%
                              </span>
                            </div>
                            
                            <div className="space-y-1.5">
                              {[
                                { label: 'MS1', old: change.old_odd_1, new: change.new_odd_1, change: change.change_1 },
                                { label: 'MSX', old: change.old_odd_x, new: change.new_odd_x, change: change.change_x },
                                { label: 'MS2', old: change.old_odd_2, new: change.new_odd_2, change: change.change_2 }
                              ].map((odd, i) => (
                                <div key={i} className="flex items-center justify-between text-xs">
                                  <span className="text-[#9295AC] font-medium w-10">{odd.label}:</span>
                                  <span className="text-[#F8FAFC]">
                                    {odd.old.toFixed(2)} → {odd.new.toFixed(2)}
                                  </span>
                                  <span className={`font-bold ml-auto ${
                                    odd.change > 0 ? 'text-green-400' : odd.change < 0 ? 'text-red-400' : 'text-[#9295AC]'
                                  }`}>
                                    {odd.change > 0 ? '+' : ''}{odd.change.toFixed(1)}%
                                  </span>
                                </div>
                              ))}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* DETAILS MODAL */}
      {detailsModal && analysis && (
        <div className="fixed inset-0 z-[10000] flex items-center justify-center p-3 sm:p-4">
          <div 
            className="absolute inset-0 bg-[#080A18]/98 backdrop-blur-2xl"
            onClick={() => setDetailsModal(null)}
          />

          <div className="relative w-full max-w-md bg-gradient-to-b from-[#15152D] to-[#0D0E1F] rounded-[20px] shadow-2xl shadow-purple-900/20 max-h-[92vh] sm:max-h-[90vh] overflow-hidden flex flex-col border border-white/[0.08]">
            {/* Header */}
            <div className="flex-shrink-0 bg-gradient-to-r from-[#1a1a35]/90 to-[#15152D]/90 backdrop-blur-xl border-b border-white/[0.06] px-4 sm:px-6 py-4 sm:py-5 flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-[#F8FAFC] flex items-center gap-2">
                  <span className={detailsModal === 'exact' ? 'text-[#8B5CF6]' : 'text-[#6366F1]'}>
                    {detailsModal === 'exact' ? '●' : '●'}
                  </span>
                  {detailsModal === 'exact' ? 'Aynı Oranlar' : 'Yakın Oranlar'}
                </h3>
                <p className="text-xs text-[#9295AC] mt-1">Detaylı istatistikler ve maç listesi</p>
              </div>
              <button
                onClick={() => setDetailsModal(null)}
                className="w-9 h-9 rounded-xl bg-white/[0.05] flex items-center justify-center hover:bg-white/[0.1] transition-all flex-shrink-0 border border-white/[0.06]"
              >
                <X className="w-4 h-4 text-[#9295AC]" />
              </button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto px-4 sm:px-5 py-4 sm:py-5 space-y-4 bg-gradient-to-b from-transparent to-[#080A18]/30">
              {(() => {
                const stats = detailsModal === 'exact' ? exactStats : similarStats;
                const matches = detailsModal === 'exact' ? analysis.exact : analysis.similar;
                const primaryColor = detailsModal === 'exact' ? '#8B5CF6' : '#6366F1';

                return (
                  <div>
                    {/* İlk Yarı Stats */}
                    {stats && stats.ht_total > 0 && (
                      <div className="relative bg-gradient-to-br from-[#8B5CF6]/10 via-[#6366F1]/5 to-transparent border border-[#8B5CF6]/20 rounded-[18px] p-5 mb-4 shadow-lg shadow-purple-900/10">
                        <div className="absolute inset-0 bg-gradient-to-br from-[#8B5CF6]/5 to-transparent rounded-[18px] opacity-50"></div>
                        
                        <p className="relative text-xs font-bold uppercase tracking-wider mb-4" style={{ color: primaryColor }}>
                          İlk Yarı Sonuçları
                        </p>
                        <div className="relative grid grid-cols-3 gap-3">
                          {[
                            { emoji: '🏠', count: stats.ht_home },
                            { emoji: '🤝', count: stats.ht_draw },
                            { emoji: '✈️', count: stats.ht_away }
                          ].map((item, idx) => (
                            <div key={idx} className="bg-gradient-to-br from-[#1a1a35] to-[#15152D] rounded-[14px] p-4 text-center border border-white/[0.08] shadow-xl">
                              <div className="w-10 h-10 mx-auto mb-2 rounded-xl bg-gradient-to-br from-[#8B5CF6]/10 to-[#6366F1]/5 flex items-center justify-center border border-[#8B5CF6]/20">
                                <span className="text-xl">{item.emoji}</span>
                              </div>
                              <p className="text-[#F8FAFC] font-bold text-2xl mb-1">{item.count}</p>
                              <p className="text-xs text-[#9295AC]">
                                {((item.count / stats.ht_total) * 100).toFixed(0)}%
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Maç Listesi */}
                    <div className="space-y-3">
                      <div className="flex items-center justify-between px-1">
                        <p className="text-xs font-bold uppercase tracking-wider text-[#9295AC]">
                          Maç Detayları
                        </p>
                        <span className="text-xs text-[#9295AC] bg-white/[0.05] px-2.5 py-1 rounded-lg border border-white/[0.06]">
                          {matches.length}
                        </span>
                      </div>
                      
                      <div className="space-y-2">
                        {matches.slice(0, 100).map((m: any, idx: number) => {
                          // Oran bilgilerini parse et
                          const hasOdds = m.odd_1 && m.odd_x && m.odd_2;
                          
                          return (
                            <div 
                              key={idx} 
                              className="relative bg-gradient-to-br from-[#15152D]/90 to-[#1a1a35]/70 backdrop-blur-sm rounded-[16px] p-4 border border-white/[0.08] hover:border-[#8B5CF6]/30 hover:shadow-lg hover:shadow-purple-900/10 transition-all group"
                            >
                              <div className="absolute inset-0 bg-gradient-to-br from-[#8B5CF6]/0 group-hover:from-[#8B5CF6]/5 to-transparent rounded-[16px] transition-all"></div>
                              
                              {/* Main Row - Teams + Score */}
                              <div className="relative flex items-center justify-between gap-4">
                                <div className="flex items-center gap-3 flex-1 min-w-0">
                                  <div className="flex-1 min-w-0">
                                    <p className="text-[#F8FAFC] text-sm font-semibold truncate">
                                      {m.home_team}
                                    </p>
                                  </div>
                                  
                                  <div className="flex-shrink-0">
                                    <div className="bg-gradient-to-br from-[#22C55E]/20 to-[#22C55E]/10 rounded-lg px-3 py-1.5 border border-[#22C55E]/20 shadow-lg shadow-green-900/10">
                                      <span className="text-[#22C55E] font-bold text-sm tabular-nums">
                                        {m.score || '?-?'}
                                      </span>
                                    </div>
                                  </div>
                                  
                                  <div className="flex-1 min-w-0 text-right">
                                    <p className="text-[#F8FAFC] text-sm font-semibold truncate">
                                      {m.away_team}
                                    </p>
                                  </div>
                                </div>
                              </div>

                              {/* Half Score - Center */}
                              {m.half_score && m.half_score !== '?-?' && (
                                <div className="relative mt-2 text-center">
                                  <span className="text-[#9295AC] text-xs font-medium">
                                    İY: <span className="text-[#F8FAFC] font-semibold tabular-nums">{m.half_score}</span>
                                  </span>
                                </div>
                              )}

                              {/* Odds - Center with dashes */}
                              {hasOdds && (
                                <div className="relative mt-2 text-center">
                                  <span className="text-[#8B5CF6] text-xs font-bold tabular-nums">
                                    {typeof m.odd_1 === 'number' ? m.odd_1.toFixed(2) : m.odd_1}
                                    <span className="text-[#9295AC] mx-1.5">-</span>
                                    {typeof m.odd_x === 'number' ? m.odd_x.toFixed(2) : m.odd_x}
                                    <span className="text-[#9295AC] mx-1.5">-</span>
                                    {typeof m.odd_2 === 'number' ? m.odd_2.toFixed(2) : m.odd_2}
                                  </span>
                                </div>
                              )}
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                );
              })()}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

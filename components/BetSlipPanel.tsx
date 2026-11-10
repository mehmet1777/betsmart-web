'use client';

import { useState } from 'react';
import { BetSelection } from '@/types';
import { X, TrendingUp, Trash2, Sparkles, ChevronUp, ChevronDown } from 'lucide-react';

interface BetSlipPanelProps {
  selections: BetSelection[];
  onRemove: (matchId: number) => void;
  onClear: () => void;
  isMobileOpen: boolean;
  onMobileToggle: () => void;
}

export default function BetSlipPanel({ selections, onRemove, onClear, isMobileOpen, onMobileToggle }: BetSlipPanelProps) {
  const [analyzing, setAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  const handleAnalyze = async () => {
    if (selections.length === 0) return;

    setAnalyzing(true);
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ selections })
      });

      if (response.ok) {
        const data = await response.json();
        setAnalysisResult(data.analysis);
      }
    } catch (error) {
      console.error('Analiz hatası:', error);
    } finally {
      setAnalyzing(false);
    }
  };

  const getPredictionText = (prediction: '1' | 'X' | '2') => {
    switch (prediction) {
      case '1': return 'Ev Sahibi';
      case 'X': return 'Beraberlik';
      case '2': return 'Deplasman';
    }
  };

  return (
    <>
      {/* Mobile Toggle Button (Fixed Bottom) */}
      <button
        onClick={onMobileToggle}
        className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-bg-primary/95 backdrop-blur-xl border-t border-border-primary px-5 py-4 flex items-center justify-between shadow-editorial-lg"
      >
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 gradient-accent rounded-xl flex items-center justify-center shadow-editorial">
            <span className="text-bg-primary font-bold text-base">{selections.length}</span>
          </div>
          <div className="text-left">
            <p className="text-sm font-bold text-text-primary tracking-tight">Kuponum</p>
            <p className="text-xs text-text-tertiary font-medium">{selections.length} maç seçildi</p>
          </div>
        </div>
        {isMobileOpen ? (
          <ChevronDown className="w-5 h-5 text-text-secondary" />
        ) : (
          <ChevronUp className="w-5 h-5 text-text-secondary" />
        )}
      </button>

      {/* Mobile Overlay */}
      {isMobileOpen && (
        <div 
          className="lg:hidden fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
          onClick={onMobileToggle}
        />
      )}

      {/* Panel */}
      <aside className={`
        fixed right-0 z-50 bg-bg-secondary border-l border-border-primary flex flex-col
        lg:w-80 lg:h-screen lg:top-0
        w-full h-[85vh] rounded-t-2xl
        transition-transform duration-300 ease-out
        lg:translate-y-0
        ${isMobileOpen ? 'bottom-0 translate-y-0' : 'translate-y-full lg:translate-y-0'}
      `}>
        {/* Mobile Handle */}
        <div className="lg:hidden flex justify-center pt-3 pb-2">
          <div className="w-12 h-1 bg-border-primary rounded-full"></div>
        </div>

        {/* Header */}
        <div className="px-6 py-5 border-b border-border-primary">
          <div className="flex items-center justify-between mb-2">
            <h2 className="heading-md">Kuponum</h2>
            {selections.length > 0 && (
              <button
                onClick={onClear}
                className="p-1.5 text-text-tertiary hover:text-red-400 premium-hover rounded"
              >
                <Trash2 className="w-4 h-4" />
              </button>
            )}
          </div>
          <p className="body-sm text-text-tertiary">
            {selections.length} maç seçildi
          </p>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-6 py-6">
          {selections.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="w-14 h-14 bg-bg-elevated rounded-xl flex items-center justify-center mb-4 editorial-border">
                <TrendingUp className="w-6 h-6 text-text-muted" />
              </div>
              <h3 className="heading-md mb-2">Kupon Boş</h3>
              <p className="body-md text-text-tertiary">
                Maçları seçerek kuponunuzu oluşturun
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {selections.map(selection => (
                <div
                  key={selection.matchId}
                  className="group bg-bg-tertiary editorial-border rounded-lg p-4 hover:border-border-accent premium-hover"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1 pr-2">
                      <p className="text-text-primary font-semibold text-sm leading-snug tracking-tight">
                        {selection.match.home.name}
                      </p>
                      <p className="text-text-primary font-semibold text-sm leading-snug tracking-tight mt-0.5">
                        {selection.match.away.name}
                      </p>
                      <p className="body-sm text-text-muted mt-1.5">
                        {selection.match.time}
                      </p>
                    </div>
                    <button
                      onClick={() => onRemove(selection.matchId)}
                      className="text-text-muted hover:text-red-400 premium-hover"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="flex items-center justify-between pt-3 border-t border-border-secondary">
                    <span className="body-sm text-text-tertiary">Seçim</span>
                    <span className="body-sm font-bold px-2.5 py-1 bg-active-overlay text-accent-primary rounded-md border border-border-accent">
                      {getPredictionText(selection.prediction)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Analyze Button */}
          {selections.length > 0 && (
            <button
              onClick={handleAnalyze}
              disabled={analyzing}
              className="w-full mt-6 gradient-accent text-bg-primary font-bold py-3.5 rounded-lg premium-hover disabled:opacity-50 disabled:cursor-not-allowed shadow-editorial-lg"
            >
              {analyzing ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="animate-spin rounded-full h-4 w-4 border-2 border-bg-primary border-t-transparent"></div>
                  Analiz Ediliyor...
                </span>
              ) : (
                <span className="flex items-center justify-center gap-2">
                  <Sparkles className="w-4 h-4" />
                  Akıllı Analiz Yap
                </span>
              )}
            </button>
          )}

          {/* Analysis Results */}
          {analysisResult && (
            <div className="mt-6 bg-bg-tertiary editorial-border rounded-lg p-5 space-y-4">
              <h3 className="heading-md text-sm flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-accent-primary" />
                Analiz Sonuçları
              </h3>
              
              <div className="grid grid-cols-2 gap-3">
                <div className="bg-bg-elevated editorial-border rounded-lg p-3">
                  <p className="body-sm text-text-tertiary mb-1.5">Toplam Maç</p>
                  <p className="text-2xl font-bold text-text-primary tracking-tight">{analysisResult.totalMatches}</p>
                </div>
                <div className="bg-bg-elevated editorial-border rounded-lg p-3">
                  <p className="body-sm text-text-tertiary mb-1.5">İhtimal</p>
                  <p className="text-2xl font-bold gradient-text tracking-tight">{analysisResult.winProbability}%</p>
                </div>
              </div>

              <div className="space-y-2.5 pt-3 border-t border-border-secondary">
                {[
                  { label: 'Ev Sahibi', value: analysisResult.homeWins, color: 'text-accent-primary' },
                  { label: 'Beraberlik', value: analysisResult.draws, color: 'text-accent-amber' },
                  { label: 'Deplasman', value: analysisResult.awayWins, color: 'text-accent-blue' }
                ].map((stat, i) => (
                  <div key={i} className="flex items-center justify-between">
                    <span className="body-md text-text-tertiary">{stat.label}</span>
                    <span className={`body-md font-bold ${stat.color}`}>{stat.value}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-border-primary bg-bg-primary/50">
          <div className="text-center">
            <p className="body-sm text-text-muted">
              Veri Tabanı: <span className="gradient-text font-bold">38,089</span> Maç
            </p>
          </div>
        </div>
      </aside>
    </>
  );
}

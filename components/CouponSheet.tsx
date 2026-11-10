'use client';

import { useState } from 'react';
import { X, Trash2, Ticket } from 'lucide-react';
import { BetSelection } from '@/types';

interface CouponSheetProps {
  isOpen: boolean;
  onClose: () => void;
  selections: BetSelection[];
  totalOdds: number;
  onRemove: (matchId: number) => void;
  onClear: () => void;
}

export default function CouponSheet({ isOpen, onClose, selections, totalOdds, onRemove, onClear }: CouponSheetProps) {
  const [betAmount, setBetAmount] = useState<string>('100');

  const getPredictionLabel = (prediction: '1' | 'X' | '2') => {
    return prediction;
  };

  // Gerçek odds değerini al
  const getOddsForSelection = (selection: BetSelection) => {
    const { match, prediction } = selection;
    if (!match.odds) return 1.50;
    
    switch (prediction) {
      case '1': return parseFloat(match.odds.home);
      case 'X': return parseFloat(match.odds.draw);
      case '2': return parseFloat(match.odds.away);
    }
  };

  const formatDate = (timeStr: string) => {
    // "DD.MM.YYYY HH:MM" formatından sadece tarih ve saat
    return timeStr.replace(' ', ' • ');
  };

  const potentialWin = betAmount ? (parseFloat(betAmount) * totalOdds).toFixed(2) : '0.00';

  // Türkçe sayı formatı: 123.456,78
  const formatTurkishNumber = (value: string) => {
    const [integer, decimal] = value.split('.');
    const formattedInteger = integer.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return `${formattedInteger},${decimal}`;
  };

  const formattedWin = formatTurkishNumber(potentialWin);
  const formattedOdds = totalOdds.toFixed(2).replace('.', ',');

  // Dinamik font boyutu - rakam uzunluğuna göre
  const getOddsFontSize = (value: string) => {
    if (value.length <= 6) return 'text-2xl'; // 123,45
    if (value.length <= 8) return 'text-xl';  // 12.345,67
    if (value.length <= 11) return 'text-lg'; // 1.234.567,89
    return 'text-base'; // Daha uzun
  };

  const getWinFontSize = (value: string) => {
    if (value.length <= 9) return 'text-2xl';  // 12.345,67
    if (value.length <= 12) return 'text-xl';  // 123.456.789,01
    if (value.length <= 15) return 'text-lg';  // 1.234.567.890,12
    return 'text-base'; // Daha uzun
  };

  return (
    <>
      {/* Backdrop Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/80 z-50 transition-opacity"
          onClick={onClose}
        />
      )}

      {/* Bottom Sheet - Tam Ekran Kupon */}
      <div className={`
        fixed inset-0 z-50 bg-[#0A0E13] flex flex-col
        transition-transform duration-300 ease-out
        ${isOpen ? 'translate-y-0' : 'translate-y-full'}
      `}>
        {/* Header - Gradient Background */}
        <div className="bg-gradient-to-br from-[#0D1821] to-[#0A0E13] px-5 py-4 flex items-center justify-between border-b border-gray-800/50">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-accent-primary/10 rounded-lg flex items-center justify-center border border-accent-primary/30">
              <Ticket className="w-5 h-5 text-accent-primary" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Kuponum</h2>
              <p className="text-xs text-gray-400">{selections.length} maç seçildi</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {selections.length > 0 && (
              <button
                onClick={onClear}
                className="p-2 text-gray-400 hover:text-white transition-colors"
              >
                <Trash2 className="w-5 h-5" />
              </button>
            )}
            <button
              onClick={onClose}
              className="p-2 text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Content - Scrollable */}
        <div className="flex-1 overflow-y-auto px-4 py-4">
          {selections.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 text-center">
              <div className="w-20 h-20 bg-gray-800/50 rounded-2xl flex items-center justify-center mb-4 border border-gray-700/50">
                <Ticket className="w-10 h-10 text-gray-600" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">Kupon Boş</h3>
              <p className="text-sm text-gray-400">
                Maçları seçerek kuponunuzu oluşturun
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {selections.map((selection) => {
                const odds = getOddsForSelection(selection);
                
                return (
                  <div
                    key={selection.matchId}
                    className="bg-gradient-to-br from-[#141B24] to-[#0F1419] rounded-2xl p-4 border border-gray-800/50 relative shadow-lg shadow-accent-primary/5"
                  >
                    {/* Remove Button - Top Right */}
                    <button
                      onClick={() => onRemove(selection.matchId)}
                      className="absolute top-3 right-3 p-1.5 text-gray-500 hover:text-gray-300 transition-colors"
                    >
                      <X className="w-4 h-4" />
                    </button>

                    {/* Date & Time with Trophy */}
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-lg">🏆</span>
                      <span className="text-xs text-gray-400 font-medium">
                        {formatDate(selection.match.time)}
                      </span>
                    </div>

                    {/* Teams */}
                    <div className="flex items-center justify-between pr-20">
                      <div className="space-y-2.5">
                        {/* Home Team */}
                        <div className="flex items-center gap-2.5">
                          <div className="w-8 h-8 bg-gradient-to-br from-gray-700 to-gray-800 rounded-full flex items-center justify-center flex-shrink-0 border border-gray-700/50">
                            <span className="text-sm">🏠</span>
                          </div>
                          <span className="text-sm font-semibold text-white">
                            {selection.match.home.name}
                          </span>
                        </div>
                        {/* Away Team */}
                        <div className="flex items-center gap-2.5">
                          <div className="w-8 h-8 bg-gradient-to-br from-gray-700 to-gray-800 rounded-full flex items-center justify-center flex-shrink-0 border border-gray-700/50">
                            <span className="text-sm">✈️</span>
                          </div>
                          <span className="text-sm font-semibold text-white">
                            {selection.match.away.name}
                          </span>
                        </div>
                      </div>

                      {/* Prediction Badge & Odds - Right Side */}
                      <div className="absolute right-4 top-1/2 -translate-y-1/2 flex items-center gap-3">
                        <div className="w-10 h-10 bg-accent-primary/10 rounded-xl flex items-center justify-center border-2 border-accent-primary">
                          <span className="text-base font-bold text-accent-primary">
                            {getPredictionLabel(selection.prediction)}
                          </span>
                        </div>
                        <span className="text-2xl font-bold text-accent-primary">
                          {odds.toFixed(2)}
                        </span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Footer - Fixed Bottom Summary */}
        {selections.length > 0 && (
          <div className="px-5 pb-6 pt-4 bg-gradient-to-t from-[#0D1117] to-[#0A0E13] border-t border-gray-800/50">
            {/* Toplam Oran ve Olası Kazanç */}
            <div className="flex items-center justify-between mb-4 px-1">
              {/* Toplam Oran */}
              <div className="flex-1">
                <p className="text-xs text-gray-400 mb-1">Toplam Oran</p>
                <div className="flex items-center gap-2">
                  <span className="text-xl flex-shrink-0">💰</span>
                  <span className={`${getOddsFontSize(formattedOdds)} font-black text-accent-primary`}>
                    {formattedOdds}
                  </span>
                </div>
              </div>

              {/* Divider */}
              <div className="w-px h-12 bg-gray-800 mx-3 flex-shrink-0"></div>

              {/* Olası Kazanç */}
              <div className="flex-1 text-right">
                <p className="text-xs text-gray-400 mb-1">Olası Kazanç</p>
                <div className="flex items-center gap-2 justify-end">
                  <span className="text-xl flex-shrink-0">🏆</span>
                  <span className={`${getWinFontSize(formattedWin)} font-black text-white`}>
                    {formattedWin} ₺
                  </span>
                </div>
              </div>
            </div>

            {/* Kuponu Oyna Butonu */}
            <button className="w-full bg-gradient-to-r from-accent-primary to-[#15D67D] hover:opacity-90 text-[#0A0E13] font-bold py-4 rounded-xl transition-all shadow-xl shadow-accent-primary/20 flex items-center justify-center gap-2">
              <Ticket className="w-5 h-5" />
              <span className="text-base">Kuponu Oyna</span>
            </button>
          </div>
        )}
      </div>
    </>
  );
}

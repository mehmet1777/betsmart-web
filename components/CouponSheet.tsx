'use client';

import { useState } from 'react';
import { X, Trash2, Ticket, Minus, Plus, Bookmark } from 'lucide-react';
import { BetSelection } from '@/types';
import Toast from './Toast';

interface CouponSheetProps {
  isOpen: boolean;
  onClose: () => void;
  selections: BetSelection[];
  totalOdds: number;
  onRemove: (matchId: number) => void;
  onClear: () => void;
}

export default function CouponSheet({ isOpen, onClose, selections, totalOdds, onRemove, onClear }: CouponSheetProps) {
  const [betAmount, setBetAmount] = useState<number>(100);
  const [isSaving, setIsSaving] = useState(false);
  const [showToast, setShowToast] = useState(false);
  const [toastData, setToastData] = useState({ title: '', message: '', type: 'success' as const });

  const getPredictionLabel = (prediction: '1' | 'X' | '2') => {
    return prediction;
  };

  const getOddsForSelection = (selection: BetSelection) => {
    const { match, prediction } = selection;
    if (!match.odds) return 1.50;
    
    switch (prediction) {
      case '1': return parseFloat(match.odds.home);
      case 'X': return parseFloat(match.odds.draw);
      case '2': return parseFloat(match.odds.away);
    }
  };

  const formatTurkishCurrency = (value: number) => {
    return new Intl.NumberFormat('tr-TR', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  };

  const formatDateTime = (timeStr: string) => {
    const parts = timeStr.split(' ');
    return `${parts[0]} • ${parts[1]}`;
  };

  const increaseBet = () => {
    setBetAmount(betAmount + 50);
  };

  const decreaseBet = () => {
    if (betAmount > 50) {
      setBetAmount(betAmount - 50);
    }
  };

  const potentialWin = betAmount * totalOdds;

  const saveCoupon = async () => {
    // Validasyon
    if (selections.length === 0) {
      alert('Kuponda en az 1 maç olmalıdır');
      return;
    }

    if (betAmount <= 0) {
      alert('Lütfen geçerli bir tutar girin');
      return;
    }

    setIsSaving(true);

    try {
      // 6 haneli rastgele ID oluştur
      const randomId = Math.floor(100000 + Math.random() * 900000).toString();
      
      const coupon = {
        id: Date.now().toString(),
        name: `#${randomId}`,
        date: new Date().toISOString(),
        selections: selections,
        totalOdds: totalOdds,
        betAmount: betAmount,
        potentialWin: potentialWin,
        status: 'pending' as const,
        actualWin: undefined,
      };

      if (typeof window !== 'undefined') {
        const stored = localStorage.getItem('savedCoupons');
        const coupons = stored ? JSON.parse(stored) : [];
        
        // Aynı kuponun tekrar kaydedilmesini önle (son 5 saniye içinde)
        const recentCoupon = coupons.find((c: any) => 
          Date.now() - parseInt(c.id) < 5000 &&
          c.selections.length === selections.length &&
          c.totalOdds === totalOdds
        );
        
        if (recentCoupon) {
          alert('Bu kupon zaten kaydedildi!');
          setIsSaving(false);
          return;
        }

        coupons.unshift(coupon);
        localStorage.setItem('savedCoupons', JSON.stringify(coupons));
      }

      // Başarı mesajı - TOAST
      setToastData({
        title: 'Kupon Kaydedildi! ✅',
        message: `🎫 Kupon: ${coupon.name}\n💰 Yatırılan: ${formatTurkishCurrency(betAmount)} ₺\n🏆 Olası Kazanç: ${formatTurkishCurrency(potentialWin)} ₺`,
        type: 'success'
      });
      setShowToast(true);
      
      // Kuponu temizle ve kapat
      setTimeout(() => {
        onClear();
        onClose();
      }, 500);
      
    } catch (error) {
      console.error('Kupon kaydetme hatası:', error);
      alert('Kupon kaydedilirken bir hata oluştu');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <>
      {/* Toast Notification */}
      <Toast
        show={showToast}
        onClose={() => setShowToast(false)}
        title={toastData.title}
        message={toastData.message}
        type={toastData.type}
        duration={4000}
      />

      {/* Backdrop Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/90 z-50 transition-opacity backdrop-blur-sm"
          onClick={onClose}
        />
      )}

      {/* Full Screen Coupon Sheet */}
      <div className={`
        fixed inset-0 z-[60] flex flex-col
        transition-transform duration-300 ease-out
        bg-[#0A0E13]
        ${isOpen ? 'translate-y-0' : 'translate-y-full'}
      `}>
        {/* Header */}
        <div className="relative px-3 pt-3 pb-2 overflow-hidden">
          {/* Neon glow beams - AZALTILMIŞ */}
          <div className="absolute top-0 left-0 w-64 h-64 pointer-events-none opacity-40">
            <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-[#19E98B]/10 via-[#19E98B]/5 to-transparent blur-2xl"></div>
          </div>
          
          <div className="relative flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 bg-gradient-to-br from-[#19E98B]/20 to-[#19E98B]/5 rounded-xl flex items-center justify-center border border-[#19E98B]/30 shadow-lg relative">
                <Ticket className="w-5 h-5 text-[#19E98B] relative z-10" strokeWidth={2.5} />
              </div>
              <div>
                <h2 className="text-base font-black text-white tracking-tight">Kupon Oluştur</h2>
                <p className="text-[10px] text-gray-400 font-medium">Seçtiğiniz maçlar kuponunuzda</p>
              </div>
            </div>
            <button
              onClick={onClear}
              className="px-2.5 py-1.5 bg-gray-900/60 hover:bg-gray-800/80 text-white text-[10px] font-semibold rounded-lg border border-gray-700/50 transition-all flex items-center gap-1"
            >
              <Trash2 className="w-3 h-3" />
              Temizle
            </button>
          </div>
        </div>

        {/* Content - Scrollable */}
        <div className="flex-1 overflow-y-auto px-3 pb-3 scrollbar-thin scrollbar-thumb-gray-700 scrollbar-track-transparent">
          {selections.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-12 text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-[#19E98B]/10 to-transparent rounded-2xl flex items-center justify-center mb-3 border border-[#19E98B]/20 shadow-xl">
                <Ticket className="w-8 h-8 text-[#19E98B]/40" />
              </div>
              <h3 className="text-lg font-bold text-white mb-1">Kupon Boş</h3>
              <p className="text-xs text-gray-400 max-w-sm leading-relaxed">
                Maç bülteninden maçları seçerek kuponunuzu oluşturun
              </p>
            </div>
          ) : (
            <>
              {/* Seçilen Maçlar - Ana Kart İÇİNDE Maçlar */}
              <div className="bg-gradient-to-br from-[#0D2820] via-[#0A1A15] to-[#0A0E13] rounded-xl p-2.5 mb-2.5 border border-[#19E98B]/20 relative overflow-hidden shadow-lg">
                <div className="absolute inset-0 bg-gradient-to-br from-[#19E98B]/5 to-transparent pointer-events-none"></div>
                
                {/* Header */}
                <div className="relative flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <div className="w-8 h-8 bg-[#19E98B] rounded-lg flex items-center justify-center shadow-lg">
                      <span className="text-base font-black text-[#0A0E13]">{selections.length}</span>
                    </div>
                    <h3 className="text-sm font-black text-white">Seçilen Maçlar</h3>
                  </div>
                  <div className="flex items-center gap-1">
                    <span className="text-[10px] text-gray-400 font-medium">Toplam Oran:</span>
                    <span className="text-base font-black text-[#19E98B]">{totalOdds.toFixed(2)}</span>
                    <svg className="w-3.5 h-3.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 15l7-7 7 7" />
                    </svg>
                  </div>
                </div>

                {/* Maç Listesi - Kart İçinde */}
                <div className="relative space-y-1.5">
                  {selections.map((selection) => {
                    const odds = getOddsForSelection(selection);
                    
                    return (
                      <div
                        key={selection.matchId}
                        className="relative bg-[#0F1419]/50 rounded-lg px-2.5 py-2 border border-gray-800/50 hover:border-gray-700/50 transition-all"
                      >
                        {/* Date & Time */}
                        <div className="flex items-center gap-1 mb-1.5">
                          <svg className="w-3 h-3 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                          </svg>
                          <span className="text-[10px] text-gray-400 font-medium">
                            {formatDateTime(selection.match.time)}
                          </span>
                        </div>

                        {/* Teams and Odds */}
                        <div className="flex items-center justify-between gap-2">
                          {/* Left: Soccer Icon + Teams */}
                          <div className="flex items-center gap-2 flex-1 min-w-0">
                            <div className="w-9 h-9 bg-[#1A2028] rounded-full flex items-center justify-center flex-shrink-0">
                              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                              </svg>
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="font-bold text-white text-sm leading-tight truncate">
                                {selection.match.home.name}
                              </div>
                              <div className="font-semibold text-gray-400 text-sm leading-tight truncate">
                                {selection.match.away.name}
                              </div>
                              <div className="flex items-center gap-1 mt-0.5">
                                <div className="h-0.5 w-0.5 bg-[#19E98B] rounded-full"></div>
                                <span className="text-[9px] text-gray-400">Maç Sonucu</span>
                                <span className="text-[9px] text-gray-600">•</span>
                                <span className="text-[9px] font-bold text-white">{getPredictionLabel(selection.prediction)}</span>
                              </div>
                            </div>
                          </div>

                          {/* Right: Odds + X */}
                          <div className="flex items-center gap-1.5 flex-shrink-0">
                            <div className="px-2.5 py-1 bg-transparent rounded-lg border border-[#19E98B] shadow-md">
                              <span className="text-lg font-black text-[#19E98B]">
                                {odds.toFixed(2)}
                              </span>
                            </div>
                            <button
                              onClick={() => onRemove(selection.matchId)}
                              className="w-6 h-6 hover:bg-gray-800 rounded-lg transition-colors flex items-center justify-center group"
                            >
                              <X className="w-3.5 h-3.5 text-gray-500 group-hover:text-white transition-colors" strokeWidth={2.5} />
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Kupon Özeti - REFERANS GÖRSELDEKİ GİBİ */}
              <div className="bg-gradient-to-br from-[#0D1621] to-[#0A0E13] rounded-xl p-3 border border-gray-800/60 shadow-xl mb-2.5">
                {/* Başlık */}
                <div className="flex items-center gap-1.5 mb-3">
                  <svg className="w-4 h-4 text-[#19E98B]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  <h3 className="text-sm font-black text-white">Kupon Özeti</h3>
                </div>

                {/* Toplam Oran ve Olası Kazanç - Flex Layout */}
                <div className="flex items-stretch gap-0 mb-3">
                  {/* Toplam Oran */}
                  <div className="flex-1 bg-[#0F1419] p-2.5 rounded-l-lg">
                    <p className="text-[10px] text-gray-400 mb-1 font-medium">Toplam Oran</p>
                    <p className="text-2xl font-black text-[#19E98B]">
                      {totalOdds.toFixed(2)}
                    </p>
                  </div>

                  {/* Vertical Divider */}
                  <div className="w-px bg-gray-800/50"></div>

                  {/* Olası Kazanç */}
                  <div className="flex-1 bg-[#0F1419] p-2.5 rounded-r-lg text-right">
                    <p className="text-[10px] text-gray-400 mb-1 font-medium">Olası Kazanç</p>
                    <div className="flex items-center justify-end gap-1">
                      <span className="text-lg">💰</span>
                      <p className="text-base font-black text-[#FFA500]">
                        {formatTurkishCurrency(potentialWin)} ₺
                      </p>
                    </div>
                  </div>
                </div>

                {/* Yatırılan Tutar */}
                <div>
                  <p className="text-[10px] text-gray-400 mb-2 font-medium">Yatırılan Tutar</p>
                  <div className="flex items-center gap-2">
                    {/* Minus Button */}
                    <button
                      onClick={decreaseBet}
                      disabled={betAmount <= 50}
                      className="w-10 h-10 bg-[#1A2028] hover:bg-[#222932] disabled:opacity-30 disabled:cursor-not-allowed rounded-lg flex items-center justify-center border border-gray-700/30 transition-all"
                    >
                      <Minus className="w-4 h-4 text-white" strokeWidth={2.5} />
                    </button>

                    {/* Amount Display */}
                    <div className="flex-1 bg-[#0F1419] rounded-lg border border-gray-700/30 px-2.5 py-2 text-center">
                      <span className="text-base font-black text-white">{formatTurkishCurrency(betAmount)} ₺</span>
                    </div>

                    {/* Plus Button */}
                    <button
                      onClick={increaseBet}
                      disabled={betAmount >= 10000}
                      className="w-10 h-10 bg-[#19E98B]/10 hover:bg-[#19E98B]/20 disabled:opacity-30 disabled:cursor-not-allowed rounded-lg flex items-center justify-center border border-[#19E98B]/40 transition-all"
                    >
                      <Plus className="w-4 h-4 text-[#19E98B]" strokeWidth={2.5} />
                    </button>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Fixed Footer - Kaydet Butonu */}
        {selections.length > 0 && (
          <div className="flex-shrink-0 px-3 pb-4 pt-3 bg-[#0A0E13] border-t border-gray-800/50">
            <button
              onClick={saveCoupon}
              disabled={betAmount <= 0 || isSaving}
              className="w-full bg-[#19E98B] hover:bg-[#15D67D] disabled:opacity-50 disabled:cursor-not-allowed text-[#0A0E13] font-black text-sm py-3.5 rounded-lg transition-all shadow-lg flex items-center justify-center gap-2"
            >
              {isSaving ? (
                <>
                  <div className="w-4 h-4 border-2 border-[#0A0E13]/30 border-t-[#0A0E13] rounded-full animate-spin"></div>
                  <span>Kaydediliyor...</span>
                </>
              ) : (
                <>
                  <Bookmark className="w-4 h-4" strokeWidth={2.5} />
                  <span>Kuponu Kaydet</span>
                </>
              )}
            </button>
          </div>
        )}
      </div>
    </>
  );
}

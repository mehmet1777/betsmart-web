'use client';

import { Sparkles, TrendingUp, Target, ArrowRight } from 'lucide-react';

interface NotificationDropdownProps {
  isOpen: boolean;
  totalMatches: number;
  recommendedCount: number;
  selectedDate: string;
  onViewRecommendations: () => void;
  onClose: () => void;
}

export default function NotificationDropdown({ 
  isOpen, 
  totalMatches, 
  recommendedCount,
  selectedDate, 
  onViewRecommendations,
  onClose 
}: NotificationDropdownProps) {
  if (!isOpen) return null;

  const formatDate = (dateStr: string) => {
    const [year, month, day] = dateStr.split('-');
    const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    date.setHours(0, 0, 0, 0);
    
    if (date.getTime() === today.getTime()) return 'Bugün';
    
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    if (date.getTime() === tomorrow.getTime()) return 'Yarın';
    
    const options: Intl.DateTimeFormatOptions = { day: 'numeric', month: 'long' };
    return date.toLocaleDateString('tr-TR', options);
  };

  return (
    <>
      <div className="fixed inset-0 z-40" onClick={onClose} />
      
      <div className="absolute top-full right-0 mt-2 w-[340px] sm:w-96 bg-[#101027] rounded-xl sm:rounded-2xl shadow-[0_0_40px_rgba(129,59,255,0.25)] border border-[rgba(139,76,255,0.30)] z-50 overflow-hidden">
        {/* Header - Kompakt */}
        <div className="bg-gradient-to-r from-[#813BFF] via-[#A04BFF] to-[#813BFF] p-3 sm:p-4">
          <div className="flex items-center gap-2">
            <Sparkles size={18} className="text-white" strokeWidth={2.5} />
            <h3 className="text-white font-bold text-base">Bugünün Önerileri</h3>
          </div>
        </div>

        {/* Content - Kompakt */}
        <div className="p-3 sm:p-4">
          {recommendedCount > 0 ? (
            <>
              {/* Tek satır metin */}
              <p className="text-white text-xs sm:text-sm mb-3 leading-tight">
                <span className="text-[#A5A5C5]">Merhaba!</span>{' '}
                <span className="font-semibold text-[#813BFF]">{formatDate(selectedDate)}</span>{' '}
                <span className="text-[#A5A5C5]">bülteninde</span>{' '}
                <span className="font-bold text-white">{totalMatches}</span>{' '}
                <span className="text-[#A5A5C5]">maç var.</span>
              </p>
              
              {/* Öneri Kartı - Çok Kompakt */}
              <div className="relative bg-gradient-to-br from-[#813BFF]/20 to-[#171633] border border-[rgba(139,76,255,0.40)] rounded-xl p-3 mb-3 overflow-hidden">
                <div className="absolute top-0 right-0 w-24 h-24 bg-[#813BFF]/10 rounded-full blur-2xl"></div>
                
                <div className="relative flex items-center gap-3">
                  <div className="bg-gradient-to-br from-[#813BFF]/30 to-[#A04BFF]/20 p-2 rounded-lg flex-shrink-0">
                    <TrendingUp size={20} className="text-[#813BFF]" strokeWidth={2.5} />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    <p className="text-white font-bold text-sm mb-0.5">BetSmart Sizin İçin</p>
                    <div className="flex items-baseline gap-1.5">
                      <span className="text-[#00E99A] text-lg font-bold leading-none">{recommendedCount}</span>
                      <span className="text-white text-sm font-semibold">Yüksek Başarı Bulundu</span>
                    </div>
                    <div className="inline-block bg-[#00E99A]/20 border border-[#00E99A]/40 rounded px-2 py-0.5 mt-1.5">
                      <span className="text-[#00E99A] text-[10px] font-semibold">+%75 kazanç potansiyeli</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Buton - Kompakt */}
              <button
                onClick={onViewRecommendations}
                className="w-full bg-gradient-to-r from-[#813BFF] to-[#A04BFF] text-white py-2.5 px-4 rounded-lg font-bold text-sm hover:shadow-[0_0_30px_rgba(129,59,255,0.4)] transition-all flex items-center justify-center gap-2 group"
              >
                <Target size={16} strokeWidth={2.5} />
                <span>Kuponu Gör</span>
                <ArrowRight size={14} className="group-hover:translate-x-1 transition-transform" strokeWidth={2.5} />
              </button>
            </>
          ) : (
            <div className="text-center py-4">
              <p className="text-[#A5A5C5] text-sm">{formatDate(selectedDate)} - {totalMatches} maç var</p>
              <p className="text-[#A5A5C5] text-xs mt-1">Yüksek başarılı öneri bulunamadı</p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

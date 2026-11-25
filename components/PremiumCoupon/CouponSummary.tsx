import { TrendingUp, Trophy } from 'lucide-react';

interface CouponSummaryProps {
  totalOdds: number;
  matchCount: number;
  sistemInfo?: string;
}

export default function CouponSummary({ totalOdds, matchCount, sistemInfo }: CouponSummaryProps) {
  const stake = 100;
  const potentialWin = totalOdds * stake;

  const formatCurrency = (value: number) => {
    return value.toLocaleString('tr-TR', { 
      minimumFractionDigits: 2, 
      maximumFractionDigits: 2 
    });
  };

  return (
    <div className="mt-3 px-3 pb-3">
      {/* Üç Bölüm - Kompakt Grid */}
      <div className="grid grid-cols-3 gap-2">
        {/* Sol: Toplam Oran */}
        <div className="bg-black/40 rounded-lg p-2 border" style={{ borderColor: 'rgba(0, 230, 118, 0.3)' }}>
          <TrendingUp className="w-3.5 h-3.5 text-green-500 mb-1" />
          <div className="text-[8px] text-gray-400 mb-0.5">Toplam Oran</div>
          <div className="text-sm font-bold text-green-500 leading-tight">
            {formatCurrency(totalOdds)}
          </div>
          {sistemInfo && (
            <div className="text-[7px] text-gray-500 mt-0.5">{sistemInfo}</div>
          )}
        </div>

        {/* Orta: Kupon Tutarı */}
        <div className="bg-black/40 rounded-lg p-2 border" style={{ borderColor: 'rgba(0, 230, 118, 0.3)' }}>
          <svg className="w-3.5 h-3.5 text-green-500 mb-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <div className="text-[8px] text-gray-400 mb-0.5">Kupon Tutarı</div>
          <div className="text-sm font-bold text-white leading-tight">
            {stake}<br/><span className="text-[10px]">TL</span>
          </div>
        </div>

        {/* Sağ: Muhtemel Kazanç - Parlak */}
        <div className="bg-gradient-to-br from-green-500/20 to-green-500/10 rounded-lg p-2 border-2 border-green-500 shadow-lg shadow-green-500/30">
          <Trophy className="w-3.5 h-3.5 text-green-500 mb-1" />
          <div className="text-[8px] text-green-300 mb-0.5">Muhtemel Kazanç</div>
          <div className="text-xs font-bold text-green-500 leading-tight">
            {formatCurrency(potentialWin)}<br/><span className="text-[10px]">TL</span>
          </div>
        </div>
      </div>
    </div>
  );
}

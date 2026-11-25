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
    <div className="mt-2 px-2 pb-2">
      <div className="grid grid-cols-3 gap-1.5">
        {/* Toplam Oran */}
        <div className="bg-black/40 rounded-md p-1.5 border" style={{ borderColor: 'rgba(0, 230, 118, 0.3)' }}>
          <TrendingUp className="w-3 h-3 text-green-500 mb-0.5" />
          <div className="text-[7px] text-gray-400">Toplam Oran</div>
          <div className="text-xs font-bold text-green-500 leading-tight">
            {formatCurrency(totalOdds)}
          </div>
          {sistemInfo && (
            <div className="text-[6px] text-gray-500 mt-0.5">{sistemInfo}</div>
          )}
        </div>

        {/* Kupon Tutarı */}
        <div className="bg-black/40 rounded-md p-1.5 border" style={{ borderColor: 'rgba(0, 230, 118, 0.3)' }}>
          <svg className="w-3 h-3 text-green-500 mb-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <div className="text-[7px] text-gray-400">Kupon Tutarı</div>
          <div className="text-xs font-bold text-white leading-tight">
            {stake} <span className="text-[9px]">TL</span>
          </div>
        </div>

        {/* Muhtemel Kazanç */}
        <div className="bg-gradient-to-br from-green-500/20 to-green-500/10 rounded-md p-1.5 border-2 border-green-500 shadow-lg shadow-green-500/30">
          <Trophy className="w-3 h-3 text-green-500 mb-0.5" />
          <div className="text-[7px] text-green-300">Muhtemel Kazanç</div>
          <div className="text-[11px] font-bold text-green-500 leading-tight">
            {formatCurrency(potentialWin)} <span className="text-[9px]">TL</span>
          </div>
        </div>
      </div>
    </div>
  );
}

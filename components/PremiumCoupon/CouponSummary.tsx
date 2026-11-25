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
    <div className="mt-4 px-4">
      {/* Üç Bölüm - Grid Layout */}
      <div className="grid grid-cols-12 gap-3">
        {/* Sol: Toplam Oran */}
        <div className="col-span-4 bg-black/40 rounded-xl p-3 border" style={{ borderColor: 'rgba(0, 230, 118, 0.3)' }}>
          <div className="flex items-start gap-2">
            <TrendingUp className="w-5 h-5 text-green-500 flex-shrink-0" />
            <div>
              <div className="text-[10px] text-gray-400 mb-1">Toplam Oran</div>
              <div className="text-xl font-bold text-green-500 leading-tight">
                {formatCurrency(totalOdds)}
              </div>
              {sistemInfo && (
                <div className="text-[9px] text-gray-500 mt-1">{sistemInfo}</div>
              )}
            </div>
          </div>
        </div>

        {/* Orta: Kupon Tutarı */}
        <div className="col-span-4 bg-black/40 rounded-xl p-3 border" style={{ borderColor: 'rgba(0, 230, 118, 0.3)' }}>
          <div className="flex items-start gap-2">
            <svg className="w-5 h-5 text-green-500 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <div>
              <div className="text-[10px] text-gray-400 mb-1">Kupon Tutarı</div>
              <div className="text-xl font-bold text-white leading-tight">
                {stake} TL
              </div>
            </div>
          </div>
        </div>

        {/* Sağ: Muhtemel Kazanç - Parlak/Öne Çıkan */}
        <div className="col-span-4 bg-gradient-to-br from-green-500/20 to-green-500/10 rounded-xl p-3 border-2 border-green-500 shadow-lg shadow-green-500/30">
          <div className="flex items-start gap-2">
            <Trophy className="w-5 h-5 text-green-500 flex-shrink-0" />
            <div>
              <div className="text-[10px] text-green-300 mb-1">Muhtemel Kazanç</div>
              <div className="text-xl font-bold text-green-500 leading-tight">
                {formatCurrency(potentialWin)} TL
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

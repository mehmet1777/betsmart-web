import { TrendingUp } from 'lucide-react';

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
    <div className="space-y-1.5">
      {/* Toplam Oran ve Kupon Tutarı - Yan Yana */}
      <div className="grid grid-cols-2 gap-1.5">
        {/* Toplam Oran */}
        <div className="bg-premium-card-secondary border border-premium-border rounded-lg p-2">
          <div className="flex items-center gap-1 mb-1">
            <TrendingUp className="w-2.5 h-2.5 text-premium-neon" />
            <span className="text-[8px] text-premium-text-secondary uppercase tracking-wide">
              Toplam Oran
            </span>
          </div>
          <div className="text-sm font-bold text-premium-neon">
            {formatCurrency(totalOdds)}
          </div>
          {sistemInfo && (
            <div className="text-[7px] text-premium-text-secondary mt-0.5">
              {sistemInfo}
            </div>
          )}
        </div>

        {/* Kupon Tutarı */}
        <div className="bg-premium-card-secondary border border-premium-border rounded-lg p-2">
          <div className="flex items-center gap-1 mb-1">
            <svg className="w-2.5 h-2.5 text-premium-neon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span className="text-[8px] text-premium-text-secondary uppercase tracking-wide">
              Kupon Tutarı
            </span>
          </div>
          <div className="text-sm font-bold text-premium-text">
            {stake} <span className="text-[10px] text-premium-text-secondary">TL</span>
          </div>
        </div>
      </div>

      {/* Muhtemel Kazanç - Tam Genişlik */}
      <div className="bg-gradient-to-br from-premium-neon/10 to-premium-neon/5 border border-premium-neon/50 rounded-lg p-2 shadow-lg shadow-premium-neon/10">
        <div className="flex items-center justify-between">
          <span className="text-[8px] text-premium-text-secondary uppercase tracking-wide">
            Muhtemel Kazanç
          </span>
          <div className="text-lg font-bold text-premium-neon leading-none">
            {formatCurrency(potentialWin)} <span className="text-[10px] text-premium-neon/70">TL</span>
          </div>
        </div>
      </div>
    </div>
  );
}

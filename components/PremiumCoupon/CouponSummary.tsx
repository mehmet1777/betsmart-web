import { TrendingUp, Trophy } from 'lucide-react';

interface CouponSummaryProps {
  totalOdds: number;
  matchCount: number;
  sistemInfo?: string;
}

export default function CouponSummary({ totalOdds, matchCount, sistemInfo }: CouponSummaryProps) {
  // Örnek hesaplama (100 TL sabit kupon tutarı ile)
  const stake = 100;
  const potentialWin = totalOdds * stake;

  const formatCurrency = (value: number) => {
    return value.toLocaleString('tr-TR', { 
      minimumFractionDigits: 2, 
      maximumFractionDigits: 2 
    });
  };

  return (
    <div className="mt-3 space-y-2">
      {/* Toplam Oran ve Kupon Tutarı */}
      <div className="grid grid-cols-2 gap-2">
        {/* Toplam Oran */}
        <div className="bg-premium-card-secondary border border-premium-border rounded-xl p-3">
          <div className="flex items-center gap-1.5 mb-1.5">
            <TrendingUp className="w-3.5 h-3.5 text-premium-neon" />
            <span className="text-[10px] text-premium-text-secondary uppercase tracking-wide">
              Toplam Oran
            </span>
          </div>
          <div className="text-xl font-bold text-premium-neon">
            {formatCurrency(totalOdds)}
          </div>
          {sistemInfo && (
            <div className="text-[9px] text-premium-text-secondary mt-1">
              {sistemInfo}
            </div>
          )}
        </div>

        {/* Kupon Tutarı */}
        <div className="bg-premium-card-secondary border border-premium-border rounded-xl p-3">
          <div className="flex items-center gap-1.5 mb-1.5">
            <svg className="w-3.5 h-3.5 text-premium-neon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span className="text-[10px] text-premium-text-secondary uppercase tracking-wide">
              Kupon Tutarı
            </span>
          </div>
          <div className="text-xl font-bold text-premium-text">
            {stake} <span className="text-sm text-premium-text-secondary">TL</span>
          </div>
        </div>
      </div>

      {/* Muhtemel Kazanç - Premium Card */}
      <div className="bg-gradient-to-br from-premium-neon/10 to-premium-neon/5 border-2 border-premium-neon/50 rounded-xl p-4 relative overflow-hidden shadow-lg shadow-premium-neon/10">
        {/* Glow efekti */}
        <div className="absolute inset-0 bg-gradient-to-br from-premium-neon/5 via-transparent to-transparent pointer-events-none" />
        
        <div className="relative flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-premium-neon/20 border border-premium-neon/40 flex items-center justify-center">
              <Trophy className="w-4 h-4 text-premium-neon" />
            </div>
            <div>
              <div className="text-[10px] text-premium-text-secondary uppercase tracking-wide mb-0.5">
                Muhtemel Kazanç
              </div>
              <div className="text-2xl font-bold text-premium-neon leading-none">
                {formatCurrency(potentialWin)} <span className="text-sm text-premium-neon/70">TL</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Misli Bilgisi */}
      {matchCount > 1 && (
        <div className="text-center">
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-premium-card-secondary border border-premium-border rounded-lg text-[10px] text-premium-text-secondary">
            <span className="w-1.5 h-1.5 rounded-full bg-premium-neon animate-pulse" />
            Misli {matchCount} • {matchCount} Maç
          </span>
        </div>
      )}
    </div>
  );
}

import CouponHeader from './CouponHeader';
import CouponMatch from './CouponMatch';
import CouponSummary from './CouponSummary';

interface ParsedMatch {
  teams: string;
  mbs?: string;
  tahmin?: string;
  oran?: string;
  mac_saati?: string;
  skor?: string;
  ilk_yari_skor?: string;
}

interface PremiumCouponProps {
  matches: ParsedMatch[];
  totalOdds: number;
  sistemInfo?: string;
}

export default function PremiumCoupon({ matches, totalOdds, sistemInfo }: PremiumCouponProps) {
  return (
    <div className="w-full max-w-[430px] mx-auto px-3">
      {/* Ana Kupon Kartı */}
      <div className="bg-premium-card border border-premium-border rounded-xl overflow-hidden shadow-2xl shadow-black/50">
        {/* Header */}
        <CouponHeader />

        {/* Maçlar - Daha kompakt spacing */}
        <div className="p-2 space-y-1.5">
          {matches.map((match, index) => (
            <CouponMatch key={index} match={match} index={index} />
          ))}
        </div>

        {/* Özet */}
        <div className="px-2 pb-2">
          <CouponSummary 
            totalOdds={totalOdds} 
            matchCount={matches.length}
            sistemInfo={sistemInfo}
          />
        </div>
      </div>
    </div>
  );
}

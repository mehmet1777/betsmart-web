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
    <div className="w-full max-w-[430px] mx-auto px-3 sm:px-4">
      {/* Ana Kupon Kartı */}
      <div className="bg-premium-card border border-premium-border rounded-2xl overflow-hidden shadow-2xl shadow-black/50">
        {/* Header */}
        <CouponHeader />

        {/* Maçlar */}
        <div className="p-3 space-y-2">
          {matches.map((match, index) => (
            <CouponMatch key={index} match={match} index={index} />
          ))}
        </div>

        {/* Özet */}
        <div className="px-3 pb-4">
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

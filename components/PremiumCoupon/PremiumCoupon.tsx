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
    <div className="w-full max-w-[390px] mx-auto px-2">
      {/* Ana Kupon Kartı - Mobil Kompakt */}
      <div className="bg-black/70 backdrop-blur-sm border-2 border-green-500/40 rounded-xl overflow-hidden shadow-2xl shadow-green-500/20">
        {/* Header */}
        <CouponHeader />

        {/* Maçlar - Minimum padding */}
        <div className="px-3">
          {matches.map((match, index) => (
            <CouponMatch key={index} match={match} index={index} />
          ))}
        </div>

        {/* Özet */}
        <CouponSummary 
          totalOdds={totalOdds} 
          matchCount={matches.length}
          sistemInfo={sistemInfo}
        />
      </div>
    </div>
  );
}

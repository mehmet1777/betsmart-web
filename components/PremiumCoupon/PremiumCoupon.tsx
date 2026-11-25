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
    <div className="w-full max-w-[500px] mx-auto px-4">
      {/* Ana Kupon Kartı - Referans tasarıma göre */}
      <div className="bg-black/60 backdrop-blur-sm border-2 border-green-500/40 rounded-2xl overflow-hidden shadow-2xl shadow-green-500/20">
        {/* Header */}
        <CouponHeader />

        {/* Maçlar - Border'lı liste */}
        <div className="px-4">
          {matches.map((match, index) => (
            <CouponMatch key={index} match={match} index={index} />
          ))}
        </div>

        {/* Özet - Alt kısım */}
        <CouponSummary 
          totalOdds={totalOdds} 
          matchCount={matches.length}
          sistemInfo={sistemInfo}
        />
        
        <div className="pb-4" />
      </div>
    </div>
  );
}

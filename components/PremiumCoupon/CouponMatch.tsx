import { X } from 'lucide-react';

interface CouponMatchProps {
  match: {
    teams: string;
    mac_saati?: string;
    skor?: string;
    ilk_yari_skor?: string;
    tahmin?: string;
    mbs?: string;
    oran?: string;
  };
  index: number;
}

export default function CouponMatch({ match, index }: CouponMatchProps) {
  return (
    <div className="relative py-2 border-b" style={{ borderColor: 'rgba(0, 230, 118, 0.15)' }}>
      <div className="flex items-start gap-1.5">
        {/* Sol: Futbol + Numara - Çok Küçük */}
        <div className="flex items-center gap-1 flex-shrink-0">
          <div className="w-5 h-5 rounded-full bg-white/10 flex items-center justify-center">
            <span className="text-xs">⚽</span>
          </div>
          <div className="w-5 h-5 rounded bg-green-500 flex items-center justify-center">
            <span className="text-[10px] font-bold text-black">{index + 1}</span>
          </div>
        </div>

        {/* Orta: Maç Bilgileri */}
        <div className="flex-1 min-w-0">
          {/* Takım ve Skor */}
          <div className="flex items-start justify-between gap-2 mb-1">
            <div className="flex-1 min-w-0">
              <h3 className="text-xs font-bold text-white leading-tight">{match.teams}</h3>
            </div>
            {/* Skor */}
            {match.skor && (
              <div className="text-[9px] flex-shrink-0">
                <span className="text-white">MS / {match.skor}</span>
                {match.ilk_yari_skor && (
                  <span className="text-green-500 ml-1">(İY: {match.ilk_yari_skor})</span>
                )}
              </div>
            )}
          </div>

          {/* Bahis ve Oran - Tek Satır */}
          <div className="flex items-center gap-1.5">
            {/* Bahis */}
            <div className="bg-gray-800/80 rounded px-1.5 py-0.5">
              <span className="text-[9px] font-medium text-white whitespace-nowrap">
                {match.tahmin || '1 & Var'}
              </span>
            </div>
            {/* Oran */}
            <div className="ml-auto flex-shrink-0">
              <span className="text-lg font-bold text-green-500">
                {match.oran || '13.00'}
              </span>
            </div>
          </div>
        </div>

        {/* X Butonu */}
        <button className="flex-shrink-0 p-0.5 hover:bg-white/5 rounded transition-colors">
          <X className="w-3.5 h-3.5 text-green-500" />
        </button>
      </div>
    </div>
  );
}

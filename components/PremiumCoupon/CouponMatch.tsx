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
    <div className="relative py-3 border-b" style={{ borderColor: 'rgba(0, 230, 118, 0.15)' }}>
      <div className="flex items-start gap-2">
        {/* Sol: Futbol İkonu + Numara - Çok Kompakt */}
        <div className="flex items-center gap-1.5 flex-shrink-0">
          <div className="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center">
            <span className="text-sm">⚽</span>
          </div>
          <div className="w-6 h-6 rounded bg-green-500 flex items-center justify-center">
            <span className="text-xs font-bold text-black">{index + 1}</span>
          </div>
        </div>

        {/* Orta: Maç Bilgileri */}
        <div className="flex-1 min-w-0">
          {/* Takım Adı ve Skor - Üst Satır */}
          <div className="flex items-start justify-between gap-2 mb-1.5">
            <div className="flex-1 min-w-0">
              <h3 className="text-sm font-bold text-white leading-tight mb-0.5">{match.teams}</h3>
              <p className="text-[10px] text-gray-500">MS</p>
            </div>
            {/* Skor - Sağ Üst Köşe */}
            {match.skor && (
              <div className="text-right text-[10px] flex-shrink-0">
                <div>
                  <span className="text-white">MS / {match.skor}</span>
                  {match.ilk_yari_skor && (
                    <span className="text-green-500 ml-1">(İY: {match.ilk_yari_skor})</span>
                  )}
                </div>
              </div>
            )}
          </div>

          {/* Alt Satır: Bahis ve Oran */}
          <div className="flex items-center gap-2">
            {/* Bahis Kartı - Kompakt */}
            <div className="bg-gray-800/80 rounded px-2 py-1">
              <span className="text-[10px] font-medium text-white whitespace-nowrap">
                {match.tahmin || '1 & Var'}
              </span>
            </div>

            {/* Oran - Büyük ve Yeşil */}
            <div className="ml-auto flex-shrink-0">
              <span className="text-xl font-bold text-green-500">
                {match.oran || '13.00'}
              </span>
            </div>
          </div>
        </div>

        {/* Sağ: X Butonu */}
        <button className="flex-shrink-0 p-0.5 hover:bg-white/5 rounded transition-colors">
          <X className="w-4 h-4 text-green-500" />
        </button>
      </div>
    </div>
  );
}

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
    <div className="relative py-4 border-b" style={{ borderColor: 'rgba(0, 230, 118, 0.2)' }}>
      <div className="flex items-start gap-3">
        {/* Sol: Futbol İkonu + Numara */}
        <div className="flex items-center gap-2 flex-shrink-0">
          <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center">
            <span className="text-lg">⚽</span>
          </div>
          <div className="w-8 h-8 rounded bg-green-500 flex items-center justify-center">
            <span className="text-sm font-bold text-black">{index + 1}</span>
          </div>
        </div>

        {/* Orta: Maç Bilgileri */}
        <div className="flex-1 min-w-0">
          {/* Takım Adı ve Skor */}
          <div className="flex items-start justify-between mb-2">
            <div className="flex-1 min-w-0">
              <h3 className="text-base font-bold text-white mb-1">{match.teams}</h3>
              <p className="text-xs text-gray-400">{match.mac_saati || '24 Kasım 2026 21:00'}</p>
            </div>
            {/* Skor - Sağ Üst */}
            {match.skor && (
              <div className="text-right text-xs ml-3">
                <span className="text-white">MS / {match.skor}</span>
                {match.ilk_yari_skor && (
                  <span className="text-green-500 ml-1">(İY: {match.ilk_yari_skor})</span>
                )}
              </div>
            )}
          </div>

          {/* Bahis Kartları ve Oran */}
          <div className="flex items-center gap-2">
            {/* Bahis Kartı 1 */}
            <div className="bg-gray-800/80 rounded px-3 py-1.5">
              <span className="text-xs font-medium text-white">
                {match.tahmin || '1.Y Sonucu & 1.Y KG'}
              </span>
            </div>

            {/* Bahis Kartı 2 */}
            {match.mbs && (
              <div className="bg-gray-800/80 rounded px-3 py-1.5">
                <span className="text-xs font-medium text-white">
                  {match.mbs} & Var
                </span>
              </div>
            )}

            {/* Oran - Büyük ve Yeşil */}
            <div className="ml-auto flex-shrink-0">
              <span className="text-2xl font-bold text-green-500">
                {match.oran || '13.00'}
              </span>
            </div>
          </div>
        </div>

        {/* Sağ: X Butonu */}
        <button className="flex-shrink-0 p-1 hover:bg-white/5 rounded transition-colors">
          <X className="w-5 h-5 text-green-500" />
        </button>
      </div>
    </div>
  );
}

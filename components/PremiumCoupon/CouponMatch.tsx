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
    <div className="bg-premium-card-secondary border border-premium-border rounded-lg p-2.5 relative overflow-hidden">
      {/* Hafif glow efekti */}
      <div className="absolute inset-0 bg-gradient-to-br from-premium-neon/5 to-transparent pointer-events-none" />
      
      <div className="relative">
        {/* Üst Satır: Numara, Takımlar, Skor, Oran */}
        <div className="flex items-start justify-between gap-2 mb-1.5">
          <div className="flex items-start gap-1.5 flex-1 min-w-0">
            {/* Maç Numarası */}
            <div className="w-5 h-5 rounded bg-premium-neon/20 border border-premium-neon/40 flex items-center justify-center flex-shrink-0 mt-0.5">
              <span className="text-[10px] font-bold text-premium-neon">{index + 1}</span>
            </div>
            
            {/* Takım İsimleri */}
            <div className="flex-1 min-w-0">
              <h4 className="text-xs font-bold text-premium-text leading-tight">
                {match.teams}
              </h4>
              <p className="text-[9px] text-premium-text-secondary mt-0.5">MS</p>
            </div>

            {/* Skor (sağ üst) */}
            <div className="text-right flex-shrink-0">
              {match.skor && (
                <>
                  <div className="text-sm font-bold text-premium-text">{match.skor}</div>
                  {match.ilk_yari_skor && (
                    <div className="text-[8px] text-premium-neon/70">İY: {match.ilk_yari_skor}</div>
                  )}
                </>
              )}
            </div>
          </div>
        </div>

        {/* Alt Satır: Bahis ve Oran */}
        <div className="flex items-center justify-between gap-2">
          {/* Bahis Bilgisi */}
          <div className="flex-1 min-w-0 bg-premium-neon/10 border border-premium-neon/30 rounded px-2 py-1">
            <div className="text-[8px] text-premium-text-secondary uppercase">Bahis</div>
            <div className="text-[10px] font-semibold text-premium-neon leading-tight truncate">
              {match.tahmin || '1 & Var'}
            </div>
          </div>

          {/* Oran */}
          <div className="bg-premium-neon/15 border border-premium-neon/40 rounded px-2.5 py-1 flex-shrink-0">
            <div className="text-[8px] text-premium-text-secondary uppercase text-center">Oran</div>
            <div className="text-base font-bold text-premium-neon leading-tight">
              {match.oran || '-'}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

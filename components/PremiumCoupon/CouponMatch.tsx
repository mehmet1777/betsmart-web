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
    <div className="bg-premium-card-secondary border border-premium-border rounded-xl p-3 relative overflow-hidden">
      {/* Hafif glow efekti */}
      <div className="absolute inset-0 bg-gradient-to-br from-premium-neon/5 to-transparent pointer-events-none" />
      
      <div className="relative">
        {/* Üst Satır: İkon, Takımlar, Skor */}
        <div className="flex items-start justify-between gap-2 mb-2">
          <div className="flex items-start gap-2 flex-1 min-w-0">
            {/* Maç Numarası */}
            <div className="w-7 h-7 rounded-lg bg-premium-neon/20 border border-premium-neon/40 flex items-center justify-center flex-shrink-0 mt-0.5">
              <span className="text-xs font-bold text-premium-neon">{index + 1}</span>
            </div>
            
            {/* Takım İsimleri */}
            <div className="flex-1 min-w-0">
              <h4 className="text-sm font-bold text-premium-text leading-tight mb-1">
                {match.teams}
              </h4>
              {match.mac_saati && (
                <p className="text-[11px] text-premium-text-secondary">
                  {match.mac_saati}
                </p>
              )}
            </div>
          </div>

          {/* Skor */}
          {match.skor && (
            <div className="text-right flex-shrink-0">
              <div className="text-[10px] text-premium-text-secondary mb-0.5">MS</div>
              <div className="text-xs font-bold text-premium-text">{match.skor}</div>
              {match.ilk_yari_skor && (
                <div className="text-[9px] text-premium-neon/70 mt-0.5">İY: {match.ilk_yari_skor}</div>
              )}
            </div>
          )}
        </div>

        {/* Alt Satır: Tahmin, MBS, Oran */}
        <div className="flex items-center justify-between gap-2 mt-2 pt-2 border-t border-premium-border/50">
          <div className="flex items-center gap-2 flex-1 min-w-0">
            {/* Tahmin */}
            {match.tahmin && (
              <div className="bg-premium-neon/15 border border-premium-neon/30 rounded-md px-2 py-1">
                <div className="text-[9px] text-premium-text-secondary mb-0.5 uppercase">Bahis</div>
                <div className="text-[11px] font-semibold text-premium-neon leading-tight">
                  {match.tahmin}
                </div>
              </div>
            )}
            
            {/* MBS */}
            {match.mbs && (
              <div className="bg-premium-card/50 border border-premium-border rounded-md px-2 py-1">
                <div className="text-[9px] text-premium-text-secondary mb-0.5 uppercase">Seçim</div>
                <div className="text-[11px] font-semibold text-premium-text leading-tight">
                  {match.mbs} & Var
                </div>
              </div>
            )}
          </div>

          {/* Oran */}
          {match.oran && (
            <div className="bg-premium-neon/10 border border-premium-neon/40 rounded-lg px-3 py-2 flex-shrink-0">
              <div className="text-[9px] text-premium-text-secondary mb-0.5 uppercase tracking-wide">Oran</div>
              <div className="text-lg font-bold text-premium-neon leading-none">
                {match.oran}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

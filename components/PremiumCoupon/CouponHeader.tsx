import { Crown } from 'lucide-react';

export default function CouponHeader() {
  return (
    <div className="px-3 py-2.5 border-b border-premium-border">
      <div className="flex items-center justify-between">
        {/* Logo ve Marka */}
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-premium-neon to-premium-neon-light rounded-lg flex items-center justify-center">
            <span className="text-premium-card font-bold text-sm">B</span>
          </div>
          <div>
            <h2 className="text-sm font-bold leading-tight">
              <span className="text-white">Bet</span>
              <span className="text-premium-neon">smart</span>
            </h2>
            <p className="text-[8px] text-premium-text-secondary tracking-wider uppercase">
              ANALİZ • STRATEJİ • KAZANÇ
            </p>
          </div>
        </div>

        {/* Premium Badge */}
        <div className="flex items-center gap-1 px-2 py-1 bg-premium-card-secondary border border-premium-border rounded-md">
          <Crown className="w-2.5 h-2.5 text-premium-neon" />
          <span className="text-[9px] font-bold text-premium-neon tracking-wide uppercase">
            Premium
          </span>
        </div>
      </div>
    </div>
  );
}

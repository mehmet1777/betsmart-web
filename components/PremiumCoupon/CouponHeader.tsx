import { Crown } from 'lucide-react';

export default function CouponHeader() {
  return (
    <div className="px-4 py-4 border-b border-premium-border">
      <div className="flex items-center justify-between">
        {/* Logo ve Marka */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-premium-neon to-premium-neon-light rounded-lg flex items-center justify-center">
            <span className="text-premium-card font-bold text-lg">B</span>
          </div>
          <div>
            <h2 className="text-base font-bold leading-tight">
              <span className="text-white">Bet</span>
              <span className="text-premium-neon">smart</span>
            </h2>
            <p className="text-[9px] text-premium-text-secondary tracking-wider uppercase">
              ANALİZ • STRATEJİ • KAZANÇ
            </p>
          </div>
        </div>

        {/* Premium Badge */}
        <div className="flex items-center gap-1.5 px-2.5 py-1.5 bg-premium-card-secondary border border-premium-border rounded-lg">
          <Crown className="w-3 h-3 text-premium-neon" />
          <span className="text-[10px] font-bold text-premium-neon tracking-wide uppercase">
            Premium Kupon
          </span>
        </div>
      </div>
    </div>
  );
}

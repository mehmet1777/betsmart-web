import { Crown } from 'lucide-react';

export default function CouponHeader() {
  return (
    <div className="px-3 py-2 border-b" style={{ borderColor: 'rgba(0, 230, 118, 0.2)' }}>
      <div className="flex items-center justify-between">
        {/* Logo ve Marka - Minimal */}
        <div className="flex items-center gap-1.5">
          <div className="w-6 h-6 bg-gradient-to-br from-green-500 to-green-400 rounded-md flex items-center justify-center">
            <svg className="w-3.5 h-3.5 text-black" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
            </svg>
          </div>
          <div className="text-xs font-bold leading-none">
            <span className="text-white">Bet</span>
            <span className="text-green-500">smart</span>
          </div>
        </div>

        {/* Premium Badge - Mini */}
        <button className="flex items-center gap-1 px-2 py-1 bg-transparent border border-green-500 rounded-full hover:bg-green-500/10 transition-colors">
          <Crown className="w-2.5 h-2.5 text-green-500" />
          <div className="text-[8px] font-bold text-green-500 tracking-wide uppercase leading-none">
            Premium<br/>Kupon
          </div>
        </button>
      </div>
    </div>
  );
}

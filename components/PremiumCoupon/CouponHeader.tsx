import { Crown } from 'lucide-react';

export default function CouponHeader() {
  return (
    <div className="px-4 py-3 border-b" style={{ borderColor: 'rgba(0, 230, 118, 0.2)' }}>
      <div className="flex items-center justify-between">
        {/* Logo ve Marka */}
        <div className="flex items-center gap-4">
          {/* Logo */}
          <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-green-400 rounded-lg flex items-center justify-center">
            <svg className="w-6 h-6 text-black" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
            </svg>
          </div>
          
          {/* Brand Name */}
          <div className="flex items-center gap-6">
            <div>
              <h2 className="text-xl font-bold leading-tight">
                <span className="text-white">Bet</span>
                <span className="text-green-500">smart</span>
              </h2>
            </div>
            <div className="text-xs text-gray-400 tracking-widest">
              ANALİZ • STRATEJİ • KAZANÇ
            </div>
          </div>
        </div>

        {/* Premium Badge */}
        <button className="flex items-center gap-2 px-4 py-2 bg-transparent border-2 border-green-500 rounded-full hover:bg-green-500/10 transition-colors">
          <Crown className="w-4 h-4 text-green-500" />
          <span className="text-sm font-bold text-green-500 tracking-wide uppercase">
            Premium Kupon
          </span>
        </button>
      </div>
    </div>
  );
}

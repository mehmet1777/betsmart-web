import { Crown } from 'lucide-react';

export default function CouponHeader() {
  return (
    <div className="px-3 py-2.5 border-b" style={{ borderColor: 'rgba(0, 230, 118, 0.2)' }}>
      <div className="flex items-center justify-between">
        {/* Logo ve Marka - Kompakt */}
        <div className="flex items-center gap-2">
          {/* Logo */}
          <div className="w-7 h-7 bg-gradient-to-br from-green-500 to-green-400 rounded-lg flex items-center justify-center">
            <svg className="w-4 h-4 text-black" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12 2L2 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-10-5z"/>
            </svg>
          </div>
          
          {/* Brand Name */}
          <div>
            <div className="flex items-center gap-1">
              <span className="text-sm font-bold text-white">Bet</span>
              <span className="text-sm font-bold text-green-500">smart</span>
            </div>
          </div>
          
          {/* Tagline - Çok Küçük */}
          <div className="text-[8px] text-gray-500 tracking-wider ml-2 hidden xs:block">
            ANALİZ •<br/>STRATEJİ •<br/>KAZANÇ
          </div>
        </div>

        {/* Premium Badge - Kompakt */}
        <button className="flex items-center gap-1.5 px-2.5 py-1.5 bg-transparent border border-green-500 rounded-full hover:bg-green-500/10 transition-colors">
          <Crown className="w-3 h-3 text-green-500" />
          <div className="text-[9px] font-bold text-green-500 tracking-wide uppercase leading-none">
            Premium<br/>Kupon
          </div>
        </button>
      </div>
    </div>
  );
}

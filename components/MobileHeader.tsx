'use client';

import { Bell, Search, TrendingUp } from 'lucide-react';
import BetSmartLogo from './BetSmartLogo';
import Link from 'next/link';

interface MobileHeaderProps {
  onNotificationClick: () => void;
  onSearchClick: () => void;
  notificationCount?: number;
}

export default function MobileHeader({ onNotificationClick, onSearchClick, notificationCount = 0 }: MobileHeaderProps) {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-bg-app gradient-header border-b border-border-color safe-top">
      <div className="flex items-center justify-between px-4 py-3">
        {/* Left: Logo */}
        <div className="flex items-center">
          <BetSmartLogo variant="full" className="h-7" />
        </div>

        {/* Right: Analiz Kuponları + Icons */}
        <div className="flex items-center gap-2">
          {/* Analiz Kuponları Button */}
          <Link 
            href="/analiz-kuponlari"
            className="flex items-center gap-1.5 py-2 px-4 bg-gradient-to-r from-[#10B981] to-[#059669] hover:from-[#059669] hover:to-[#047857] text-white font-semibold rounded-xl transition-all text-[13px] shadow-lg shadow-green-500/30 border border-green-400/20"
          >
            <TrendingUp className="w-4 h-4" />
            <span>Analiz Kuponları</span>
          </Link>
          
          <button 
            onClick={onNotificationClick}
            className="p-2 text-text-secondary hover:text-accent-primary transition-colors relative"
          >
            <Bell className="w-5 h-5" />
            {notificationCount > 0 && (
              <span className="absolute top-1 right-1 min-w-[18px] h-[18px] bg-gradient-to-r from-[#8B5CF6] to-[#6366F1] text-white text-[10px] font-bold rounded-full flex items-center justify-center px-1 animate-pulse">
                {notificationCount}
              </span>
            )}
          </button>
          <button 
            onClick={onSearchClick}
            className="p-2 text-text-secondary hover:text-accent-primary transition-colors"
          >
            <Search className="w-5 h-5" />
          </button>
        </div>
      </div>
    </header>
  );
}

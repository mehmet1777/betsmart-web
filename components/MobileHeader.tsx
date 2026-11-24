'use client';

import { Bell, Search } from 'lucide-react';
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

        {/* Right: Icons */}
        <div className="flex items-center gap-1">
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
      
      {/* Analiz Kuponları Button */}
      <div className="px-4 pb-3">
        <Link 
          href="/analiz-kuponlari"
          className="flex items-center justify-center gap-2 py-2.5 px-4 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-green-500/20"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          Analiz Kuponları
        </Link>
      </div>
    </header>
  );
}

'use client';

import { Menu, Bell, User } from 'lucide-react';
import BetSmartLogo from './BetSmartLogo';

interface MobileHeaderProps {
  onMenuClick: () => void;
}

export default function MobileHeader({ onMenuClick }: MobileHeaderProps) {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-bg-app gradient-header border-b border-border-color safe-top">
      <div className="flex items-center justify-between px-4 py-3">
        {/* Left: Menu */}
        <button
          onClick={onMenuClick}
          className="p-2 -ml-2 text-text-primary hover:text-accent-primary transition-colors"
        >
          <Menu className="w-6 h-6" />
        </button>

        {/* Center: Logo */}
        <div className="flex-1 flex justify-center px-4">
          <BetSmartLogo variant="full" className="h-7" />
        </div>

        {/* Right: Icons */}
        <div className="flex items-center gap-1">
          <button className="p-2 text-text-secondary hover:text-accent-primary transition-colors relative">
            <Bell className="w-5 h-5" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-red-500 rounded-full"></span>
          </button>
          <button className="p-2 text-text-secondary hover:text-accent-primary transition-colors">
            <User className="w-5 h-5" />
          </button>
        </div>
      </div>
    </header>
  );
}

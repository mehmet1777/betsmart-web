'use client';

import { Bell, Search, Menu, X } from 'lucide-react';
import BetSmartLogo from './BetSmartLogo';
import Link from 'next/link';
import { useState } from 'react';

interface MobileHeaderProps {
  onNotificationClick: () => void;
  onSearchClick: () => void;
  notificationCount?: number;
}

export default function MobileHeader({ onNotificationClick, onSearchClick, notificationCount = 0 }: MobileHeaderProps) {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
  const closeMenu = () => setIsMenuOpen(false);

  return (
    <>
      <header className="fixed top-0 left-0 right-0 z-50 bg-bg-app gradient-header border-b border-border-color safe-top">
        <div className="flex items-center justify-between px-4 py-3">
          {/* Left: Hamburger Menu + Logo */}
          <div className="flex items-center gap-3">
            <button 
              onClick={toggleMenu}
              className="p-2 text-text-secondary hover:text-accent-primary transition-colors -ml-2"
              aria-label="Menü"
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
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
      </header>

      {/* Sidebar Menu */}
      {isMenuOpen && (
        <>
          {/* Overlay */}
          <div 
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 safe-top"
            onClick={closeMenu}
          />
          
          {/* Menu Panel */}
          <div className="fixed top-0 left-0 bottom-0 w-72 bg-bg-secondary border-r border-border-color z-50 safe-top animate-slide-in-left">
            <div className="flex flex-col h-full">
              {/* Menu Header */}
              <div className="flex items-center justify-between px-4 py-3 border-b border-border-color gradient-header">
                <BetSmartLogo variant="full" className="h-7" />
                <button 
                  onClick={closeMenu}
                  className="p-2 text-text-secondary hover:text-accent-primary transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Menu Items */}
              <nav className="flex-1 overflow-y-auto py-4">
                <Link 
                  href="/analiz-kuponlari"
                  onClick={closeMenu}
                  className="flex items-center gap-3 px-4 py-3 text-text-primary hover:bg-bg-hover transition-colors"
                >
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-r from-[#10B981] to-[#059669] flex items-center justify-center">
                    <span className="text-xl">📈</span>
                  </div>
                  <div>
                    <div className="font-semibold">Analiz Kuponları</div>
                    <div className="text-sm text-text-secondary">Nesine & Mackolik</div>
                  </div>
                </Link>

                {/* Gelecek özellikler için placeholder */}
                <div className="px-4 py-2 mt-4">
                  <div className="text-xs text-text-secondary uppercase tracking-wider">Yakında</div>
                </div>
                
                <div className="px-4 py-3 text-text-secondary opacity-50 cursor-not-allowed">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-bg-hover flex items-center justify-center">
                      <span className="text-xl">⚙️</span>
                    </div>
                    <div>
                      <div className="font-semibold">Ayarlar</div>
                      <div className="text-sm">Yakında eklenecek</div>
                    </div>
                  </div>
                </div>
              </nav>

              {/* Menu Footer */}
              <div className="border-t border-border-color px-4 py-3">
                <div className="text-xs text-text-secondary text-center">
                  BetSmart v1.0
                </div>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Slide-in Animation */}
      <style jsx>{`
        @keyframes slide-in-left {
          from {
            transform: translateX(-100%);
          }
          to {
            transform: translateX(0);
          }
        }
        .animate-slide-in-left {
          animation: slide-in-left 0.3s ease-out;
        }
      `}</style>
    </>
  );
}

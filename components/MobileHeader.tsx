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
          <div className="fixed top-0 left-0 bottom-0 w-72 bg-[#0F1419] border-r border-border-color z-50 safe-top animate-slide-in-left shadow-2xl">
            <div className="flex flex-col h-full">
              {/* Menu Header */}
              <div className="flex items-center justify-between px-4 py-3 border-b border-border-color bg-[#1a1f27]">
                <BetSmartLogo variant="full" className="h-7" />
                <button 
                  onClick={closeMenu}
                  className="p-2 text-text-secondary hover:text-accent-primary transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Menu Items */}
              <nav className="flex-1 overflow-y-auto py-4 bg-[#0F1419]">
                <Link 
                  href="/analiz-kuponlari"
                  onClick={closeMenu}
                  className="flex items-center gap-4 mx-3 px-4 py-4 rounded-xl bg-gradient-to-r from-[#10B981]/10 to-[#059669]/10 border border-[#10B981]/20 hover:border-[#10B981]/40 transition-all group"
                >
                  <div className="relative">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#10B981] to-[#059669] flex items-center justify-center shadow-lg shadow-green-500/20">
                      <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                      </svg>
                    </div>
                    <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
                  </div>
                  <div className="flex-1">
                    <div className="font-semibold text-white group-hover:text-green-400 transition-colors">
                      Analiz Kuponları
                    </div>
                    <div className="text-sm text-text-secondary">
                      Nesine & Mackolik
                    </div>
                  </div>
                  <svg className="w-5 h-5 text-text-secondary group-hover:text-green-400 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </Link>

                {/* Divider */}
                <div className="my-6 mx-3 border-t border-border-color"></div>

                {/* Gelecek özellikler için placeholder */}
                <div className="px-6 mb-3">
                  <div className="text-xs text-text-secondary uppercase tracking-wider font-semibold">
                    Yakında
                  </div>
                </div>
                
                <div className="flex items-center gap-4 mx-3 px-4 py-4 rounded-xl bg-[#1a1f27]/50 border border-transparent opacity-50 cursor-not-allowed">
                  <div className="w-12 h-12 rounded-xl bg-[#2a2f37] flex items-center justify-center">
                    <svg className="w-6 h-6 text-text-secondary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div className="flex-1">
                    <div className="font-semibold text-text-secondary">
                      Ayarlar
                    </div>
                    <div className="text-sm text-text-secondary/70">
                      Yakında eklenecek
                    </div>
                  </div>
                </div>
              </nav>

              {/* Menu Footer */}
              <div className="border-t border-border-color px-4 py-3 bg-[#0F1419]">
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

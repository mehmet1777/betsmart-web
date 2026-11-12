'use client';

import { Home, Radio, Ticket, Star } from 'lucide-react';

interface BottomNavProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export default function BottomNav({ activeTab, onTabChange }: BottomNavProps) {
  const tabs = [
    { id: 'home', label: 'Ana Sayfa', icon: Home },
    { id: 'live', label: 'Canlı', icon: Radio },
    { id: 'coupons', label: 'Kuponlarım', icon: Ticket },
    { id: 'favorites', label: 'Favorilerim', icon: Star },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-[#0A0E13] border-t border-gray-800/50 safe-bottom z-50">
      <div className="grid grid-cols-4">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`relative flex flex-col items-center gap-1.5 py-3 transition-all ${
                isActive ? 'text-[#19E98B]' : 'text-gray-500'
              }`}
            >
              {/* Active indicator glow */}
              {isActive && (
                <div className="absolute inset-0 bg-gradient-to-t from-[#19E98B]/10 to-transparent pointer-events-none"></div>
              )}
              
              {/* Icon with glow effect for active tab */}
              <div className={`relative ${isActive ? 'drop-shadow-[0_0_8px_rgba(25,233,139,0.5)]' : ''}`}>
                <Icon className="w-6 h-6" strokeWidth={isActive ? 2.5 : 2} />
              </div>
              
              <span className={`text-[11px] font-semibold relative ${isActive ? 'text-[#19E98B]' : 'text-gray-500'}`}>
                {tab.label}
              </span>
              
              {/* Active indicator line */}
              {isActive && (
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-12 h-1 bg-[#19E98B] rounded-b-full shadow-lg shadow-[#19E98B]/50"></div>
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
}

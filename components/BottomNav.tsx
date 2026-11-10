'use client';

import { Home, Radio, FileText, Star } from 'lucide-react';

interface BottomNavProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export default function BottomNav({ activeTab, onTabChange }: BottomNavProps) {
  const tabs = [
    { id: 'home', label: 'Ana Sayfa', icon: Home },
    { id: 'live', label: 'Canlı', icon: Radio },
    { id: 'coupons', label: 'Kuponlarım', icon: FileText },
    { id: 'favorites', label: 'Favorilerim', icon: Star },
  ];

  return (
    <nav className="fixed bottom-0 left-0 right-0 bg-bg-card border-t border-border-color safe-bottom z-50">
      <div className="grid grid-cols-4">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`flex flex-col items-center gap-1 py-3 transition-colors ${
                isActive ? 'text-accent-primary' : 'text-text-muted'
              }`}
            >
              <Icon className="w-5 h-5" />
              <span className="text-[10px] font-medium">{tab.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}

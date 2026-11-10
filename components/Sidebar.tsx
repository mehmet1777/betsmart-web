'use client';

import { Home, Radio, Calendar, Trophy, Star, BarChart3, User, X } from 'lucide-react';
import { useState } from 'react';
import BetSmartLogo from './BetSmartLogo';

interface SidebarProps {
  isMobileOpen: boolean;
  onMobileClose: () => void;
}

export default function Sidebar({ isMobileOpen, onMobileClose }: SidebarProps) {
  const [activeMenu, setActiveMenu] = useState('home');

  const menuItems = [
    { id: 'home', label: 'Ana Sayfa', icon: Home },
    { id: 'live', label: 'Canlı Maçlar', icon: Radio, badge: '3' },
    { id: 'matches', label: 'Tüm Maçlar', icon: Calendar },
    { id: 'leagues', label: 'Ligler', icon: Trophy },
    { id: 'favorites', label: 'Favoriler', icon: Star },
    { id: 'analytics', label: 'Analiz Merkezi', icon: BarChart3 },
  ];

  const handleMenuClick = (id: string) => {
    setActiveMenu(id);
    onMobileClose();
  };

  return (
    <>
      {/* Mobile Overlay */}
      {isMobileOpen && (
        <div 
          className="fixed inset-0 bg-black/70 backdrop-blur-sm z-40 lg:hidden"
          onClick={onMobileClose}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed top-0 left-0 z-50 h-screen w-72 bg-bg-card border-r border-border-color flex flex-col
        transition-transform duration-300 ease-out
        lg:translate-x-0
        ${isMobileOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        {/* Header */}
        <div className="px-6 py-6 border-b border-border-color flex items-center justify-between">
          <BetSmartLogo variant="full" className="h-8" />
          <button
            onClick={onMobileClose}
            className="lg:hidden text-text-secondary hover:text-text-primary p-1"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-6 space-y-1 overflow-y-auto">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeMenu === item.id;
            
            return (
              <button
                key={item.id}
                onClick={() => handleMenuClick(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${
                  isActive
                    ? 'bg-accent-primary/10 text-accent-primary border border-accent-primary/30'
                    : 'text-text-secondary hover:bg-bg-elevated'
                }`}
              >
                <Icon className={`w-5 h-5 ${isActive ? 'text-accent-primary' : 'text-text-muted'}`} />
                <span className="flex-1 text-left text-sm font-semibold">{item.label}</span>
                {item.badge && (
                  <span className="px-2 py-0.5 text-xs font-bold bg-accent-primary text-bg-app rounded-full">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* User Profile */}
        <div className="px-3 pb-6 border-t border-border-color pt-4">
          <div className="flex items-center gap-3 px-4 py-3 rounded-xl bg-bg-elevated border border-border-color">
            <div className="w-10 h-10 bg-accent-primary rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-bg-app" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-bold text-text-primary truncate">Kullanıcı</p>
              <p className="text-xs text-text-secondary">Premium</p>
            </div>
          </div>
        </div>
      </aside>
    </>
  );
}

'use client';

import { Calendar, ChevronDown } from 'lucide-react';

interface SectionHeaderProps {
  title: string;
  matchCount: number;
  selectedDate?: string;
  onDateChange?: (date: string) => void;
  sortBy?: 'time' | 'league';
  onSortChange?: (sort: 'time' | 'league') => void;
  matches?: any[];  // Maç listesi - tarih gruplama için
}

export default function SectionHeader({ title, matchCount, selectedDate, onDateChange, sortBy = 'time', onSortChange, matches = [] }: SectionHeaderProps) {
  // Bugünden 7 gün sonraya kadar tarihler
  const dates = [];
  const today = new Date();
  today.setHours(0, 0, 0, 0); // Saat kısmını sıfırla
  
  for (let i = 0; i < 7; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() + i);
    dates.push(date);
  }

  const formatDateDisplay = (dateStr: string) => {
    const [year, month, day] = dateStr.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    const displayDay = date.getDate();
    const displayMonth = date.toLocaleDateString('tr-TR', { month: 'short' });
    
    // Bugün mü kontrol et
    const todayDate = new Date();
    todayDate.setHours(0, 0, 0, 0);
    const todayKey = `${todayDate.getFullYear()}-${String(todayDate.getMonth() + 1).padStart(2, '0')}-${String(todayDate.getDate()).padStart(2, '0')}`;
    
    if (dateStr === todayKey) {
      return 'Bugün';
    }
    
    // Yarın mı kontrol et
    const tomorrowDate = new Date(todayDate);
    tomorrowDate.setDate(tomorrowDate.getDate() + 1);
    const tomorrowKey = `${tomorrowDate.getFullYear()}-${String(tomorrowDate.getMonth() + 1).padStart(2, '0')}-${String(tomorrowDate.getDate()).padStart(2, '0')}`;
    
    if (dateStr === tomorrowKey) {
      return 'Yarın';
    }
    
    return `${displayDay} ${displayMonth}`;
  };

  // Her tarih için maç sayısını hesapla
  const getMatchCountForDate = (dateStr: string) => {
    if (!matches || matches.length === 0) return 0;
    
    return matches.filter(match => {
      try {
        // Match.time formatı: "11.11.2026 00:30"
        const matchDateStr = match.time.split(' ')[0]; // "11.11.2026"
        const [day, month, year] = matchDateStr.split('.');
        const matchDateKey = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
        
        return matchDateKey === dateStr;
      } catch (e) {
        return false;
      }
    }).length;
  };

  return (
    <div className="px-4 py-4 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-1 h-6 bg-accent-primary rounded-full"></div>
        <h2 className="text-xl font-bold text-text-primary">{title}</h2>
      </div>
      
      <div className="flex items-center gap-2">
        {/* Sort Toggle Button */}
        {onSortChange && (
          <button
            onClick={() => onSortChange(sortBy === 'time' ? 'league' : 'time')}
            className="p-2 bg-bg-elevated border border-border-color rounded-lg hover:border-accent-primary transition-colors"
            title={sortBy === 'time' ? 'Lige Göre Sırala' : 'Saate Göre Sırala'}
          >
            <span className="text-base">
              {sortBy === 'time' ? '🕐' : '🏆'}
            </span>
          </button>
        )}
      
      {selectedDate && onDateChange ? (
        <div className="relative">
          <select
            value={selectedDate}
            onChange={(e) => onDateChange(e.target.value)}
            className="appearance-none bg-bg-elevated border border-border-color rounded-lg pl-8 pr-8 py-2 text-sm text-text-secondary font-medium cursor-pointer hover:border-accent-primary transition-colors"
          >
            {dates.map(date => {
              const year = date.getFullYear();
              const month = String(date.getMonth() + 1).padStart(2, '0');
              const day = String(date.getDate()).padStart(2, '0');
              const dateKey = `${year}-${month}-${day}`;
              const count = getMatchCountForDate(dateKey);
              return (
                <option key={dateKey} value={dateKey}>
                  {count} Maç, {formatDateDisplay(dateKey)}
                </option>
              );
            })}
          </select>
          {/* Calendar Icon */}
          <Calendar className="absolute left-2 top-1/2 -translate-y-1/2 w-4 h-4 text-text-secondary pointer-events-none" />
          {/* Dropdown Icon */}
          <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 w-4 h-4 text-text-secondary pointer-events-none" />
        </div>
      ) : (
        <button className="flex items-center gap-2 text-text-secondary text-sm">
          <Calendar className="w-4 h-4" />
          <span>{matchCount} Maç, Bugün</span>
          <ChevronDown className="w-4 h-4" />
        </button>
      )}
      </div>
    </div>
  );
}

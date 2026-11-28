'use client';

import { Calendar } from 'lucide-react';

interface SectionHeaderProps {
  title: string;
  matchCount: number;
  selectedDate?: string;
  onDateChange?: (date: string) => void;
  sortBy?: 'time' | 'league' | 'recommended';
  onSortChange?: (sort: 'time' | 'league' | 'recommended') => void;
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
        {/* Sort Toggle Buttons */}
        {onSortChange && (
          <div className="flex items-center gap-1 bg-bg-elevated border border-border-color rounded-lg p-1">
            <button
              onClick={() => onSortChange('time')}
              className={`p-1.5 rounded transition-all ${
                sortBy === 'time' 
                  ? 'bg-accent-primary text-white' 
                  : 'text-text-secondary hover:text-text-primary'
              }`}
              title="Saate Göre"
            >
              <span className="text-base">🕐</span>
            </button>
            <button
              onClick={() => onSortChange('recommended')}
              className={`p-1.5 rounded transition-all ${
                sortBy === 'recommended' 
                  ? 'bg-gradient-to-r from-[#8B5CF6] to-[#6366F1] text-white shadow-lg' 
                  : 'text-text-secondary hover:text-text-primary'
              }`}
              title="Önerilen Önce"
            >
              <span className="text-base">⭐</span>
            </button>
          </div>
        )}
      
      {selectedDate && onDateChange ? (
        <div className="bg-gradient-to-r from-[#8B5CF6]/10 to-[#6366F1]/10 border border-[#8B5CF6]/30 rounded-lg p-1">
          <div className="flex items-center gap-1.5 p-1.5 rounded">
            <Calendar className="w-4 h-4 text-[#8B5CF6]" />
            <span className="text-base text-[#A78BFA] font-semibold whitespace-nowrap leading-none">
              {getMatchCountForDate(selectedDate)} Maç
            </span>
          </div>
        </div>
      ) : (
        <div className="bg-gradient-to-r from-[#8B5CF6]/10 to-[#6366F1]/10 border border-[#8B5CF6]/30 rounded-lg p-1">
          <div className="flex items-center gap-1.5 p-1.5 rounded">
            <Calendar className="w-4 h-4 text-[#8B5CF6]" />
            <span className="text-base text-[#A78BFA] font-semibold whitespace-nowrap leading-none">{matchCount} Maç</span>
          </div>
        </div>
      )}
      </div>
    </div>
  );
}

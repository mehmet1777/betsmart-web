'use client';

interface DateFilterProps {
  selectedDate: string; // 'YYYY-MM-DD' format
  onSelectDate: (date: string) => void;
}

export default function DateFilter({ selectedDate, onSelectDate }: DateFilterProps) {
  // Bugünden 7 gün sonraya kadar tarihler
  const dates = [];
  const today = new Date();
  
  for (let i = 0; i < 7; i++) {
    const date = new Date(today);
    date.setDate(today.getDate() + i);
    dates.push(date);
  }

  const formatDate = (date: Date) => {
    const day = date.getDate();
    const month = date.toLocaleDateString('tr-TR', { month: 'short' });
    const weekday = date.toLocaleDateString('tr-TR', { weekday: 'short' });
    return { day, month, weekday };
  };

  const getDateKey = (date: Date) => {
    return date.toISOString().split('T')[0];
  };

  const isToday = (date: Date) => {
    return getDateKey(date) === getDateKey(new Date());
  };

  return (
    <div className="px-4 py-3 overflow-x-auto scrollbar-hide border-b border-border-color">
      <div className="flex gap-2">
        {dates.map(date => {
          const { day, month, weekday } = formatDate(date);
          const dateKey = getDateKey(date);
          const isSelected = selectedDate === dateKey;
          const today = isToday(date);

          return (
            <button
              key={dateKey}
              onClick={() => onSelectDate(dateKey)}
              className={`flex-shrink-0 px-4 py-3 rounded-xl transition-all min-w-[70px] ${
                isSelected
                  ? 'bg-accent-primary'
                  : 'bg-bg-card border border-border-color'
              }`}
            >
              <div className={`text-xs font-medium mb-1 ${
                isSelected ? 'text-bg-app' : 'text-text-muted'
              }`}>
                {today ? 'Bugün' : weekday}
              </div>
              <div className={`text-xl font-bold mb-0.5 ${
                isSelected ? 'text-bg-app' : 'text-text-primary'
              }`}>
                {day}
              </div>
              <div className={`text-xs ${
                isSelected ? 'text-bg-app opacity-80' : 'text-text-secondary'
              }`}>
                {month}
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}

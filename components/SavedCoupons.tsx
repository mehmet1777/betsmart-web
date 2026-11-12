'use client';

import { useState, useEffect } from 'react';
import { Ticket, Calendar, Trophy, Trash2, ChevronDown, ChevronUp, CheckCircle2, Clock, XCircle, Copy } from 'lucide-react';

interface SavedBetSelection {
  matchId: number;
  prediction: '1' | 'X' | '2';
  match: {
    home: { name: string };
    away: { name: string };
    time: string;
    odds?: { home: string; draw: string; away: string };
  };
}

type CouponStatus = 'pending' | 'won' | 'lost';

interface SavedCoupon {
  id: string;
  name: string;
  date: string;
  selections: SavedBetSelection[];
  totalOdds: number;
  betAmount?: number;
  potentialWin?: number;
  status?: CouponStatus;
  actualWin?: number;
}

export default function SavedCoupons() {
  const [coupons, setCoupons] = useState<SavedCoupon[]>([]);
  const [expandedCouponId, setExpandedCouponId] = useState<string | null>(null);
  const [filterStatus, setFilterStatus] = useState<'all' | CouponStatus>('all');
  const [isFilterOpen, setIsFilterOpen] = useState(false);

  useEffect(() => {
    loadCoupons();
  }, []);

  const loadCoupons = () => {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('savedCoupons');
      if (stored) {
        try {
          const parsed = JSON.parse(stored);
          // Eski kuponlara status ekle (geriye dönük uyumluluk)
          const withStatus = parsed.map((c: SavedCoupon) => ({
            ...c,
            status: c.status || 'pending'
          }));
          setCoupons(withStatus);
        } catch (error) {
          console.error('Error loading coupons:', error);
          setCoupons([]);
        }
      }
    }
  };

  const deleteCoupon = (couponId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    const updated = coupons.filter(c => c.id !== couponId);
    setCoupons(updated);
    if (typeof window !== 'undefined') {
      localStorage.setItem('savedCoupons', JSON.stringify(updated));
    }
  };

  const toggleExpand = (couponId: string) => {
    setExpandedCouponId(expandedCouponId === couponId ? null : couponId);
  };

  const copyCouponCode = (couponId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    navigator.clipboard.writeText(couponId);
    // TODO: Toast bildirimi eklenebilir
  };

  const getStatusConfig = (status: CouponStatus) => {
    switch (status) {
      case 'won':
        return {
          label: 'Kazanan Kupon',
          icon: CheckCircle2,
          color: 'text-accent-primary',
          bg: 'bg-accent-primary/10',
          border: 'border-accent-primary/30',
          glow: 'shadow-accent-primary/20'
        };
      case 'lost':
        return {
          label: 'Kaybeden Kupon',
          icon: XCircle,
          color: 'text-red-500',
          bg: 'bg-red-500/10',
          border: 'border-red-500/30',
          glow: 'shadow-red-500/20'
        };
      default:
        return {
          label: 'Beklemede Kupon',
          icon: Clock,
          color: 'text-yellow-500',
          bg: 'bg-yellow-500/10',
          border: 'border-yellow-500/30',
          glow: 'shadow-yellow-500/20'
        };
    }
  };

  const getOddsForSelection = (selection: SavedBetSelection) => {
    if (!selection.match.odds) return 1.50;
    switch (selection.prediction) {
      case '1': return parseFloat(selection.match.odds.home);
      case 'X': return parseFloat(selection.match.odds.draw);
      case '2': return parseFloat(selection.match.odds.away);
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${day}.${month}.${year} • ${hours}:${minutes}`;
  };

  const formatTurkishNumber = (value: number) => {
    return value.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, '.').replace('.', ',');
  };

  const filteredCoupons = filterStatus === 'all' 
    ? coupons 
    : coupons.filter(c => (c.status || 'pending') === filterStatus);

  const filterOptions = [
    { value: 'all' as const, label: 'Tümü', count: coupons.length },
    { value: 'pending' as const, label: 'Bekleyen', count: coupons.filter(c => (c.status || 'pending') === 'pending').length },
    { value: 'won' as const, label: 'Kazanan', count: coupons.filter(c => c.status === 'won').length },
    { value: 'lost' as const, label: 'Kaybeden', count: coupons.filter(c => c.status === 'lost').length },
  ];

  const totalWinnings = coupons
    .filter(c => c.status === 'won')
    .reduce((sum, c) => sum + (c.actualWin || c.potentialWin || 0), 0);

  if (coupons.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#0A0E13] via-[#0D1117] to-[#0A0E13] pt-16 pb-24">
        <div className="flex flex-col items-center justify-center py-20 text-center px-4">
          <div className="w-28 h-28 bg-gradient-to-br from-bg-card to-bg-elevated rounded-3xl flex items-center justify-center mb-6 border border-border-color/50 shadow-2xl">
            <Ticket className="w-14 h-14 text-accent-primary/40" />
          </div>
          <h2 className="text-2xl font-bold text-text-primary mb-3">
            Henüz Kayıtlı Kupon Yok
          </h2>
          <p className="text-sm text-text-muted max-w-sm leading-relaxed">
            Kupon oluşturduktan sonra "Kaydet" butonuna tıklayarak kuponlarınızı saklayabilirsiniz
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0A0E13] via-[#0D1117] to-[#0A0E13] pt-16 pb-24">
      {/* Header with Gradient */}
      <div className="relative px-4 py-6 bg-gradient-to-br from-[#0D1821]/80 via-[#0A0E13] to-transparent border-b border-accent-primary/10">
        {/* Neon glow effect */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-accent-primary/5 blur-3xl rounded-full pointer-events-none"></div>
        
        <div className="relative">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-14 h-14 bg-gradient-to-br from-accent-primary/20 to-accent-primary/5 rounded-2xl flex items-center justify-center border border-accent-primary/30 shadow-lg shadow-accent-primary/20">
                <Ticket className="w-7 h-7 text-accent-primary" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">Kuponlarım</h1>
                <p className="text-sm text-text-muted">Tüm kuponlarınız burada</p>
              </div>
            </div>
          </div>

          {/* Total Winnings Banner - if has won coupons */}
          {totalWinnings > 0 && (
            <div className="mt-4 p-4 bg-gradient-to-r from-yellow-500/10 via-yellow-500/5 to-transparent rounded-2xl border border-yellow-500/20 shadow-lg">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Trophy className="w-6 h-6 text-yellow-500" />
                  <div>
                    <p className="text-xs text-text-muted mb-0.5">Toplam Kazanç</p>
                    <p className="text-xl font-black text-yellow-500">
                      {formatTurkishNumber(totalWinnings)} ₺
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xs text-text-muted mb-0.5">Kazanan</p>
                  <p className="text-lg font-bold text-accent-primary">
                    {coupons.filter(c => c.status === 'won').length} Kupon
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Filter Dropdown */}
      <div className="px-4 py-4 border-b border-border-color/50">
        <div className="relative">
          <button
            onClick={() => setIsFilterOpen(!isFilterOpen)}
            className="w-full flex items-center justify-between px-4 py-3 bg-gradient-to-br from-bg-card to-bg-elevated rounded-xl border border-border-color hover:border-accent-primary/30 transition-all shadow-lg"
          >
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-text-primary">
                {filterOptions.find(f => f.value === filterStatus)?.label}
              </span>
              <span className="text-xs px-2 py-0.5 bg-accent-primary/10 text-accent-primary rounded-full font-bold">
                {filteredCoupons.length}
              </span>
            </div>
            <ChevronDown className={`w-5 h-5 text-text-muted transition-transform ${isFilterOpen ? 'rotate-180' : ''}`} />
          </button>

          {/* Dropdown Menu */}
          {isFilterOpen && (
            <>
              <div 
                className="fixed inset-0 z-40" 
                onClick={() => setIsFilterOpen(false)}
              />
              <div className="absolute top-full left-0 right-0 mt-2 bg-gradient-to-br from-bg-elevated to-bg-card rounded-xl border border-border-color shadow-2xl overflow-hidden z-50">
                {filterOptions.map((option) => (
                  <button
                    key={option.value}
                    onClick={() => {
                      setFilterStatus(option.value);
                      setIsFilterOpen(false);
                    }}
                    className={`w-full flex items-center justify-between px-4 py-3 transition-colors ${
                      filterStatus === option.value
                        ? 'bg-accent-primary/10 text-accent-primary'
                        : 'text-text-primary hover:bg-white/5'
                    }`}
                  >
                    <span className="text-sm font-semibold">{option.label}</span>
                    <span className={`text-xs px-2 py-0.5 rounded-full font-bold ${
                      filterStatus === option.value
                        ? 'bg-accent-primary/20 text-accent-primary'
                        : 'bg-bg-app text-text-muted'
                    }`}>
                      {option.count}
                    </span>
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      </div>

      {/* Coupons List */}
      <div className="px-4 py-4 space-y-3">
        {filteredCoupons.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-text-muted">Bu kategoride kupon bulunmuyor</p>
          </div>
        ) : (
          filteredCoupons.map((coupon) => {
            const isExpanded = expandedCouponId === coupon.id;
            const statusConfig = getStatusConfig(coupon.status || 'pending');
            const StatusIcon = statusConfig.icon;
            
            return (
              <div
                key={coupon.id}
                className={`bg-gradient-to-br from-[#141B24] to-[#0F1419] rounded-2xl border ${statusConfig.border} overflow-hidden shadow-xl ${statusConfig.glow} transition-all`}
              >
                {/* Coupon Header - Clickable */}
                <div
                  onClick={() => toggleExpand(coupon.id)}
                  className="w-full p-4 hover:bg-white/[0.02] transition-colors cursor-pointer"
                >
                  {/* Status Badge */}
                  <div className="flex items-center justify-between mb-3">
                    <div className={`flex items-center gap-2 px-3 py-1.5 ${statusConfig.bg} rounded-lg border ${statusConfig.border}`}>
                      <StatusIcon className={`w-4 h-4 ${statusConfig.color}`} />
                      <span className={`text-xs font-bold ${statusConfig.color}`}>
                        {statusConfig.label}
                      </span>
                    </div>
                    <ChevronDown className={`w-5 h-5 text-text-muted transition-transform ${isExpanded ? 'rotate-180' : ''}`} />
                  </div>

                  {/* Coupon Info Grid */}
                  <div className="grid grid-cols-2 gap-3 mb-3">
                    {/* Left: Coupon Name & Date */}
                    <div className="text-left">
                      <p className="text-xs text-text-muted mb-1">Kupon Adı</p>
                      <p className="text-sm font-bold text-white truncate">{coupon.name}</p>
                      <div className="flex items-center gap-1.5 mt-2">
                        <Calendar className="w-3 h-3 text-text-muted flex-shrink-0" />
                        <span className="text-xs text-text-muted">
                          {formatDate(coupon.date)}
                        </span>
                      </div>
                    </div>

                    {/* Right: Coupon Code */}
                    <div className="text-right">
                      <p className="text-xs text-text-muted mb-1">Kupon No</p>
                      <button
                        onClick={(e) => copyCouponCode(coupon.id, e)}
                        className="inline-flex items-center gap-1.5 px-2 py-1 bg-bg-app/50 rounded-lg hover:bg-bg-app transition-colors"
                      >
                        <span className="text-xs font-mono font-bold text-accent-primary">
                          #{coupon.id.slice(-8)}
                        </span>
                        <Copy className="w-3 h-3 text-accent-primary" />
                      </button>
                    </div>
                  </div>

                  {/* Stats Row */}
                  <div className="grid grid-cols-3 gap-2 p-3 bg-bg-app/30 rounded-xl">
                    <div className="text-center">
                      <p className="text-xs text-text-muted mb-1">Maç</p>
                      <p className="text-sm font-bold text-white">{coupon.selections.length}</p>
                    </div>
                    <div className="text-center border-x border-border-color/50">
                      <p className="text-xs text-text-muted mb-1">Toplam Oran</p>
                      <p className="text-sm font-bold text-accent-primary">{coupon.totalOdds.toFixed(2)}</p>
                    </div>
                    <div className="text-center">
                      <p className="text-xs text-text-muted mb-1">
                        {coupon.status === 'won' ? 'Kazanç' : 'Potansiyel'}
                      </p>
                      <p className={`text-sm font-bold ${coupon.status === 'won' ? 'text-yellow-500' : 'text-accent-primary'}`}>
                        {formatTurkishNumber(coupon.status === 'won' ? (coupon.actualWin || coupon.potentialWin || 0) : (coupon.potentialWin || 0))} ₺
                      </p>
                    </div>
                  </div>
                </div>

                {/* Expanded Content */}
                {isExpanded && (
                  <div className="border-t border-border-color/30 bg-[#0A0E13]/50">
                    {/* Bet Amount - Compact */}
                    {coupon.betAmount && (
                      <div className="px-3 pt-3 pb-2">
                        <div className="flex items-center justify-between px-3 py-2 bg-[#0F1419]/80 rounded-lg border border-gray-800/40">
                          <span className="text-xs text-text-muted font-medium">Yatırılan Tutar</span>
                          <span className="text-sm font-bold text-white">
                            {formatTurkishNumber(coupon.betAmount)} ₺
                          </span>
                        </div>
                      </div>
                    )}

                    {/* Matches List - Ultra Compact */}
                    <div className="px-3 py-2 space-y-1.5">
                      {coupon.selections.map((selection, index) => {
                        const odds = getOddsForSelection(selection);
                        
                        return (
                          <div
                            key={`${selection.matchId}-${index}`}
                            className="px-2.5 py-2 bg-[#0F1419]/60 rounded-lg border border-gray-800/30 hover:border-gray-700/50 transition-colors"
                          >
                            {/* Match Time - Inline with Icon */}
                            <div className="flex items-center gap-1.5 mb-1.5">
                              <svg className="w-3.5 h-3.5 text-gray-500 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24">
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                              </svg>
                              <span className="text-[10px] text-gray-400 font-medium">
                                {selection.match.time}
                              </span>
                            </div>

                            {/* Teams and Odds - Side by Side */}
                            <div className="flex items-center justify-between gap-2">
                              {/* Teams - Left */}
                              <div className="flex-1 min-w-0">
                                <p className="text-xs font-bold text-white leading-tight truncate">
                                  {selection.match.home.name}
                                </p>
                                <p className="text-xs font-semibold text-gray-400 leading-tight truncate">
                                  {selection.match.away.name}
                                </p>
                              </div>

                              {/* Prediction + Odds - Right */}
                              <div className="flex items-center gap-1.5 flex-shrink-0">
                                <div className="text-right">
                                  <p className="text-[9px] text-gray-500 mb-0.5">Maç Sonucu</p>
                                  <div className="flex items-center gap-1.5">
                                    <div className="w-7 h-7 bg-transparent rounded-md flex items-center justify-center border border-accent-primary">
                                      <span className="text-sm font-black text-accent-primary">
                                        {selection.prediction}
                                      </span>
                                    </div>
                                    <span className="text-base font-bold text-accent-primary">
                                      {odds.toFixed(2)}
                                    </span>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>

                    {/* Delete Button - Compact */}
                    <div className="px-3 pb-3 pt-1">
                      <button
                        onClick={(e) => deleteCoupon(coupon.id, e)}
                        className="w-full bg-red-500/5 hover:bg-red-500/10 text-red-500 font-semibold text-xs py-2.5 rounded-lg transition-all border border-red-500/20 hover:border-red-500/30 flex items-center justify-center gap-1.5"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                        <span>Kuponu Sil</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

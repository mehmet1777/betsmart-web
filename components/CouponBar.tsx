'use client';

import { Ticket } from 'lucide-react';

interface CouponBarProps {
  selectionCount: number;
  totalOdds: number;
  onOpenCoupon: () => void;
}

export default function CouponBar({ selectionCount, totalOdds, onOpenCoupon }: CouponBarProps) {
  return (
    <div className="fixed bottom-16 left-0 right-0 z-40 px-4 safe-bottom">
      <button
        onClick={onOpenCoupon}
        className="w-full bg-accent-primary hover:bg-accent-hover text-bg-app font-bold py-4 rounded-2xl flex items-center justify-between transition-all shadow-xl"
      >
        <div className="flex items-center gap-3 pl-2">
          <Ticket className="w-5 h-5" />
          <div className="text-left">
            <div className="text-sm font-bold">Kuponum</div>
            <div className="text-xs font-medium opacity-80">{selectionCount} seçim</div>
          </div>
        </div>
        <div className="flex items-center gap-3 pr-2">
          <div className="text-right">
            <div className="text-xs font-medium opacity-80">Oran</div>
            <div className="text-sm font-bold">{totalOdds.toFixed(2)}</div>
          </div>
          <div className="text-sm font-bold px-4 py-2 bg-bg-app/20 rounded-xl">
            İncele
          </div>
        </div>
      </button>
    </div>
  );
}

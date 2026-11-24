'use client';

import { useState, useEffect } from 'react';
import { X, TrendingUp, Calendar, Star } from 'lucide-react';
import { useRouter } from 'next/navigation';

interface ParsedCoupon {
  id: string;
  date: string;
  matches: ParsedMatch[];
  totalOdds: number;
  status: 'pending' | 'won' | 'lost';
  featured?: boolean;
}

interface ParsedMatch {
  teams: string;
  mbs?: string;
  tahmin?: string;
  oran?: string;
  mac_saati?: string;
  skor?: string;
}

export default function AnalizKuponlariPage() {
  const router = useRouter();
  const [coupons, setCoupons] = useState<ParsedCoupon[]>([]);
  const [activeTab, setActiveTab] = useState<'gunun' | 'kazanan' | 'kaybeden'>('gunun');
  const [loading, setLoading] = useState(true);
  const [selectedCoupon, setSelectedCoupon] = useState<ParsedCoupon | null>(null);

  // Supabase'den kuponları çek
  useEffect(() => {
    const fetchCoupons = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/nesine-coupons');
        const data = await response.json();
        
        if (data.coupons) {
          // Supabase verisini ParsedCoupon formatına dönüştür
          const formattedCoupons: ParsedCoupon[] = data.coupons.map((c: any) => ({
            id: c.id,
            date: new Date(c.coupon_date).toLocaleDateString('tr-TR', { 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric',
              weekday: 'long'
            }),
            matches: c.matches.map((m: any) => ({
              teams: m.teams,
              mbs: m.mbs,
              tahmin: m.tahmin,
              oran: m.oran,
              mac_saati: m.mac_saati,
              skor: m.skor
            })),
            totalOdds: parseFloat(c.total_odds),
            status: c.status,
            featured: c.featured
          }));
          
          setCoupons(formattedCoupons);
          console.log('✅ Kuponlar yüklendi:', formattedCoupons.length);
        }
      } catch (error) {
        console.error('❌ Kuponlar yüklenirken hata:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchCoupons();
  }, []);

  return (
    <div className="min-h-screen bg-bg-app pb-20">
      {/* Header */}
      <div className="fixed top-0 left-0 right-0 z-50 bg-bg-app border-b border-border-color">
        <div className="flex items-center justify-between px-4 py-3">
          <button onClick={() => router.back()} className="p-2 hover:bg-white/5 rounded-lg transition-colors">
            <X className="w-5 h-5 text-text-primary" />
          </button>
          <h1 className="text-lg font-bold text-text-primary">Analiz Kuponları</h1>
          <div className="w-9" />
        </div>

        {/* Tabs */}
        <div className="flex items-center px-4 pb-3 gap-2">
          <button
            onClick={() => setActiveTab('gunun')}
            className={`flex-1 py-2.5 px-4 rounded-xl font-medium transition-all ${
              activeTab === 'gunun'
                ? 'bg-gradient-to-r from-accent-primary to-accent-secondary text-white'
                : 'bg-card-bg text-text-secondary'
            }`}
          >
            <Star className="w-4 h-4 inline mr-1" />
            Günün Kuponları
          </button>
          <button
            onClick={() => setActiveTab('kazanan')}
            className={`flex-1 py-2.5 px-4 rounded-xl font-medium transition-all ${
              activeTab === 'kazanan'
                ? 'bg-gradient-to-r from-accent-primary to-accent-secondary text-white'
                : 'bg-card-bg text-text-secondary'
            }`}
          >
            <svg className="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Kazanan
          </button>
          <button
            onClick={() => setActiveTab('kaybeden')}
            className={`flex-1 py-2.5 px-4 rounded-xl font-medium transition-all ${
              activeTab === 'kaybeden'
                ? 'bg-gradient-to-r from-accent-primary to-accent-secondary text-white'
                : 'bg-card-bg text-text-secondary'
            }`}
          >
            <svg className="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Kaybeden
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="pt-32 px-4 space-y-4">
        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-2 border-green-500 border-t-transparent"></div>
          </div>
        )}

        {/* Coupon List */}
        {!loading && coupons.filter(c => {
          if (activeTab === 'kazanan') return c.status === 'won';
          if (activeTab === 'kaybeden') return c.status === 'lost';
          return c.status === 'pending'; // Günün kuponları
        }).map((coupon) => (
          <div key={coupon.id} className="bg-card-bg rounded-2xl overflow-hidden border border-border-color">
            {/* Coupon Header */}
            {coupon.featured && (
              <div className="bg-gradient-to-r from-green-500 to-emerald-600 px-4 py-2 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Star className="w-4 h-4 text-white fill-white" />
                  <span className="text-sm font-bold text-white">Öne Çıkan Kupon!</span>
                </div>
              </div>
            )}

            {/* Date */}
            <div className="px-4 pt-3 pb-2 border-b border-border-color">
              <div className="flex items-center gap-2 text-xs text-text-secondary">
                <Calendar className="w-3.5 h-3.5" />
                {coupon.date}
              </div>
            </div>

            {/* Matches - İlk 3 maç göster */}
            <div className="p-3 space-y-2">
              {coupon.matches.slice(0, 3).map((match, idx) => (
                <div key={idx} className="flex items-center gap-2 p-2 bg-bg-darker rounded-lg">
                  <div className="w-7 h-7 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center text-white flex-shrink-0">
                    ⚽
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-semibold text-text-primary text-sm mb-0.5 truncate">{match.teams}</h4>
                    {match.tahmin && (
                      <p className="text-[11px] text-green-400 truncate">{match.tahmin}</p>
                    )}
                    {match.skor && (
                      <p className="text-[10px] text-text-secondary">Skor: {match.skor}</p>
                    )}
                  </div>
                  {match.oran && (
                    <div className="text-right flex-shrink-0">
                      <div className="text-base font-bold text-text-primary">{match.oran}</div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Footer - Toplam Oran */}
            <div className="px-4 py-2.5 bg-bg-darker border-t border-border-color flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="p-1.5 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg">
                  <TrendingUp className="w-3.5 h-3.5 text-white" />
                </div>
                <span className="text-xs text-text-secondary">Toplam Oran</span>
              </div>
              <div className="text-xl font-bold text-green-400">{coupon.totalOdds.toFixed(2)}</div>
            </div>

            {/* Action Button - Sadece 4+ maç varsa göster */}
            {coupon.matches.length > 3 && (
              <div className="px-4 pb-3">
                <button 
                  onClick={() => setSelectedCoupon(coupon)}
                  className="w-full py-2.5 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-bold rounded-xl transition-all flex items-center justify-center gap-2 text-sm"
                >
                  <TrendingUp className="w-4 h-4" />
                  Kupon Detayları ({coupon.matches.length} Maç)
                </button>
              </div>
            )}
          </div>
        ))}

        {/* Empty State */}
        {!loading && coupons.filter(c => {
          if (activeTab === 'kazanan') return c.status === 'won';
          if (activeTab === 'kaybeden') return c.status === 'lost';
          return c.status === 'pending';
        }).length === 0 && (
          <div className="text-center py-12">
            <div className="w-20 h-20 bg-card-bg rounded-full flex items-center justify-center mx-auto mb-4">
              <Star className="w-10 h-10 text-text-secondary" />
            </div>
            <h3 className="text-lg font-bold text-text-primary mb-2">
              {activeTab === 'kazanan' ? 'Kazanan Kupon Yok' : 
               activeTab === 'kaybeden' ? 'Kaybeden Kupon Yok' : 
               'Henüz Kupon Yok'}
            </h3>
            <p className="text-sm text-text-secondary">
              {activeTab === 'gunun' ? 'Nesine Parser ile kupon ekleyin!' : 'Bu kategoride kupon bulunmuyor.'}
            </p>
          </div>
        )}
      </div>

      {/* BetSmart Analiz Ekibi Footer */}
      <div className="fixed bottom-20 left-4 right-4 bg-gradient-to-r from-green-500/10 to-emerald-500/10 border border-green-500/30 rounded-xl p-4 backdrop-blur-sm">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-600 rounded-full flex items-center justify-center flex-shrink-0">
            ✓
          </div>
          <div className="flex-1 min-w-0">
            <h4 className="text-sm font-bold text-white">BetSmart Analiz Ekibi</h4>
            <p className="text-xs text-green-300">Veriye dayalı, profesyonel analizler</p>
          </div>
        </div>
      </div>

      {/* Coupon Detail Modal */}
      {selectedCoupon && (
        <div className="fixed inset-0 bg-black/80 z-50 flex items-end justify-center" onClick={() => setSelectedCoupon(null)}>
          <div className="bg-bg-app rounded-t-3xl w-full max-w-2xl max-h-[85vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            {/* Modal Header */}
            <div className="sticky top-0 bg-bg-app border-b border-border-color px-6 py-4 flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-text-primary">Kupon Detayları</h3>
                <p className="text-sm text-text-secondary">{selectedCoupon.matches.length} Maç</p>
              </div>
              <button 
                onClick={() => setSelectedCoupon(null)}
                className="p-2 hover:bg-white/5 rounded-lg transition-colors"
              >
                <X className="w-5 h-5 text-text-primary" />
              </button>
            </div>

            {/* All Matches */}
            <div className="p-4 space-y-2">
              {selectedCoupon.matches.map((match, idx) => (
                <div key={idx} className="flex items-center gap-2 p-2 bg-card-bg rounded-lg border border-border-color">
                  <div className="w-7 h-7 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center text-white flex-shrink-0 text-xs font-bold">
                    {idx + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-semibold text-text-primary text-sm mb-0.5">{match.teams}</h4>
                    {match.tahmin && (
                      <p className="text-[11px] text-green-400">{match.tahmin}</p>
                    )}
                    {match.skor && (
                      <p className="text-[10px] text-text-secondary">Skor: {match.skor}</p>
                    )}
                  </div>
                  {match.oran && (
                    <div className="text-right flex-shrink-0">
                      <div className="text-base font-bold text-text-primary">{match.oran}</div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Modal Footer */}
            <div className="sticky bottom-0 bg-bg-darker border-t border-border-color px-6 py-4">
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm text-text-secondary">Toplam Oran</span>
                <span className="text-2xl font-bold text-green-400">{selectedCoupon.totalOdds.toFixed(2)}</span>
              </div>
              <button 
                onClick={() => setSelectedCoupon(null)}
                className="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-bold rounded-xl transition-all"
              >
                Kapat
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

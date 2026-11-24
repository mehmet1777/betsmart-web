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
  const [activeTab, setActiveTab] = useState<'gunun' | 'gecmis' | 'analiz'>('gunun');
  const [loading, setLoading] = useState(true);

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
            onClick={() => setActiveTab('gecmis')}
            className={`flex-1 py-2.5 px-4 rounded-xl font-medium transition-all ${
              activeTab === 'gecmis'
                ? 'bg-gradient-to-r from-accent-primary to-accent-secondary text-white'
                : 'bg-card-bg text-text-secondary'
            }`}
          >
            <Calendar className="w-4 h-4 inline mr-1" />
            Geçmiş Kuponlar
          </button>
          <button
            onClick={() => setActiveTab('analiz')}
            className={`flex-1 py-2.5 px-4 rounded-xl font-medium transition-all ${
              activeTab === 'analiz'
                ? 'bg-gradient-to-r from-accent-primary to-accent-secondary text-white'
                : 'bg-card-bg text-text-secondary'
            }`}
          >
            <TrendingUp className="w-4 h-4 inline mr-1" />
            Analiz Ekibi
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="pt-32 px-4 space-y-4">
        {/* Hero Card */}
        <div className="relative bg-gradient-to-br from-green-500/10 via-emerald-500/10 to-teal-500/10 border border-green-500/30 rounded-2xl p-6 overflow-hidden">
          <div className="absolute top-0 right-0 w-48 h-48 bg-green-500/10 rounded-full blur-3xl" />
          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-white" />
              </div>
              <div className="flex-1">
                <h2 className="text-xl font-bold text-white">Analiz Kuponları</h2>
                <p className="text-sm text-green-300">Uzman analiziz ekibimizin hazırladığı en güncel kuponlar burada!</p>
              </div>
            </div>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-2 border-green-500 border-t-transparent"></div>
          </div>
        )}

        {/* Coupon List */}
        {!loading && coupons.map((coupon) => (
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
            <div className="px-4 pt-4 pb-2 border-b border-border-color">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-sm text-text-secondary">
                  <Calendar className="w-4 h-4" />
                  {coupon.date}
                </div>
              </div>
            </div>

            {/* Matches */}
            <div className="p-4 space-y-3">
              {coupon.matches.map((match, idx) => (
                <div key={idx} className="flex items-start gap-3 pb-3 border-b border-border-color last:border-0 last:pb-0">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
                    ⚽
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-semibold text-text-primary mb-1">{match.teams}</h4>
                    {match.tahmin && (
                      <p className="text-xs text-accent-primary mb-1">{match.tahmin}</p>
                    )}
                    {match.skor && (
                      <p className="text-xs text-text-secondary">Skor: {match.skor}</p>
                    )}
                  </div>
                  {match.oran && (
                    <div className="text-right flex-shrink-0">
                      <div className="text-lg font-bold text-text-primary">{match.oran}</div>
                    </div>
                  )}
                </div>
              ))}
            </div>

            {/* Footer */}
            <div className="px-4 py-3 bg-bg-darker border-t border-border-color flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="p-2 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg">
                  <TrendingUp className="w-4 h-4 text-white" />
                </div>
                <span className="text-sm text-text-secondary">Toplam Oran</span>
              </div>
              <div className="text-2xl font-bold text-green-400">{coupon.totalOdds.toFixed(2)}</div>
            </div>

            {/* Action Button */}
            <div className="p-4 bg-bg-darker">
              <button className="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-bold rounded-xl transition-all flex items-center justify-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Kuponu Görüntüle
              </button>
            </div>
          </div>
        ))}

        {/* Empty State */}
        {!loading && coupons.length === 0 && (
          <div className="text-center py-12">
            <div className="w-20 h-20 bg-card-bg rounded-full flex items-center justify-center mx-auto mb-4">
              <Star className="w-10 h-10 text-text-secondary" />
            </div>
            <h3 className="text-lg font-bold text-text-primary mb-2">Henüz Kupon Yok</h3>
            <p className="text-sm text-text-secondary">Nesine Parser ile kupon ekleyin!</p>
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
    </div>
  );
}

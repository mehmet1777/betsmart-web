'use client';

import { useState, useEffect } from 'react';
import { X, Star, Calendar } from 'lucide-react';
import { useRouter } from 'next/navigation';
import PremiumCoupon from '@/components/PremiumCoupon/PremiumCoupon';

interface ParsedCoupon {
  id: string;
  date: string;
  matches: ParsedMatch[];
  totalOdds: number;
  status: 'pending' | 'won' | 'lost';
  featured?: boolean;
  sistemInfo?: string;
}

interface ParsedMatch {
  teams: string;
  mbs?: string;
  tahmin?: string;
  oran?: string;
  mac_saati?: string;
  skor?: string;
  ilk_yari_skor?: string;
}

export default function AnalizKuponlariPage() {
  const router = useRouter();
  const [coupons, setCoupons] = useState<ParsedCoupon[]>([]);
  const [activeTab, setActiveTab] = useState<'gunun' | 'kazanan' | 'kaybeden'>('gunun');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCoupons = async () => {
      try {
        setLoading(true);
        const response = await fetch(`/api/nesine-coupons?t=${Date.now()}`, {
          cache: 'no-store'
        });
        const data = await response.json();
        
        if (data.coupons) {
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
              skor: m.skor,
              ilk_yari_skor: m.ilk_yari_skor
            })),
            totalOdds: parseFloat(c.total_odds),
            status: c.status,
            featured: c.featured,
            sistemInfo: c.sistem_info
          }));
          
          setCoupons(formattedCoupons);
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
    <div className="min-h-screen bg-premium-bg pb-20">
      {/* Header */}
      <div className="fixed top-0 left-0 right-0 z-50 bg-premium-bg/95 backdrop-blur-lg border-b border-premium-border">
        <div className="flex items-center justify-between px-4 py-3">
          <button onClick={() => router.back()} className="p-2 hover:bg-premium-neon/10 rounded-lg transition-colors">
            <X className="w-5 h-5 text-premium-text" />
          </button>
          <h1 className="text-lg font-bold">
            <span className="text-white">Bet</span>
            <span className="text-premium-neon">smart</span>
            <span className="text-premium-text-secondary text-sm ml-2">Kuponları</span>
          </h1>
          <div className="w-9" />
        </div>

        {/* Tabs */}
        <div className="flex items-center px-4 pb-3 gap-2">
          <button
            onClick={() => setActiveTab('gunun')}
            className={`flex-1 py-2.5 px-3 rounded-xl font-medium transition-all text-sm ${
              activeTab === 'gunun'
                ? 'bg-premium-neon text-premium-card shadow-lg shadow-premium-neon/30'
                : 'bg-premium-card-secondary text-premium-text-secondary border border-premium-border'
            }`}
          >
            <Star className="w-3.5 h-3.5 inline mr-1.5" />
            Günün Kuponları
          </button>
          <button
            onClick={() => setActiveTab('kazanan')}
            className={`flex-1 py-2.5 px-3 rounded-xl font-medium transition-all text-sm ${
              activeTab === 'kazanan'
                ? 'bg-premium-neon text-premium-card shadow-lg shadow-premium-neon/30'
                : 'bg-premium-card-secondary text-premium-text-secondary border border-premium-border'
            }`}
          >
            ✓ Kazanan
          </button>
          <button
            onClick={() => setActiveTab('kaybeden')}
            className={`flex-1 py-2.5 px-3 rounded-xl font-medium transition-all text-sm ${
              activeTab === 'kaybeden'
                ? 'bg-premium-neon text-premium-card shadow-lg shadow-premium-neon/30'
                : 'bg-premium-card-secondary text-premium-text-secondary border border-premium-border'
            }`}
          >
            ✕ Kaybeden
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="pt-32 space-y-6">
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-2 border-premium-neon border-t-transparent"></div>
          </div>
        )}

        {!loading && coupons.filter(c => {
          let statusMatch = false;
          if (activeTab === 'kazanan') statusMatch = c.status === 'won';
          else if (activeTab === 'kaybeden') statusMatch = c.status === 'lost';
          else statusMatch = c.status === 'pending';
          const hasMatches = c.matches && c.matches.length > 0;
          return statusMatch && hasMatches;
        }).map((coupon) => (
          <div key={coupon.id}>
            {/* Tarih Bilgisi */}
            {coupon.featured && (
              <div className="px-4 mb-2">
                <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-premium-neon/10 border border-premium-neon/30 rounded-lg">
                  <Star className="w-3.5 h-3.5 text-premium-neon fill-premium-neon" />
                  <span className="text-xs font-bold text-premium-neon">Öne Çıkan Kupon</span>
                </div>
              </div>
            )}
            
            <div className="px-4 mb-3">
              <div className="flex items-center gap-2 text-xs text-premium-text-secondary">
                <Calendar className="w-3.5 h-3.5" />
                {coupon.date}
              </div>
            </div>

            {/* Premium Kupon */}
            <PremiumCoupon 
              matches={coupon.matches}
              totalOdds={coupon.totalOdds}
              sistemInfo={coupon.sistemInfo}
            />
          </div>
        ))}

        {!loading && coupons.filter(c => {
          let statusMatch = false;
          if (activeTab === 'kazanan') statusMatch = c.status === 'won';
          else if (activeTab === 'kaybeden') statusMatch = c.status === 'lost';
          else statusMatch = c.status === 'pending';
          const hasMatches = c.matches && c.matches.length > 0;
          return statusMatch && hasMatches;
        }).length === 0 && (
          <div className="text-center py-12 px-4">
            <div className="w-20 h-20 bg-premium-card-secondary border border-premium-border rounded-full flex items-center justify-center mx-auto mb-4">
              <Star className="w-10 h-10 text-premium-text-secondary" />
            </div>
            <h3 className="text-lg font-bold text-premium-text mb-2">
              {activeTab === 'kazanan' ? 'Kazanan Kupon Yok' : 
               activeTab === 'kaybeden' ? 'Kaybeden Kupon Yok' : 
               'Henüz Kupon Yok'}
            </h3>
            <p className="text-sm text-premium-text-secondary">
              {activeTab === 'gunun' ? 'Nesine Parser ile kupon ekleyin!' : 'Bu kategoride kupon bulunmuyor.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

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
  sistemInfo?: string; // Sistem bilgisi
}

interface ParsedMatch {
  teams: string;
  mbs?: string;
  tahmin?: string;
  oran?: string;
  mac_saati?: string;
  skor?: string;
  ilk_yari_skor?: string; // İlk yarı skoru
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
        // Cache bypass için timestamp ekle
        const response = await fetch(`/api/nesine-coupons?t=${Date.now()}`, {
          cache: 'no-store'
        });
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
              skor: m.skor,
              ilk_yari_skor: m.ilk_yari_skor // İlk yarı skoru ekle
            })),
            totalOdds: parseFloat(c.total_odds),
            status: c.status,
            featured: c.featured,
            sistemInfo: c.sistem_info // Sistem bilgisi ekle
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
          // Önce status'e göre filtrele
          let statusMatch = false;
          if (activeTab === 'kazanan') statusMatch = c.status === 'won';
          else if (activeTab === 'kaybeden') statusMatch = c.status === 'lost';
          else statusMatch = c.status === 'pending'; // Günün kuponları
          
          // Sonra maçı olan kuponları filtrele
          const hasMatches = c.matches && c.matches.length > 0;
          
          return statusMatch && hasMatches;
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

            {/* Matches - İlk 3 maç göster - Nesine tarzı */}
            <div className="divide-y divide-border-color">
              {coupon.matches && coupon.matches.length > 0 ? (
                coupon.matches.slice(0, 3).map((match, idx) => (
                  <div key={idx} className="p-4">
                    {/* Üst satır: Takımlar ve Oran */}
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <div className="flex items-start gap-2 flex-1 min-w-0">
                        <div className="w-6 h-6 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center text-white flex-shrink-0 text-xs font-bold mt-0.5">
                          ⚽
                        </div>
                        <div className="flex-1 min-w-0">
                          <h4 className="font-bold text-text-primary text-sm leading-tight mb-1">
                            {match.teams}
                          </h4>
                          {match.mac_saati && (
                            <p className="text-[11px] text-text-secondary">
                              {match.mac_saati}
                            </p>
                          )}
                        </div>
                      </div>
                      <div className="text-right flex-shrink-0">
                        <div className="text-lg font-bold text-text-primary">{match.oran || '-'}</div>
                      </div>
                    </div>

                    {/* Alt satır: Tahmin + Skorlar */}
                    <div className="flex items-center gap-2 ml-8">
                      {match.tahmin && (
                        <span className="inline-flex items-center px-2.5 py-1 bg-green-500/20 text-green-400 text-xs font-medium rounded-md">
                          {match.tahmin}
                        </span>
                      )}
                      {match.mbs && (
                        <span className="inline-flex items-center px-2 py-0.5 bg-gray-500/20 text-gray-400 text-[10px] font-medium rounded">
                          {match.mbs} & Var
                        </span>
                      )}
                      {match.skor && (
                        <div className="flex items-center gap-1.5 text-[11px]">
                          <span className="text-text-secondary">MS:</span>
                          <span className="font-semibold text-text-primary">{match.skor}</span>
                          {match.ilk_yari_skor && (
                            <>
                              <span className="text-text-secondary ml-1">İY:</span>
                              <span className="font-semibold text-green-400">{match.ilk_yari_skor}</span>
                            </>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center text-text-secondary text-sm py-6">
                  Maç bilgisi bulunamadı
                </div>
              )}
            </div>

            {/* Footer - Toplam Oran ve Sistem */}
            <div className="px-4 py-3 bg-bg-darker border-t border-border-color">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-sm text-text-secondary font-medium">Toplam Oran</span>
                  {coupon.matches && coupon.matches.length > 1 && (
                    <span className="text-xs text-text-secondary/70">
                      Misli {coupon.matches.length}
                    </span>
                  )}
                  {coupon.sistemInfo && (
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-green-500/20 text-green-400 text-xs font-medium rounded">
                      <span>📋</span>
                      {coupon.sistemInfo}
                    </span>
                  )}
                </div>
                <div className="text-2xl font-bold text-green-400">
                  {coupon.totalOdds.toLocaleString('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </div>
              </div>
            </div>

            {/* Action Button - Sadece 4+ maç varsa göster */}
            {coupon.matches && coupon.matches.length > 3 && (
              <div className="px-4 pb-4 pt-2">
                <button 
                  onClick={() => setSelectedCoupon(coupon)}
                  className="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-bold rounded-xl transition-all flex items-center justify-center gap-2 shadow-lg shadow-green-500/25"
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
          let statusMatch = false;
          if (activeTab === 'kazanan') statusMatch = c.status === 'won';
          else if (activeTab === 'kaybeden') statusMatch = c.status === 'lost';
          else statusMatch = c.status === 'pending';
          const hasMatches = c.matches && c.matches.length > 0;
          return statusMatch && hasMatches;
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
            <div className="divide-y divide-border-color">
              {selectedCoupon.matches.map((match, idx) => (
                <div key={idx} className="p-4">
                  {/* Üst satır: Numara + Takımlar + Oran */}
                  <div className="flex items-start justify-between gap-3 mb-2">
                    <div className="flex items-start gap-2 flex-1 min-w-0">
                      <div className="w-6 h-6 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center text-white flex-shrink-0 text-xs font-bold mt-0.5">
                        {idx + 1}
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-bold text-text-primary text-sm leading-tight mb-1">
                          {match.teams}
                        </h4>
                        {match.mac_saati && (
                          <p className="text-[11px] text-text-secondary">
                            {match.mac_saati}
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="text-right flex-shrink-0">
                      <div className="text-lg font-bold text-text-primary">{match.oran || '-'}</div>
                    </div>
                  </div>

                  {/* Alt satır: Tahmin + Skorlar */}
                  <div className="flex items-center gap-2 ml-8 flex-wrap">
                    {match.tahmin && (
                      <span className="inline-flex items-center px-2.5 py-1 bg-green-500/20 text-green-400 text-xs font-medium rounded-md">
                        {match.tahmin}
                      </span>
                    )}
                    {match.mbs && (
                      <span className="inline-flex items-center px-2 py-0.5 bg-gray-500/20 text-gray-400 text-[10px] font-medium rounded">
                        {match.mbs} & Var
                      </span>
                    )}
                    {match.skor && (
                      <div className="flex items-center gap-1.5 text-[11px]">
                        <span className="text-text-secondary">MS:</span>
                        <span className="font-semibold text-text-primary">{match.skor}</span>
                        {match.ilk_yari_skor && (
                          <>
                            <span className="text-text-secondary ml-1">İY:</span>
                            <span className="font-semibold text-green-400">{match.ilk_yari_skor}</span>
                          </>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </div>

            {/* Modal Footer */}
            <div className="sticky bottom-0 bg-bg-darker border-t border-border-color px-6 py-4">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center gap-3">
                  <span className="text-sm text-text-secondary font-medium">Toplam Oran</span>
                  {selectedCoupon.matches && selectedCoupon.matches.length > 1 && (
                    <span className="text-xs text-text-secondary/70">
                      Misli {selectedCoupon.matches.length}
                    </span>
                  )}
                  {selectedCoupon.sistemInfo && (
                    <span className="inline-flex items-center gap-1 px-2 py-1 bg-green-500/20 text-green-400 text-xs font-medium rounded">
                      <span>📋</span>
                      {selectedCoupon.sistemInfo}
                    </span>
                  )}
                </div>
                <span className="text-2xl font-bold text-green-400">
                  {selectedCoupon.totalOdds.toLocaleString('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                </span>
              </div>
              <button 
                onClick={() => setSelectedCoupon(null)}
                className="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-bold rounded-xl transition-all shadow-lg shadow-green-500/25"
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

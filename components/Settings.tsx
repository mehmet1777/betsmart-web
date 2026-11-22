'use client';

import { Bell, Moon, Globe, HelpCircle, Info, ChevronRight, Sliders } from 'lucide-react';
import { useState, useEffect } from 'react';

export default function Settings() {
  // Tolerans ayarları - localStorage'dan yükle
  const [exactTolerance, setExactTolerance] = useState(0.01);
  const [similarTolerance, setSimilarTolerance] = useState(0.02);
  const [hasChanges, setHasChanges] = useState(false);

  // Component mount olduğunda localStorage'dan yükle
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const storedExact = localStorage.getItem('exactTolerance');
      const storedSimilar = localStorage.getItem('similarTolerance');
      
      if (storedExact) setExactTolerance(parseFloat(storedExact));
      if (storedSimilar) setSimilarTolerance(parseFloat(storedSimilar));
    }
  }, []);

  // Tolerans değiştiğinde
  const handleToleranceChange = (type: 'exact' | 'similar', value: number) => {
    if (type === 'exact') {
      setExactTolerance(value);
    } else {
      setSimilarTolerance(value);
    }
    setHasChanges(true);
  };

  // Varsayılana dön
  const resetToDefaults = () => {
    setExactTolerance(0.01);
    setSimilarTolerance(0.02);
    setHasChanges(true);
  };

  // Kaydet
  const saveSettings = () => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('exactTolerance', exactTolerance.toString());
      localStorage.setItem('similarTolerance', similarTolerance.toString());
      setHasChanges(false);
      
      // Cache'i sil - yeni toleransla analiz yapılsın
      localStorage.removeItem('lastAnalysisTime');
      localStorage.removeItem('cachedAnalysisResults');
      console.log('🗑️ Cache temizlendi, yeni analiz tetiklenecek');
      
      // Yeniden analiz tetikle
      const event = new CustomEvent('reAnalyzeMatches');
      window.dispatchEvent(event);
      
      // Modern toast notification göster
      showToast();
    }
  };

  // Toast notification
  const [showToastNotif, setShowToastNotif] = useState(false);
  
  const showToast = () => {
    setShowToastNotif(true);
    setTimeout(() => {
      setShowToastNotif(false);
    }, 3000);
  };

  return (
    <div className="min-h-screen bg-bg-app pb-32 pt-20 px-4">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-text-primary mb-2">Ayarlar</h1>
          <p className="text-text-secondary">Uygulamayı kişiselleştir</p>
        </div>

        {/* Settings Sections */}
        <div className="space-y-6">
          {/* Analiz Ayarları */}
          <section className="bg-bg-card rounded-2xl border border-border-color overflow-hidden">
            <h2 className="text-lg font-bold text-text-primary px-5 py-4 border-b border-border-color flex items-center gap-2">
              <Sliders className="w-5 h-5 text-accent-primary" />
              Analiz Toleransı
            </h2>
            
            <div className="p-5 space-y-8">
              {/* Tam Eşleşme Slider */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <h3 className="text-sm font-bold text-text-primary">Tam Eşleşme Toleransı</h3>
                    <p className="text-xs text-text-secondary mt-1">Daha kesin sonuçlar</p>
                  </div>
                  <div className="text-right">
                    <span className="text-2xl font-bold text-accent-primary">±{exactTolerance.toFixed(3)}</span>
                  </div>
                </div>
                
                <input
                  type="range"
                  min="0.01"
                  max="0.10"
                  step="0.005"
                  value={exactTolerance}
                  onChange={(e) => handleToleranceChange('exact', parseFloat(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-accent-primary slider"
                />
                
                <div className="flex justify-between text-xs text-text-muted mt-2">
                  <span>0.010</span>
                  <span>0.055</span>
                  <span>0.100</span>
                </div>
              </div>

              {/* Benzer Eşleşme Slider */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div>
                    <h3 className="text-sm font-bold text-text-primary">Benzer Eşleşme Toleransı</h3>
                    <p className="text-xs text-text-secondary mt-1">Daha geniş sonuçlar</p>
                  </div>
                  <div className="text-right">
                    <span className="text-2xl font-bold text-accent-primary">±{similarTolerance.toFixed(3)}</span>
                  </div>
                </div>
                
                <input
                  type="range"
                  min="0.02"
                  max="0.20"
                  step="0.005"
                  value={similarTolerance}
                  onChange={(e) => handleToleranceChange('similar', parseFloat(e.target.value))}
                  className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-accent-primary slider"
                />
                
                <div className="flex justify-between text-xs text-text-muted mt-2">
                  <span>0.020</span>
                  <span>0.110</span>
                  <span>0.200</span>
                </div>
              </div>

              {/* Info Box */}
              <div className="bg-accent-primary/5 border border-accent-primary/20 rounded-xl p-4">
                <p className="text-xs text-text-secondary">
                  <span className="font-bold text-accent-primary">💡 İpucu:</span> Düşük tolerans daha az ama kesin sonuç verir. Yüksek tolerans daha fazla ama çeşitli sonuç verir.
                </p>
              </div>

              {/* Action Buttons */}
              <div className="flex gap-3">
                <button
                  onClick={resetToDefaults}
                  className="flex-1 px-4 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-xl font-semibold transition-colors"
                >
                  Varsayılana Dön
                </button>
                <button
                  onClick={saveSettings}
                  disabled={!hasChanges}
                  className={`flex-1 px-4 py-3 rounded-xl font-semibold transition-all ${
                    hasChanges
                      ? 'bg-gradient-to-r from-[#8B5CF6] to-[#6366F1] text-white hover:shadow-lg hover:shadow-accent-primary/50'
                      : 'bg-gray-700 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  {hasChanges ? 'Kaydet' : 'Kaydedildi ✓'}
                </button>
              </div>
            </div>
          </section>

          {/* Bildirimler */}
          <section className="bg-bg-card rounded-2xl border border-border-color overflow-hidden">
            <h2 className="text-lg font-bold text-text-primary px-5 py-4 border-b border-border-color">
              Bildirimler
            </h2>
            <div className="divide-y divide-border-color">
              <SettingItem
                icon={Bell}
                title="Oran Değişiklikleri"
                description="Önemli oran değişikliklerinde bildir"
                hasToggle
                defaultChecked={true}
              />
              <SettingItem
                icon={Bell}
                title="Canlı Maç Bildirimleri"
                description="Canlı maçlar başladığında bildir"
                hasToggle
                defaultChecked={false}
              />
            </div>
          </section>

          {/* Görünüm */}
          <section className="bg-bg-card rounded-2xl border border-border-color overflow-hidden">
            <h2 className="text-lg font-bold text-text-primary px-5 py-4 border-b border-border-color">
              Görünüm
            </h2>
            <div className="divide-y divide-border-color">
              <SettingItem
                icon={Moon}
                title="Karanlık Mod"
                description="Varsayılan olarak açık"
                hasToggle
                defaultChecked={true}
                disabled
              />
              <SettingItem
                icon={Globe}
                title="Dil"
                description="Türkçe"
                hasChevron
              />
            </div>
          </section>

          {/* Hakkında */}
          <section className="bg-bg-card rounded-2xl border border-border-color overflow-hidden">
            <h2 className="text-lg font-bold text-text-primary px-5 py-4 border-b border-border-color">
              Hakkında
            </h2>
            <div className="divide-y divide-border-color">
              <SettingItem
                icon={HelpCircle}
                title="Yardım & Destek"
                hasChevron
              />
              <SettingItem
                icon={Info}
                title="Uygulama Bilgisi"
                description="Versiyon 1.0.0"
                hasChevron
              />
            </div>
          </section>

          {/* Version Info */}
          <div className="text-center py-8">
            <p className="text-text-muted text-sm">BetSmart © 2024</p>
            <p className="text-text-muted text-xs mt-1">Tüm hakları saklıdır</p>
          </div>
        </div>
      </div>

      {/* Modern Toast Notification */}
      {showToastNotif && (
        <div className="fixed bottom-24 left-1/2 -translate-x-1/2 z-50 animate-slide-up">
          <div className="bg-gradient-to-r from-[#8B5CF6] to-[#6366F1] text-white px-6 py-4 rounded-2xl shadow-2xl flex items-center gap-3 min-w-[280px]">
            <div className="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div>
              <p className="font-bold text-base">Ayarlar Kaydedildi!</p>
              <p className="text-sm text-white/80">Değişiklikler uygulandı</p>
            </div>
          </div>
        </div>
      )}

      {/* Custom Slider Styles */}
      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          width: 24px;
          height: 24px;
          border-radius: 50%;
          background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
          cursor: pointer;
          box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.2);
          transition: all 0.2s ease;
        }

        .slider::-webkit-slider-thumb:hover {
          transform: scale(1.1);
          box-shadow: 0 0 0 6px rgba(139, 92, 246, 0.3);
        }

        .slider::-moz-range-thumb {
          width: 24px;
          height: 24px;
          border-radius: 50%;
          background: linear-gradient(135deg, #8B5CF6 0%, #6366F1 100%);
          cursor: pointer;
          border: none;
          box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.2);
          transition: all 0.2s ease;
        }

        .slider::-moz-range-thumb:hover {
          transform: scale(1.1);
          box-shadow: 0 0 0 6px rgba(139, 92, 246, 0.3);
        }

        @keyframes slide-up {
          from {
            opacity: 0;
            transform: translate(-50%, 20px);
          }
          to {
            opacity: 1;
            transform: translate(-50%, 0);
          }
        }

        .animate-slide-up {
          animation: slide-up 0.3s ease-out forwards;
        }
      `}</style>
    </div>
  );
}

interface SettingItemProps {
  icon: any;
  title: string;
  description?: string;
  hasToggle?: boolean;
  hasChevron?: boolean;
  defaultChecked?: boolean;
  disabled?: boolean;
}

function SettingItem({ 
  icon: Icon, 
  title, 
  description, 
  hasToggle, 
  hasChevron,
  defaultChecked = false,
  disabled = false
}: SettingItemProps) {
  return (
    <div className="px-5 py-4 flex items-center gap-4 hover:bg-bg-elevated transition-colors">
      <div className="w-10 h-10 rounded-xl bg-accent-primary/10 flex items-center justify-center">
        <Icon className="w-5 h-5 text-accent-primary" />
      </div>
      
      <div className="flex-1 min-w-0">
        <h3 className="text-sm font-semibold text-text-primary">{title}</h3>
        {description && (
          <p className="text-xs text-text-secondary mt-0.5">{description}</p>
        )}
      </div>

      {hasToggle && (
        <label className="relative inline-flex items-center cursor-pointer">
          <input 
            type="checkbox" 
            className="sr-only peer" 
            defaultChecked={defaultChecked}
            disabled={disabled}
          />
          <div className={`w-11 h-6 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-accent-primary ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}></div>
        </label>
      )}

      {hasChevron && (
        <ChevronRight className="w-5 h-5 text-text-muted" />
      )}
    </div>
  );
}

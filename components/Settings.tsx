'use client';

import { Bell, Moon, Globe, HelpCircle, Info, ChevronRight } from 'lucide-react';

export default function Settings() {
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

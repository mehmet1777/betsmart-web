'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence, useReducedMotion } from 'framer-motion';
import Image from 'next/image';

type InstallStep = 'discover' | 'select' | 'install' | 'complete';

export default function PWAInstallPrompt() {
  const [isVisible, setIsVisible] = useState(false);
  const [currentStep, setCurrentStep] = useState<InstallStep>('discover');
  const [isIOS, setIsIOS] = useState(false);
  const [isStandalone, setIsStandalone] = useState(false);
  const [isDismissed, setIsDismissed] = useState(false);
  const prefersReducedMotion = useReducedMotion();

  useEffect(() => {
    // Check if iOS Safari
    const ua = window.navigator.userAgent;
    const iOS = /iPad|iPhone|iPod/.test(ua) && !(window as any).MSStream;
    setIsIOS(iOS);

    // Check if already installed (standalone mode)
    const standalone = window.matchMedia('(display-mode: standalone)').matches;
    setIsStandalone(standalone);

    // Check if user dismissed before
    const dismissed = localStorage.getItem('betsmart_pwa_dismissed');
    setIsDismissed(dismissed === 'true');

    // Show prompt after 2 seconds on iOS Safari, if not dismissed and not installed
    if (iOS && !standalone && !dismissed) {
      const timer = setTimeout(() => {
        setIsVisible(true);
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleDismiss = () => {
    localStorage.setItem('betsmart_pwa_dismissed', 'true');
    setIsVisible(false);
  };

  const handleStepComplete = () => {
    if (currentStep === 'discover') setCurrentStep('select');
    else if (currentStep === 'select') setCurrentStep('install');
    else if (currentStep === 'install') setCurrentStep('complete');
  };

  const handleClose = () => {
    handleDismiss();
  };

  // Don't render if not iOS, already installed, or dismissed
  if (!isIOS || isStandalone || isDismissed) return null;

  const springTransition = prefersReducedMotion 
    ? { duration: 0 }
    : { type: 'spring', damping: 25, stiffness: 300 };

  return (
    <AnimatePresence>
      {isVisible && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: prefersReducedMotion ? 0 : 0.4 }}
            className="fixed inset-0 bg-black/90 backdrop-blur-xl z-[100]"
            onClick={handleClose}
          />

          {/* Main Container */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={springTransition}
            className="fixed inset-4 z-[101] flex items-center justify-center p-4"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="relative w-full max-w-md">
              {/* Close Button */}
              <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={handleClose}
                className="absolute -top-12 right-0 w-10 h-10 flex items-center justify-center rounded-full bg-white/5 backdrop-blur-sm border border-white/10 text-white/60 hover:text-white hover:bg-white/10 transition-colors"
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </motion.button>

              {/* Content Card */}
              <div className="relative bg-gradient-to-b from-[#0A0F1A] to-[#050810] rounded-3xl border border-white/10 overflow-hidden shadow-2xl">
                {/* Ambient Light Effect */}
                <div className="absolute inset-0 opacity-30">
                  <div className="absolute top-0 left-1/2 -translate-x-1/2 w-96 h-96 bg-[#19E98B]/20 rounded-full blur-[120px]" />
                </div>

                {/* Content */}
                <div className="relative z-10 p-8">
                  {currentStep === 'discover' && (
                    <DiscoverStep onNext={handleStepComplete} prefersReducedMotion={prefersReducedMotion} />
                  )}
                  {currentStep === 'select' && (
                    <SelectStep onNext={handleStepComplete} prefersReducedMotion={prefersReducedMotion} />
                  )}
                  {currentStep === 'install' && (
                    <InstallStep onNext={handleStepComplete} onClose={handleClose} prefersReducedMotion={prefersReducedMotion} />
                  )}
                  {currentStep === 'complete' && (
                    <CompleteStep onClose={handleClose} prefersReducedMotion={prefersReducedMotion} />
                  )}
                </div>

                {/* Step Indicators */}
                <div className="flex items-center justify-center gap-2 pb-6">
                  {(['discover', 'select', 'install'] as InstallStep[]).map((step, index) => (
                    <motion.div
                      key={step}
                      className={`h-1.5 rounded-full transition-all duration-300 ${
                        currentStep === step 
                          ? 'w-8 bg-[#19E98B]' 
                          : index < ['discover', 'select', 'install'].indexOf(currentStep)
                          ? 'w-1.5 bg-[#19E98B]/50'
                          : 'w-1.5 bg-white/10'
                      }`}
                      layoutId={`step-${step}`}
                    />
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

// STEP 01: DISCOVER
function DiscoverStep({ onNext, prefersReducedMotion }: { onNext: () => void; prefersReducedMotion: boolean }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: prefersReducedMotion ? 0 : 0.5 }}
      className="space-y-8"
    >
      {/* Logo with premium effects */}
      <div className="flex justify-center">
        <motion.div
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2, duration: prefersReducedMotion ? 0 : 0.6, type: 'spring', damping: 20 }}
          className="relative"
        >
          {/* Glow effect */}
          <div className="absolute inset-0 bg-[#19E98B]/20 rounded-3xl blur-2xl scale-110" />
          
          {/* Logo container with 3D depth */}
          <div className="relative w-24 h-24 rounded-3xl bg-gradient-to-br from-[#19E98B]/10 to-[#0FA760]/10 border border-[#19E98B]/20 flex items-center justify-center shadow-2xl">
            <Image 
              src="/apple-touch-icon.png" 
              alt="BetSmart" 
              width={80} 
              height={80}
              className="rounded-2xl"
            />
          </div>
        </motion.div>
      </div>

      {/* Text content with editorial typography */}
      <div className="text-center space-y-3">
        <motion.h2
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: prefersReducedMotion ? 0 : 0.5 }}
          className="text-2xl font-bold text-white tracking-tight"
        >
          BetSmart'ı Yükleyin
        </motion.h2>
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4, duration: prefersReducedMotion ? 0 : 0.5 }}
          className="text-sm text-white/60 leading-relaxed max-w-xs mx-auto font-normal"
        >
          Profesyonel bahis analizi artık cebinizde. Tam ekran deneyimi için ana ekrana ekleyin.
        </motion.p>
      </div>

      {/* Features with staggered reveal */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={{
          visible: {
            transition: {
              staggerChildren: prefersReducedMotion ? 0 : 0.1,
              delayChildren: 0.5,
            },
          },
        }}
        className="space-y-3"
      >
        {[
          { icon: '⚡', text: 'Hızlı Analiz', desc: 'Gerçek zamanlı oran karşılaştırma' },
          { icon: '🎯', text: 'Akıllı Kupon', desc: 'AI destekli tahmin önerileri' },
          { icon: '📊', text: 'Detaylı İstatistik', desc: '350.000+ geçmiş maç verisi' },
        ].map((feature, i) => (
          <motion.div
            key={i}
            variants={{
              hidden: { opacity: 0, x: -20 },
              visible: { opacity: 1, x: 0 },
            }}
            className="flex items-center gap-4 p-3 rounded-xl bg-white/5 backdrop-blur-sm border border-white/5"
          >
            <div className="w-10 h-10 rounded-xl bg-[#19E98B]/10 flex items-center justify-center text-xl flex-shrink-0">
              {feature.icon}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-white">{feature.text}</p>
              <p className="text-xs text-white/50">{feature.desc}</p>
            </div>
          </motion.div>
        ))}
      </motion.div>

      {/* CTA Button with premium interaction */}
      <motion.button
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8, duration: prefersReducedMotion ? 0 : 0.5 }}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={onNext}
        className="w-full py-4 rounded-2xl bg-gradient-to-r from-[#19E98B] to-[#0FA760] text-white font-semibold text-sm shadow-lg shadow-[#19E98B]/25 hover:shadow-xl hover:shadow-[#19E98B]/40 transition-shadow"
      >
        Nasıl Yüklenir?
      </motion.button>
    </motion.div>
  );
}

// STEP 02: SELECT
function SelectStep({ onNext, prefersReducedMotion }: { onNext: () => void; prefersReducedMotion: boolean }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: prefersReducedMotion ? 0 : 0.5 }}
      className="space-y-8"
    >
      {/* Step Title */}
      <div className="text-center space-y-2">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: 'spring', damping: 20 }}
          className="w-12 h-12 rounded-full bg-[#19E98B]/10 border border-[#19E98B]/20 flex items-center justify-center mx-auto mb-4"
        >
          <span className="text-2xl">📲</span>
        </motion.div>
        <h3 className="text-xl font-bold text-white">Adım 1: Paylaş Butonuna Dokunun</h3>
        <p className="text-sm text-white/60">Safari'nin alt kısmındaki paylaş ikonunu bulun</p>
      </div>

      {/* iOS Safari Share Icon Illustration */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.3, duration: prefersReducedMotion ? 0 : 0.6 }}
        className="relative"
      >
        {/* Mock Safari Bottom Bar */}
        <div className="relative mx-auto max-w-[280px] bg-gradient-to-b from-[#1C1C1E] to-[#000000] rounded-3xl p-6 border border-white/10 shadow-2xl">
          {/* Safari URL Bar (minimal) */}
          <div className="mb-8 flex items-center justify-center gap-2 py-2 px-4 bg-white/5 rounded-full border border-white/5">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" className="text-white/40">
              <path d="M6 2h2M6 12h2M2 6v2M12 6v2" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
            </svg>
            <span className="text-xs text-white/40 font-medium">betsmart-web.vercel.app</span>
          </div>

          {/* Bottom Navigation Bar */}
          <div className="flex items-center justify-around py-2">
            <button className="w-10 h-10 flex items-center justify-center text-white/30">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M15 19l-7-7 7-7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            <button className="w-10 h-10 flex items-center justify-center text-white/30">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M9 5l7 7-7 7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
            
            {/* Highlighted Share Button */}
            <motion.button
              animate={{
                scale: [1, 1.1, 1],
                boxShadow: [
                  '0 0 0 0px rgba(25, 233, 139, 0)',
                  '0 0 0 8px rgba(25, 233, 139, 0.2)',
                  '0 0 0 0px rgba(25, 233, 139, 0)',
                ],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
              className="relative w-12 h-12 flex items-center justify-center text-[#19E98B] bg-[#19E98B]/10 rounded-xl border border-[#19E98B]/30"
            >
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 13V3M10 3L6 7M10 3l4 4M3 17h14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              
              {/* Pulsing indicator */}
              <motion.div
                animate={{ scale: [1, 1.2, 1], opacity: [1, 0, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute -top-1 -right-1 w-3 h-3 bg-[#19E98B] rounded-full"
              />
            </motion.button>

            <button className="w-10 h-10 flex items-center justify-center text-white/30">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <rect x="3" y="3" width="18" height="18" rx="2" stroke="currentColor" strokeWidth="2"/>
                <rect x="7" y="7" width="10" height="10" rx="1" stroke="currentColor" strokeWidth="2"/>
              </svg>
            </button>
            <button className="w-10 h-10 flex items-center justify-center text-white/30">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M12 6v.01M12 12v.01M12 18v.01" stroke="currentColor" strokeWidth="3" strokeLinecap="round"/>
              </svg>
            </button>
          </div>
        </div>

        {/* Animated Arrow Pointer */}
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
          className="absolute -bottom-8 left-1/2 -translate-x-1/2 text-[#19E98B]"
        >
          <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
            <path d="M16 8v16m0 0l-6-6m6 6l6-6" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </motion.div>
      </motion.div>

      {/* Next Button */}
      <motion.button
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={onNext}
        className="w-full py-4 rounded-2xl bg-gradient-to-r from-[#19E98B] to-[#0FA760] text-white font-semibold text-sm shadow-lg"
      >
        Devam Et
      </motion.button>
    </motion.div>
  );
}

// STEP 03: INSTALL
function InstallStep({ onNext, onClose, prefersReducedMotion }: { onNext: () => void; onClose: () => void; prefersReducedMotion: boolean }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: -20 }}
      transition={{ duration: prefersReducedMotion ? 0 : 0.5 }}
      className="space-y-8"
    >
      {/* Step Title */}
      <div className="text-center space-y-2">
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: 'spring', damping: 20 }}
          className="w-12 h-12 rounded-full bg-[#19E98B]/10 border border-[#19E98B]/20 flex items-center justify-center mx-auto mb-4"
        >
          <span className="text-2xl">✨</span>
        </motion.div>
        <h3 className="text-xl font-bold text-white">Adım 2: Ana Ekrana Ekle</h3>
        <p className="text-sm text-white/60">Açılan menüden "Ana Ekrana Ekle" seçeneğine dokunun</p>
      </div>

      {/* iOS Share Sheet Mock */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3, duration: prefersReducedMotion ? 0 : 0.6 }}
        className="relative"
      >
        <div className="bg-gradient-to-b from-[#1C1C1E]/95 to-[#2C2C2E]/95 backdrop-blur-xl rounded-3xl border border-white/10 shadow-2xl overflow-hidden max-w-[300px] mx-auto">
          {/* Sheet Handle */}
          <div className="pt-2 pb-4 flex justify-center">
            <div className="w-10 h-1 bg-white/20 rounded-full" />
          </div>

          {/* Options */}
          <div className="px-4 pb-4 space-y-1">
            {/* Other options (dimmed) */}
            <div className="flex items-center gap-4 p-3 rounded-xl opacity-30">
              <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-sm">📋</div>
              <span className="text-sm text-white">Kopyala</span>
            </div>
            
            {/* Highlighted: Add to Home Screen */}
            <motion.div
              animate={{
                scale: [1, 1.02, 1],
                backgroundColor: ['rgba(25, 233, 139, 0.1)', 'rgba(25, 233, 139, 0.15)', 'rgba(25, 233, 139, 0.1)'],
              }}
              transition={{ duration: 2, repeat: Infinity }}
              className="flex items-center gap-4 p-3 rounded-xl border-2 border-[#19E98B]/30 relative"
            >
              <div className="w-10 h-10 rounded-xl bg-[#19E98B]/20 flex items-center justify-center text-lg flex-shrink-0">
                ➕
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-white">Ana Ekrana Ekle</p>
                <p className="text-xs text-white/50">BetSmart'ı yükle</p>
              </div>
              
              {/* Pulsing indicator */}
              <motion.div
                animate={{ scale: [1, 1.3, 1], opacity: [1, 0.5, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute -right-2 -top-2 w-4 h-4 bg-[#19E98B] rounded-full shadow-lg shadow-[#19E98B]/50"
              />
            </motion.div>

            {/* Other options (dimmed) */}
            <div className="flex items-center gap-4 p-3 rounded-xl opacity-30">
              <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-sm">🔖</div>
              <span className="text-sm text-white">Yer İmi Ekle</span>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Action Buttons */}
      <div className="space-y-3">
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={onClose}
          className="w-full py-4 rounded-2xl bg-gradient-to-r from-[#19E98B] to-[#0FA760] text-white font-semibold text-sm shadow-lg"
        >
          Anladım, Şimdi Ekle
        </motion.button>
        
        <button
          onClick={onClose}
          className="w-full py-2 text-sm text-white/50 hover:text-white/70 transition-colors"
        >
          Şimdi Değil
        </button>
      </div>
    </motion.div>
  );
}

// STEP 04: COMPLETE (Optional success message)
function CompleteStep({ onClose, prefersReducedMotion }: { onClose: () => void; prefersReducedMotion: boolean }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ duration: prefersReducedMotion ? 0 : 0.5 }}
      className="space-y-8 text-center py-8"
    >
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 0.2, type: 'spring', damping: 15 }}
      >
        <div className="w-20 h-20 rounded-full bg-gradient-to-br from-[#19E98B] to-[#0FA760] flex items-center justify-center mx-auto mb-6 shadow-2xl shadow-[#19E98B]/30">
          <span className="text-4xl">🎉</span>
        </div>
      </motion.div>

      <div className="space-y-3">
        <h3 className="text-2xl font-bold text-white">Harika!</h3>
        <p className="text-sm text-white/60 max-w-xs mx-auto">
          Artık BetSmart'ı ana ekranınızdan açabilir, tam ekran deneyimin keyfini çıkarabilirsiniz.
        </p>
      </div>

      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={onClose}
        className="w-full py-4 rounded-2xl bg-gradient-to-r from-[#19E98B] to-[#0FA760] text-white font-semibold text-sm shadow-lg"
      >
        Başlayalım
      </motion.button>
    </motion.div>
  );
}

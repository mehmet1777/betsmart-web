'use client';

import { useState, useEffect } from 'react';
import { X, Lock, Eye, EyeOff } from 'lucide-react';

export default function SkorTahminiPage() {
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const ADMIN_PASSWORD = 'Bet17'; // Şifre buradan değiştirilebilir

  // Authentication kontrolü (sadece client-side)
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const authTime = localStorage.getItem('skorTahminiAuth');
      if (authTime) {
        const timePassed = Date.now() - parseInt(authTime);
        const oneDayInMs = 24 * 60 * 60 * 1000;
        
        if (timePassed < oneDayInMs) {
          setIsAuthenticated(true);
        } else {
          localStorage.removeItem('skorTahminiAuth');
        }
      }
    }
    setIsLoading(false);
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (password === ADMIN_PASSWORD) {
      setIsAuthenticated(true);
      setError('');
      // localStorage'a kaydet (1 gün geçerli)
      if (typeof window !== 'undefined') {
        localStorage.setItem('skorTahminiAuth', Date.now().toString());
      }
    } else {
      setError('Hatalı şifre! Lütfen tekrar deneyin.');
      setPassword('');
    }
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen bg-bg-app flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block w-8 h-8 border-4 border-[#8B5CF6] border-t-transparent rounded-full animate-spin"></div>
        </div>
      </div>
    );
  }

  if (isAuthenticated) {
    // Mock data - gerçek veriler API'den gelecek
    const totalMatches = 100;
    const matchesWithDetails = 60;
    const predictedMatches = 15;
    const completionPercentage = Math.round((matchesWithDetails / totalMatches) * 100);
    
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#1a0f2e] via-[#1f1333] to-[#2a1a4a] relative overflow-hidden">
        {/* Purple Gradient Overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-transparent to-purple-900/20"></div>

        {/* Content Container */}
        <div className="relative z-10 max-w-md mx-auto px-4 py-6">
          
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            {/* Logo */}
            <div className="flex items-center gap-3">
              <div className="w-14 h-14 bg-gradient-to-br from-purple-500 to-purple-700 rounded-2xl flex items-center justify-center shadow-lg shadow-purple-500/50">
                <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2.5}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h1 className="text-2xl font-bold">
                <span className="text-white">Skor</span>
                <span className="text-purple-400">Tahmin</span>
              </h1>
            </div>

            {/* Premium Badge */}
            <div className="flex items-center gap-2 px-4 py-2 rounded-full border border-yellow-600/40 bg-gradient-to-r from-yellow-600/10 to-orange-600/10 backdrop-blur-sm">
              <span className="text-lg">👑</span>
              <div className="text-sm">
                <div className="text-yellow-500 font-semibold leading-tight">Premium</div>
                <div className="text-yellow-600 text-xs leading-tight">Erişim</div>
              </div>
            </div>
          </div>

          {/* Status Info Box */}
          <div className="mb-6 p-4 bg-gradient-to-br from-purple-900/40 to-purple-800/20 backdrop-blur-sm border border-purple-700/30 rounded-2xl">
            <div className="flex items-start gap-3 mb-4">
              <div className="w-10 h-10 bg-purple-600/30 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg className="w-6 h-6 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="text-white font-semibold mb-1">Analiz Durumu</h3>
                <p className="text-purple-200 text-sm leading-relaxed">
                  Bugünkü bültende <span className="font-bold text-white">{totalMatches} maç</span> var. 
                  Şu an <span className="font-bold text-purple-300">{matchesWithDetails} maçın</span> detaylı istatistikleri mevcut.
                </p>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="mb-3">
              <div className="flex items-center justify-between text-sm mb-2">
                <span className="text-purple-300">İstatistik Yüklemesi</span>
                <span className="text-purple-400 font-bold">%{completionPercentage}</span>
              </div>
              <div className="h-2 bg-purple-950/50 rounded-full overflow-hidden">
                <div 
                  className="h-full bg-gradient-to-r from-purple-500 to-purple-600 rounded-full transition-all duration-500"
                  style={{ width: `${completionPercentage}%` }}
                ></div>
              </div>
            </div>

            {/* Result Count */}
            <div className="p-3 bg-purple-600/20 border border-purple-600/30 rounded-xl">
              <div className="flex items-center justify-between">
                <span className="text-purple-200 text-sm">Bulunan Tahmin:</span>
                <span className="text-purple-300 font-bold text-lg">{predictedMatches} maç</span>
              </div>
            </div>

            {/* Info Text */}
            <div className="mt-3 flex items-start gap-2">
              <div className="text-lg flex-shrink-0">⏱️</div>
              <p className="text-purple-300 text-xs leading-relaxed">
                Her 10 dakikada bir yeni istatistikler ekleniyor. 
                <span className="text-purple-200 font-semibold"> ~1 saat içinde</span> tüm maç detayları yüklenecek ve daha fazla skor tahmini göreceksiniz.
              </p>
            </div>
          </div>

          {/* Matches List */}
          <div className="space-y-3">
            
            {/* Match Card 1 */}
            <div className="bg-gradient-to-br from-[#2a1f3f]/80 to-[#1f1833]/80 backdrop-blur-sm border border-purple-900/30 rounded-2xl p-4 hover:border-purple-700/50 transition-all cursor-pointer">
              <div className="flex items-center gap-4">
                {/* Time */}
                <div className="flex flex-col items-start min-w-[70px]">
                  <span className="text-white text-xl font-bold">16:00</span>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <span className="text-purple-300 text-xs">Bugün</span>
                    <div className="w-1.5 h-1.5 rounded-full bg-purple-500"></div>
                  </div>
                </div>

                {/* Teams */}
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  {/* Home Logo */}
                  <div className="w-10 h-10 rounded-full bg-purple-900/30 border border-purple-700/30 flex items-center justify-center flex-shrink-0">
                    <span className="text-xl">⚽</span>
                  </div>

                  {/* Team Names */}
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    <span className="text-white font-medium text-sm truncate">Galatasaray</span>
                    <span className="text-purple-400 text-xs font-semibold flex-shrink-0">VS</span>
                    <span className="text-white font-medium text-sm truncate">Fenerbahçe</span>
                  </div>
                </div>

                {/* Probability Badge */}
                <div className="flex flex-col items-end flex-shrink-0">
                  <div className="px-3 py-1 bg-green-500/20 border border-green-500/40 rounded-lg">
                    <span className="text-green-400 font-bold text-sm">%85</span>
                  </div>
                  <span className="text-purple-300 text-xs mt-1">2-1 / 1-2</span>
                </div>
              </div>
            </div>

            {/* Match Card 2 */}
            <div className="bg-gradient-to-br from-[#2a1f3f]/80 to-[#1f1833]/80 backdrop-blur-sm border border-purple-900/30 rounded-2xl p-4 hover:border-purple-700/50 transition-all cursor-pointer">
              <div className="flex items-center gap-4">
                <div className="flex flex-col items-start min-w-[70px]">
                  <span className="text-white text-xl font-bold">19:00</span>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <span className="text-purple-300 text-xs">Bugün</span>
                    <div className="w-1.5 h-1.5 rounded-full bg-purple-500"></div>
                  </div>
                </div>
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <div className="w-10 h-10 rounded-full bg-purple-900/30 border border-purple-700/30 flex items-center justify-center flex-shrink-0">
                    <span className="text-xl">⚽</span>
                  </div>
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    <span className="text-white font-medium text-sm truncate">Beşiktaş</span>
                    <span className="text-purple-400 text-xs font-semibold flex-shrink-0">VS</span>
                    <span className="text-white font-medium text-sm truncate">Trabzonspor</span>
                  </div>
                </div>
                <div className="flex flex-col items-end flex-shrink-0">
                  <div className="px-3 py-1 bg-yellow-500/20 border border-yellow-500/40 rounded-lg">
                    <span className="text-yellow-400 font-bold text-sm">%78</span>
                  </div>
                  <span className="text-purple-300 text-xs mt-1">2-1 / 1-2</span>
                </div>
              </div>
            </div>

            {/* Match Card 3 */}
            <div className="bg-gradient-to-br from-[#2a1f3f]/80 to-[#1f1833]/80 backdrop-blur-sm border border-purple-900/30 rounded-2xl p-4 hover:border-purple-700/50 transition-all cursor-pointer">
              <div className="flex items-center gap-4">
                <div className="flex flex-col items-start min-w-[70px]">
                  <span className="text-white text-xl font-bold">21:45</span>
                  <div className="flex items-center gap-1.5 mt-0.5">
                    <span className="text-purple-300 text-xs">Bugün</span>
                    <div className="w-1.5 h-1.5 rounded-full bg-purple-500"></div>
                  </div>
                </div>
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <div className="w-10 h-10 rounded-full bg-purple-900/30 border border-purple-700/30 flex items-center justify-center flex-shrink-0">
                    <span className="text-xl">⚽</span>
                  </div>
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    <span className="text-white font-medium text-sm truncate">Real Madrid</span>
                    <span className="text-purple-400 text-xs font-semibold flex-shrink-0">VS</span>
                    <span className="text-white font-medium text-sm truncate">Barcelona</span>
                  </div>
                </div>
                <div className="flex flex-col items-end flex-shrink-0">
                  <div className="px-3 py-1 bg-green-500/20 border border-green-500/40 rounded-lg">
                    <span className="text-green-400 font-bold text-sm">%92</span>
                  </div>
                  <span className="text-purple-300 text-xs mt-1">2-1 / 1-2</span>
                </div>
              </div>
            </div>

          </div>

          {/* Footer Message */}
          <div className="text-center mt-8 mb-6">
            <div className="inline-flex flex-col items-center gap-3 p-4 bg-purple-900/20 backdrop-blur-sm border border-purple-700/20 rounded-2xl">
              <div className="w-14 h-14 rounded-full bg-purple-600/20 border border-purple-600/30 flex items-center justify-center">
                <span className="text-3xl">📊</span>
              </div>
              <p className="text-purple-300 text-sm max-w-xs">
                İstatistikler yüklendikçe bu liste otomatik güncellenecek
              </p>
            </div>
          </div>

        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f] relative overflow-hidden flex items-center justify-center p-4">
      {/* Purple Gradient Blobs */}
      <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-purple-600/30 rounded-full blur-[150px] -translate-x-1/2 -translate-y-1/2"></div>
      <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-purple-600/30 rounded-full blur-[150px] translate-x-1/2 translate-y-1/2"></div>

      {/* Premium Auth Modal */}
      <div className="w-full max-w-md relative z-10">
        <div className="text-center space-y-8">
          
          {/* Premium Badge - Top */}
          <div className="inline-flex items-center gap-2 px-6 py-3 rounded-full border border-gray-800/50 bg-black/40 backdrop-blur-sm">
            <span className="text-2xl">👑</span>
            <span className="text-gray-400 text-sm font-medium">
              Premium Özellik - Beta Erişimi
            </span>
          </div>

          {/* Lock Icon with Orbital Ring */}
          <div className="relative inline-block my-12">
            {/* Orbital Ring */}
            <svg className="absolute inset-0 w-full h-full -m-8" viewBox="0 0 200 200">
              <ellipse
                cx="100"
                cy="100"
                rx="80"
                ry="30"
                fill="none"
                stroke="url(#gradient)"
                strokeWidth="2"
                opacity="0.6"
                className="animate-spin-slow"
                style={{ animationDuration: '8s' }}
              />
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#8B5CF6" stopOpacity="0" />
                  <stop offset="50%" stopColor="#8B5CF6" stopOpacity="1" />
                  <stop offset="100%" stopColor="#8B5CF6" stopOpacity="0" />
                </linearGradient>
              </defs>
            </svg>

            {/* Lock with Glow */}
            <div className="relative">
              <div className="absolute inset-0 bg-purple-600 rounded-3xl blur-3xl opacity-60 animate-pulse"></div>
              <div className="relative w-32 h-32 rounded-3xl bg-gradient-to-br from-purple-500 via-purple-600 to-purple-700 flex items-center justify-center shadow-2xl">
                {/* Lock SVG */}
                <svg className="w-16 h-16 text-white/90" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <rect x="5" y="11" width="14" height="10" rx="2" ry="2" />
                  <circle cx="12" cy="16" r="1" fill="currentColor" />
                  <path d="M12 17 L12 19" strokeLinecap="round" />
                  <path d="M8 11V7a4 4 0 0 1 8 0v4" />
                </svg>
              </div>
            </div>
          </div>

          {/* Title */}
          <div className="space-y-3">
            <h1 className="text-5xl font-bold">
              <span className="text-white">Skor </span>
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-purple-600">
                Tahmini
              </span>
            </h1>
            <p className="text-gray-400 text-base">
              Bu özelliğe erişim için<br />
              lütfen giriş yapın.
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4 mt-8">
            {/* Password Input */}
            <div className="relative">
              <div className="absolute left-5 top-1/2 -translate-y-1/2 text-gray-500">
                <Lock className="w-5 h-5" />
              </div>
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  setError('');
                }}
                placeholder="Şifrenizi girin"
                className="w-full pl-14 pr-14 py-5 bg-[#1a1a24]/80 backdrop-blur-sm border border-gray-800/50 rounded-2xl text-white placeholder-gray-500 focus:outline-none focus:border-purple-500/50 transition-all text-base"
                autoFocus
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-5 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300 transition-colors"
              >
                {showPassword ? (
                  <EyeOff className="w-5 h-5" />
                ) : (
                  <Eye className="w-5 h-5" />
                )}
              </button>
            </div>

            {/* Error Message */}
            {error && (
              <div className="text-red-400 text-sm text-center bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-3">
                {error}
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              className="w-full py-5 bg-gradient-to-r from-purple-600 via-purple-500 to-purple-600 hover:from-purple-500 hover:via-purple-600 hover:to-purple-500 text-white font-semibold rounded-2xl transition-all duration-300 shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50 flex items-center justify-center gap-2 text-base group"
            >
              Giriş Yap
              <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </button>
          </form>

          {/* Divider */}
          <div className="flex items-center justify-center my-6">
            <div className="text-purple-500 text-2xl">✦</div>
          </div>

          {/* Footer Info */}
          <div className="inline-flex items-center gap-3 px-6 py-4 bg-black/40 backdrop-blur-sm border border-gray-800/50 rounded-2xl">
            <span className="text-2xl">💡</span>
            <span className="text-gray-400 text-sm">
              Yakında tüm kullanıcılara açılacak!
            </span>
          </div>
        </div>
      </div>

      {/* Custom Animations */}
      <style jsx>{`
        @keyframes spin-slow {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }
        .animate-spin-slow {
          animation: spin-slow 8s linear infinite;
        }
      `}</style>
    </div>
  );
}

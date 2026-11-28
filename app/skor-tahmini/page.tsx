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
    return (
      <div className="min-h-screen bg-bg-app pt-20 pb-24 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="bg-bg-secondary border border-border-color rounded-2xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-2xl font-bold text-white">🎯 Skor Tahmini</h1>
              <div className="px-3 py-1 rounded-full bg-gradient-to-r from-[#FFD700] to-[#FFA500] text-black text-xs font-bold">
                BETA
              </div>
            </div>
            
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🚧</div>
              <h2 className="text-xl font-semibold text-white mb-2">
                Özellik Geliştiriliyor
              </h2>
              <p className="text-text-secondary">
                Skor tahmini özellikleri yakında burada olacak!
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

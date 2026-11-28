'use client';

import { useState, useEffect } from 'react';
import { X, Lock, Eye, EyeOff } from 'lucide-react';

export default function SkorTahminiPage() {
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const ADMIN_PASSWORD = 'betsmart2024'; // Şifre buradan değiştirilebilir

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
    <div className="min-h-screen bg-gradient-to-br from-[#0F1419] via-[#1a1f27] to-[#0F1419] flex items-center justify-center p-4">
      {/* Animated Background Circles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse delay-700"></div>
      </div>

      {/* Premium Auth Modal */}
      <div className="w-full max-w-md relative z-10">
        <div className="bg-gradient-to-br from-[#1e2530] to-[#151921] border border-[#2a3142] rounded-3xl p-8 shadow-2xl backdrop-blur-xl">
          
          {/* Lock Icon with Glow */}
          <div className="text-center mb-6">
            <div className="relative inline-block mb-6">
              <div className="absolute inset-0 bg-gradient-to-br from-[#8B5CF6] to-[#6366F1] rounded-full blur-2xl opacity-50 animate-pulse"></div>
              <div className="relative w-24 h-24 rounded-full bg-gradient-to-br from-[#8B5CF6] to-[#6366F1] flex items-center justify-center shadow-xl">
                <Lock className="w-12 h-12 text-white" strokeWidth={2.5} />
              </div>
            </div>
            
            {/* Premium Badge */}
            <div className="inline-flex items-center gap-2 px-6 py-2 rounded-full bg-gradient-to-r from-[#FFD700] via-[#FFA500] to-[#FFD700] text-black text-sm font-bold mb-6 shadow-lg shadow-yellow-500/30 animate-shimmer bg-[length:200%_100%]">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              Premium Özellik - Beta Erişimi
            </div>

            <h2 className="text-3xl font-bold text-white mb-3 tracking-tight">
              Skor Tahmini
            </h2>
            
            <div className="space-y-1 text-sm text-gray-400">
              <p className="font-medium">Bu özellik henüz test aşamasında!</p>
              <p>Şu an sadece yöneticilere açık.</p>
            </div>
          </div>

          {/* Divider */}
          <div className="h-px bg-gradient-to-r from-transparent via-gray-700 to-transparent mb-6"></div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-300 mb-3">
                Yönetici şifresi ile devam et
              </label>
              
              <div className="relative group">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    setError('');
                  }}
                  placeholder="Şifrenizi girin"
                  className="w-full px-5 py-4 bg-[#0F1419] border-2 border-[#2a3142] group-hover:border-[#8B5CF6]/50 focus:border-[#8B5CF6] rounded-2xl text-white placeholder-gray-500 focus:outline-none transition-all duration-300 pr-14 text-base"
                  autoFocus
                />
                
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 p-2 text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-white/5"
                >
                  {showPassword ? (
                    <EyeOff className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </button>
              </div>

              {error && (
                <div className="mt-3 flex items-center gap-2 text-red-400 text-sm bg-red-500/10 border border-red-500/20 rounded-xl px-4 py-2.5">
                  <X className="w-4 h-4 flex-shrink-0" />
                  <span>{error}</span>
                </div>
              )}
            </div>

            <button
              type="submit"
              className="w-full py-4 bg-gradient-to-r from-[#8B5CF6] via-[#7C3AED] to-[#6366F1] hover:from-[#7C3AED] hover:via-[#6D28D9] hover:to-[#5B21B6] text-white font-bold rounded-2xl transition-all duration-300 shadow-xl shadow-purple-500/30 hover:shadow-purple-500/50 hover:scale-[1.02] active:scale-[0.98] text-base"
            >
              Giriş Yap
            </button>
          </form>

          {/* Footer Info */}
          <div className="mt-6 p-4 bg-gradient-to-r from-[#8B5CF6]/5 to-[#6366F1]/5 border border-[#8B5CF6]/20 rounded-2xl">
            <div className="flex items-start gap-3">
              <div className="text-2xl">💡</div>
              <div className="flex-1">
                <p className="text-sm text-gray-400 leading-relaxed">
                  Yakında tüm kullanıcılara açılacak!
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Shimmer Animation */}
      <style jsx>{`
        @keyframes shimmer {
          0% { background-position: 200% 0; }
          100% { background-position: -200% 0; }
        }
        .animate-shimmer {
          animation: shimmer 3s linear infinite;
        }
      `}</style>
    </div>
  );
}

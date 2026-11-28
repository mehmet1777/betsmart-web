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
    <div className="min-h-screen bg-bg-app flex items-center justify-center p-4">
      {/* Premium Auth Modal */}
      <div className="w-full max-w-md">
        <div className="bg-gradient-to-br from-[#1a1f27] to-[#0F1419] border border-[#8B5CF6]/30 rounded-3xl p-6 shadow-2xl shadow-purple-500/20">
          
          {/* Header */}
          <div className="text-center mb-6">
            <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-[#8B5CF6] to-[#6366F1] mb-4 shadow-lg shadow-purple-500/30">
              <Lock className="w-10 h-10 text-white" />
            </div>
            
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-gradient-to-r from-[#FFD700] to-[#FFA500] text-black text-sm font-bold mb-4">
              <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              Premium Özellik - Beta Erişimi
            </div>

            <h2 className="text-2xl font-bold text-white mb-2">
              Skor Tahmini
            </h2>
            
            <div className="space-y-2 text-sm text-text-secondary">
              <p>Bu özellik henüz test aşamasında!</p>
              <p>Şu an sadece yöneticilere açık.</p>
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-text-secondary mb-2">
                Yönetici şifresi ile devam et
              </label>
              
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => {
                    setPassword(e.target.value);
                    setError('');
                  }}
                  placeholder="Şifrenizi girin"
                  className="w-full px-4 py-3 bg-bg-app border border-border-color rounded-xl text-white placeholder-text-secondary focus:outline-none focus:border-[#8B5CF6] transition-colors pr-12"
                  autoFocus
                />
                
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 p-1 text-text-secondary hover:text-white transition-colors"
                >
                  {showPassword ? (
                    <EyeOff className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </button>
              </div>

              {error && (
                <div className="mt-2 flex items-center gap-2 text-red-400 text-sm">
                  <X className="w-4 h-4" />
                  {error}
                </div>
              )}
            </div>

            <button
              type="submit"
              className="w-full py-3 bg-gradient-to-r from-[#8B5CF6] to-[#6366F1] hover:from-[#7C3AED] hover:to-[#5B21B6] text-white font-semibold rounded-xl transition-all shadow-lg shadow-purple-500/30 hover:shadow-purple-500/50"
            >
              Giriş Yap
            </button>
          </form>

          {/* Footer Info */}
          <div className="mt-6 p-4 bg-[#8B5CF6]/10 border border-[#8B5CF6]/20 rounded-xl">
            <div className="flex items-start gap-3">
              <div className="text-2xl">💡</div>
              <div className="flex-1">
                <p className="text-xs text-text-secondary">
                  Yakında tüm kullanıcılara açılacak!
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

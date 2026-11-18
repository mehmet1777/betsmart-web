'use client';

import { useEffect } from 'react';
import { CheckCircle2, X } from 'lucide-react';

interface ToastProps {
  show: boolean;
  onClose: () => void;
  title: string;
  message: string;
  type?: 'success' | 'error' | 'info';
  duration?: number;
}

export default function Toast({ show, onClose, title, message, type = 'success', duration = 4000 }: ToastProps) {
  useEffect(() => {
    if (show && duration > 0) {
      const timer = setTimeout(() => {
        onClose();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [show, duration, onClose]);

  if (!show) return null;

  const colors = {
    success: {
      bg: 'from-[#19E98B]/20 to-[#19E98B]/5',
      border: 'border-[#19E98B]/40',
      icon: 'text-[#19E98B]',
      iconBg: 'bg-[#19E98B]/20',
      text: 'text-[#19E98B]'
    },
    error: {
      bg: 'from-red-500/20 to-red-500/5',
      border: 'border-red-500/40',
      icon: 'text-red-500',
      iconBg: 'bg-red-500/20',
      text: 'text-red-500'
    },
    info: {
      bg: 'from-blue-500/20 to-blue-500/5',
      border: 'border-blue-500/40',
      icon: 'text-blue-500',
      iconBg: 'bg-blue-500/20',
      text: 'text-blue-500'
    }
  };

  const color = colors[type];

  return (
    <>
      {/* Backdrop - Subtle */}
      <div 
        className="fixed inset-0 bg-black/60 z-[100] backdrop-blur-sm animate-fadeIn"
        onClick={onClose}
      />

      {/* Toast Card - Center */}
      <div className="fixed inset-0 z-[101] flex items-center justify-center p-4 pointer-events-none">
        <div className={`
          pointer-events-auto
          w-full max-w-sm
          bg-gradient-to-br ${color.bg}
          backdrop-blur-xl
          border ${color.border}
          rounded-2xl
          shadow-2xl
          animate-slideUp
          overflow-hidden
        `}>
          {/* Glow Effect */}
          <div className={`absolute inset-0 bg-gradient-to-br ${color.bg} opacity-50 blur-xl pointer-events-none`}></div>
          
          {/* Content */}
          <div className="relative p-5">
            {/* Close Button */}
            <button
              onClick={onClose}
              className="absolute top-3 right-3 w-8 h-8 rounded-lg bg-white/5 hover:bg-white/10 transition-colors flex items-center justify-center"
            >
              <X className="w-4 h-4 text-white" />
            </button>

            {/* Icon + Title */}
            <div className="flex items-center gap-3 mb-3">
              <div className={`w-12 h-12 rounded-xl ${color.iconBg} flex items-center justify-center flex-shrink-0`}>
                <CheckCircle2 className={`w-7 h-7 ${color.icon}`} strokeWidth={2.5} />
              </div>
              <h3 className="text-lg font-black text-white pr-8">{title}</h3>
            </div>

            {/* Message - Formatted */}
            <div className="ml-15 space-y-1.5 pl-1">
              {message.split('\n').map((line, index) => {
                if (!line.trim()) return null;
                
                // Parse emoji + text format
                const match = line.match(/^(🎫|💰|🏆)\s*(.+)$/);
                if (match) {
                  const [, emoji, text] = match;
                  return (
                    <div key={index} className="flex items-center gap-2">
                      <span className="text-xl">{emoji}</span>
                      <span className="text-sm font-semibold text-gray-300">{text}</span>
                    </div>
                  );
                }
                
                return (
                  <p key={index} className="text-sm font-semibold text-gray-300">
                    {line}
                  </p>
                );
              })}
            </div>

            {/* Progress Bar */}
            <div className="mt-4 h-1 bg-white/10 rounded-full overflow-hidden">
              <div 
                className={`h-full bg-gradient-to-r ${color.bg} animate-shrink`}
                style={{ animationDuration: `${duration}ms` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }
        
        @keyframes shrink {
          from { width: 100%; }
          to { width: 0%; }
        }
        
        .animate-fadeIn {
          animation: fadeIn 0.2s ease-out;
        }
        
        .animate-slideUp {
          animation: slideUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }
        
        .animate-shrink {
          animation: shrink linear;
        }
      `}</style>
    </>
  );
}

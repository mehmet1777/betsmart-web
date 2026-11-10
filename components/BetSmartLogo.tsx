'use client';

interface BetSmartLogoProps {
  variant?: 'full' | 'icon';
  className?: string;
}

export default function BetSmartLogo({ variant = 'full', className = '' }: BetSmartLogoProps) {
  if (variant === 'icon') {
    return (
      <svg
        viewBox="0 0 64 64"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={className}
      >
        <defs>
          <linearGradient id="iconGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#19E98B" />
            <stop offset="40%" stopColor="#14C975" />
            <stop offset="100%" stopColor="#0FA760" />
          </linearGradient>
        </defs>
        
        {/* Modern Shield/Badge Shape */}
        <path
          d="M32 4 L54 12 L54 32 C54 45 45 56 32 60 C19 56 10 45 10 32 L10 12 Z"
          fill="url(#iconGrad)"
        />
        
        {/* Bold Modern B */}
        <path
          d="M22 18 L22 46 L35 46 C40 46 44 42 44 37 C44 34.5 42.5 32.5 40.5 31.5 C42.5 30.5 44 28.5 44 26 C44 21 40 18 35 18 Z M27 23 L34 23 C36.5 23 38.5 25 38.5 27 C38.5 29 36.5 31 34 31 L27 31 Z M27 35 L35 35 C37.5 35 39.5 37 39.5 39 C39.5 41 37.5 43 35 43 L27 43 Z"
          fill="white"
        />
      </svg>
    );
  }

  return (
    <div className={`flex items-center gap-2.5 ${className}`}>
      {/* Icon Badge */}
      <svg
        viewBox="0 0 64 64"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="h-full w-auto"
        style={{ filter: 'drop-shadow(0 2px 8px rgba(25, 233, 139, 0.3))' }}
      >
        <defs>
          <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#19E98B" />
            <stop offset="40%" stopColor="#14C975" />
            <stop offset="100%" stopColor="#0FA760" />
          </linearGradient>
        </defs>
        
        {/* Shield Shape */}
        <path
          d="M32 4 L54 12 L54 32 C54 45 45 56 32 60 C19 56 10 45 10 32 L10 12 Z"
          fill="url(#logoGrad)"
        />
        
        {/* B Letter */}
        <path
          d="M22 18 L22 46 L35 46 C40 46 44 42 44 37 C44 34.5 42.5 32.5 40.5 31.5 C42.5 30.5 44 28.5 44 26 C44 21 40 18 35 18 Z M27 23 L34 23 C36.5 23 38.5 25 38.5 27 C38.5 29 36.5 31 34 31 L27 31 Z M27 35 L35 35 C37.5 35 39.5 37 39.5 39 C39.5 41 37.5 43 35 43 L27 43 Z"
          fill="white"
        />
      </svg>
      
      {/* Text - Ultra Modern */}
      <div className="flex items-baseline">
        <span className="font-black tracking-tighter leading-none" style={{ 
          fontFamily: 'Inter, sans-serif',
          fontSize: '1.75em',
          color: '#FFFFFF',
          letterSpacing: '-0.05em'
        }}>
          Bet
        </span>
        <span className="font-black tracking-tighter leading-none" style={{ 
          fontFamily: 'Inter, sans-serif',
          fontSize: '1.75em',
          color: '#19E98B',
          letterSpacing: '-0.05em'
        }}>
          Smart
        </span>
      </div>
    </div>
  );
}

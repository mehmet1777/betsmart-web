import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        'bg-app': '#090D14',
        'bg-card': '#171E29',
        'bg-elevated': '#1F2732',
        'border-color': '#293241',
        'accent-primary': '#19E98B',
        'accent-hover': '#14C975',
        'accent-dark': '#0FA760',
        'text-primary': '#FFFFFF',
        'text-secondary': '#9CA3AF',
        'text-muted': '#6B7280',
        // Premium kupon renkleri
        'premium-bg': '#050806',
        'premium-card': '#0A100D',
        'premium-card-secondary': '#111915',
        'premium-neon': '#00E676',
        'premium-neon-light': '#65FF9A',
        'premium-text': '#F5F7F5',
        'premium-text-secondary': '#9AA69F',
        'premium-border': 'rgba(0, 230, 118, 0.25)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
export default config;

import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        cold: {
          black: '#080808',
          dark: '#0f0f0f',
          charcoal: '#1a1a1a',
          green: '#00ff41',
          'green-dim': '#00cc33',
          'green-glow': 'rgba(0,255,65,0.15)',
          gray: '#2a2a2a',
          'gray-light': '#4a4a4a',
          smoke: '#888888',
          white: '#e8e8e8',
          red: '#ff2222',
          gold: '#c9a84c',
        },
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'Courier New', 'monospace'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      animation: {
        flicker: 'flicker 3s infinite',
        fog: 'fog 8s ease-in-out infinite',
        'pulse-green': 'pulseGreen 2s ease-in-out infinite',
        'slide-up': 'slideUp 0.4s ease-out',
        'slide-in': 'slideIn 0.5s ease-out',
        glow: 'glow 2s ease-in-out infinite',
      },
      keyframes: {
        flicker: {
          '0%, 100%': { opacity: '1' },
          '41.99%': { opacity: '1' },
          '42%': { opacity: '0' },
          '43%': { opacity: '1' },
          '45%': { opacity: '0' },
          '46%': { opacity: '1' },
        },
        fog: {
          '0%, 100%': { transform: 'translateX(0) translateY(0)', opacity: '0.3' },
          '50%': { transform: 'translateX(20px) translateY(-10px)', opacity: '0.6' },
        },
        pulseGreen: {
          '0%, 100%': { boxShadow: '0 0 5px rgba(0,255,65,0.3)' },
          '50%': { boxShadow: '0 0 20px rgba(0,255,65,0.7), 0 0 40px rgba(0,255,65,0.3)' },
        },
        slideUp: {
          from: { transform: 'translateY(20px)', opacity: '0' },
          to: { transform: 'translateY(0)', opacity: '1' },
        },
        slideIn: {
          from: { transform: 'translateX(-30px)', opacity: '0' },
          to: { transform: 'translateX(0)', opacity: '1' },
        },
        glow: {
          '0%, 100%': { textShadow: '0 0 5px rgba(0,255,65,0.5)' },
          '50%': { textShadow: '0 0 20px rgba(0,255,65,1), 0 0 40px rgba(0,255,65,0.5)' },
        },
      },
      backgroundImage: {
        'noise': "url(\"data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.05'/%3E%3C/svg%3E\")",
      },
    },
  },
  plugins: [],
}

export default config

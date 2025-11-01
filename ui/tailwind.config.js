/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#0e0e10',
        surface: '#111827',
        neonPurple: '#9f7aea',
        neonCyan: '#06b6d4',
      },
      fontFamily: {
        sans: ['Inter', 'Poppins', 'Space Grotesk', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        glow: '0 0 20px rgba(159, 122, 234, 0.3)',
        cyanGlow: '0 0 20px rgba(6, 182, 212, 0.25)',
        card: '0 10px 30px rgba(0,0,0,0.35)',
      },
      backdropBlur: {
        xs: '2px',
      },
      backgroundImage: {
        'gradient-accent': 'linear-gradient(90deg, rgba(159,122,234,0.3), rgba(6,182,212,0.3))',
      },
    },
  },
  plugins: [],
}
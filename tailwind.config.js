/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./index.html'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['Sora', 'Inter', 'system-ui', 'sans-serif'],
      },
      colors: {
        primary: '#4F46E5',
        primaryDark: '#4338CA',
        dark: '#0B1220',
        darkLight: '#111A2E',
      },
      boxShadow: {
        lift: '0 20px 40px -12px rgba(79, 70, 229, 0.25)',
        card: '0 4px 16px rgba(15, 23, 42, 0.06)',
      },
      animation: {
        blob: 'blob 14s ease-in-out infinite',
        'float-slow': 'floatSlow 9s ease-in-out infinite',
        'marquee': 'marquee 20s linear infinite',
      },
      keyframes: {
        blob: {
          '0%, 100%': { transform: 'translate(0, 0) scale(1)' },
          '33%': { transform: 'translate(60px, -50px) scale(1.15)' },
          '66%': { transform: 'translate(-40px, 40px) scale(0.9)' },
        },
        floatSlow: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-16px)' },
        },
        marquee: {
          from: { transform: 'translateX(0)' },
          to: { transform: 'translateX(-50%)' },
        },
      },
    },
  },
  plugins: [],
};
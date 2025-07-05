/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        // MACHO-GPT Mode Colors
        'macho-prime': '#3b82f6',
        'macho-oracle': '#8b5cf6',
        'macho-zero': '#6b7280',
        'macho-lattice': '#10b981',
        'macho-rhythm': '#f59e0b',
        'macho-cost-guard': '#ef4444',
        // Samsung C&T Brand Colors
        'samsung-blue': '#1428a0',
        'samsung-navy': '#041e42',
        // Logistics Colors
        'logistics-green': '#059669',
        'logistics-orange': '#ea580c',
        'logistics-red': '#dc2626'
      },
      fontFamily: {
        'samsung': ['Samsung One', 'sans-serif'],
        'macho': ['Inter', 'system-ui', 'sans-serif']
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 2s infinite',
        'spin-slow': 'spin 3s linear infinite',
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'macho-glow': 'machoGlow 2s ease-in-out infinite alternate'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        slideUp: {
          '0%': { transform: 'translateY(100%)' },
          '100%': { transform: 'translateY(0)' }
        },
        machoGlow: {
          '0%': { boxShadow: '0 0 5px rgba(59, 130, 246, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgba(59, 130, 246, 0.8)' }
        }
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem'
      },
      borderRadius: {
        '4xl': '2rem'
      },
      backdropBlur: {
        xs: '2px'
      }
    }
  },
  plugins: [
    function({ addComponents }) {
      addComponents({
        '.macho-gpt-card': {
          '@apply bg-white rounded-lg shadow-lg p-6 border border-gray-200 hover:shadow-xl transition-shadow duration-300': {}
        },
        '.macho-gpt-button': {
          '@apply px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center justify-center': {}
        },
        '.macho-gpt-input': {
          '@apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent': {}
        },
        '.macho-gpt-badge': {
          '@apply inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium': {}
        }
      })
    }
  ]
} 
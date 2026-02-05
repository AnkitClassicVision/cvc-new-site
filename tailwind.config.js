/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.html", "./scripts/**/*.js", "!./node_modules/**", "!./dev/**"],
  theme: {
    extend: {
      colors: {
        "cvc-teal": {
          50: "rgba(26, 48, 40, 0.05)",
          100: "rgba(26, 48, 40, 0.1)",
          200: "rgba(26, 48, 40, 0.2)",
          300: "#2d4a3e",
          400: "#1a3028",
          500: "#1a3028",
          600: "#0f1f18",
          700: "#0f1f18",
          800: "#0a1510",
          900: "#050a08"
        },
        "cvc-gold": {
          light: "#e8d48a",
          DEFAULT: "#c9a227",
          dark: "#a68620"
        },
        "cvc-cream": "#f8f5f0",
        "cvc-charcoal": "#0f1f18"
      },
      fontFamily: {
        display: ["Fraunces", "Georgia", "serif"],
        body: ['"Instrument Sans"', "system-ui", "sans-serif"]
      }
    }
  },
  plugins: []
};

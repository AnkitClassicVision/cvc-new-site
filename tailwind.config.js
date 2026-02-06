/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.html", "./scripts/**/*.js", "!./node_modules/**", "!./dev/**"],
  theme: {
    extend: {
      colors: {
        "cvc-teal": {
          50: "rgba(17, 71, 85, 0.05)",
          100: "rgba(17, 71, 85, 0.1)",
          200: "rgba(17, 71, 85, 0.2)",
          300: "#2d4a3e",
          400: "#1a3028",
          500: "#114755",
          600: "#0d3640",
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

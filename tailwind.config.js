/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.html", "./scripts/**/*.js", "!./node_modules/**", "!./dev/**"],
  theme: {
    extend: {
      colors: {
        "cvc-teal": {
          50: "rgba(82, 199, 225, 0.05)",
          100: "rgba(82, 199, 225, 0.1)",
          200: "#52C7E1",
          300: "#3294A3",
          400: "#15737A",
          500: "#114755",
          600: "#0d3640",
          700: "#0a2e38",
          800: "#071f26",
          900: "#041114"
        },
        "cvc-gold": {
          light: "#7ED4E6",
          DEFAULT: "#52C7E1",
          dark: "#3294A3"
        },
        "cvc-cream": "#ffffff",
        "cvc-charcoal": "#1A1A1A"
      },
      fontFamily: {
        display: ['"TT Norms Pro"', "Helvetica Neue", "Arial", "sans-serif"],
        body: ["Montserrat", "system-ui", "sans-serif"]
      }
    }
  },
  plugins: []
};

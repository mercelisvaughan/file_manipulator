/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pdf_engine/templates/**/*.html', // Scans your current templates
    './**/templates/**/*.html',         // Scans future apps automatically
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
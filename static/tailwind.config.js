/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      '../viewer/templates/**/*.{html,js}',
      //'../another_app/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'custom-color-blue-grey': '#0F172A',
      },
      animation: {
        'blink': 'blink 1500ms infinite',
      },
      display: ['hover', 'focus']
    },
  },
  plugins: [],
}


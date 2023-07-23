/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      '../viewer/templates/**/*.{html,js}',
      //'../another_app/templates/**/*.html',
  ],
  theme: {
    extend: {
      animation: {
        'blink': 'blink 1500ms infinite',
      }
    },
  },
  plugins: [],
}


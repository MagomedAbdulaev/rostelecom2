/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.{html,js}",
  ],
  darkMode: 'class', // Включаем поддержку темной темы через классы
  theme: {
    extend: {
      colors: {
        primary: '#FF4F12', // Цвет Ростелекома
      },
    },
  },
  plugins: [],
}
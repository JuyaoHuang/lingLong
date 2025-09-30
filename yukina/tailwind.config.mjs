/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["selector", '[data-theme="dark"]'],
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
  theme: {
    extend: {
      colors:{
        'sakura-pink': '#FFB7C5',
      },

    },
  },
  plugins: [require("@tailwindcss/typography")],

};

/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                gamer: {
                    green: "#00C851",
                    dark: "#0F0F0F",
                    card: "#1A1A1A",
                    border: "#262626",
                }
            }
        },
    },
    plugins: [],
}

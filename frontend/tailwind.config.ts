import type { Config } from "tailwindcss";

const config: Config = {
    content: [
        "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
        "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                brand: {
                    50: "#f0f4ff",
                    100: "#e0eaff",
                    500: "#6e40c9",
                    600: "#5a32b0",
                    700: "#4a2890",
                    900: "#1e0f4a",
                },
            },
            animation: {
                "fade-in": "fadeIn 0.5s ease-in-out",
                "slide-up": "slideUp 0.3s ease-out",
                "pulse-slow": "pulse 3s infinite",
            },
            keyframes: {
                fadeIn: { "0%": { opacity: "0" }, "100%": { opacity: "1" } },
                slideUp: { "0%": { transform: "translateY(10px)", opacity: "0" }, "100%": { transform: "translateY(0)", opacity: "1" } },
            },
        },
    },
    plugins: [],
};

export default config;

import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        ukrainian: "#3b82f6",
        math: "#10b981",
        history: "#f59e0b",
        english: "#a855f7",
        glass: "rgba(255, 255, 255, 0.6)",
        glassBorder: "rgba(255, 255, 255, 0.8)",
      },
      backdropBlur: {
        glass: "12px",
      },
      boxShadow: {
        glass: "0 8px 32px 0 rgba(31, 38, 135, 0.12)",
        soft: "0 4px 20px rgba(0, 0, 0, 0.05)",
      },
    },
  },
  plugins: [],
};

export default config;

import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./lib/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: "#17202a",
        panel: "#f7f8fb",
        line: "#d9dee8",
      },
      boxShadow: {
        soft: "0 10px 30px rgba(31, 42, 68, 0.08)",
      },
    },
  },
  plugins: [],
};

export default config;

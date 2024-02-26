import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {},
  daisyui: {
    themes: [
      {
        sunset: {
          "color-scheme": "dark",
          primary: "#FF865B",
          secondary: "#FD6F9C",
          accent: "#B387FA",
          neutral: "oklch(26% 0.019 237.69)",
          "neutral-content": "oklch(70% 0.019 237.69)",
          "base-100": "oklch(20% 0.019 237.69)",
          "base-200": "oklch(18% 0.019 237.69)",
          "base-300": "oklch(16% 0.019 237.69)",
          "base-content": "#9fb9d0",
          info: "#89e0eb",
          success: "#addfad",
          warning: "#f1c891",
          error: "#ffbbbd",
          "--rounded-box": "1.2rem",
          "--rounded-btn": "0.8rem",
          "--rounded-badge": "0.4rem",
          "--tab-radius": "0.7rem",
        },
      },
    ],
  },
  plugins: [require("daisyui")],
};
export default config;

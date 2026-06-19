import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";

// Relative base so the built app works whether it's served from a domain root
// (Netlify/Vercel) or a sub-folder (GitHub Pages, a USB stick, etc.).
export default defineConfig({
  base: "./",
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      includeAssets: ["favicon.svg", "apple-touch-icon.png"],
      manifest: {
        name: "Bloom Beauty Suites",
        short_name: "Bloom",
        description: "Run your beauty business — clients, schedule, finances, and daily tasks.",
        theme_color: "#fbf4fc",
        background_color: "#fbf4fc",
        display: "standalone",
        orientation: "portrait",
        start_url: "./",
        scope: "./",
        icons: [
          { src: "icon-192.png", sizes: "192x192", type: "image/png" },
          { src: "icon-512.png", sizes: "512x512", type: "image/png" },
          { src: "icon-512.png", sizes: "512x512", type: "image/png", purpose: "maskable" },
        ],
      },
      workbox: {
        globPatterns: ["**/*.{js,css,html,svg,png,ico,woff2}"],
      },
    }),
  ],
});

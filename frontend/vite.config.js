import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
// eslint-disable-next-line no-undef
const apiTarget = process.env.VITE_API_TARGET || "http://localhost:8000";

export default defineConfig({
  plugins: [react()],
  server: {
    // Allow internal Docker Compose hostname used by e2e tests.
    allowedHosts: ["frontend"],
    // Proxy /api requests to the backend so the browser never needs
    // to know the real backend hostname (fixes Docker E2E routing).
    proxy: {
      "/api": {
        target: apiTarget,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});

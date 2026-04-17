import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Allow internal Docker Compose hostname used by e2e tests.
    allowedHosts: ["frontend"],
  },
});

import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import { fileURLToPath, URL } from "node:url";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
      "@test": fileURLToPath(new URL("./src/test", import.meta.url)),
    },
  },
  test: {
    environment: "jsdom",
    setupFiles: "./src/test/setup.js",
    coverage: {
      provider: "v8",
      reporter: ["text", "html"],
      include: ["src/**/*.{js,jsx}"],
      exclude: ["src/main.jsx"],
      thresholds: {
        lines: 85,
        branches: 76,
        functions: 70,
        statements: 85,
        // isDev captured at module load from import.meta.env.DEV — always true in
        // test env, so both false-branches of debug/info are structurally unreachable.
        "src/logger.js": { branches: 50 },
        "src/useApi.js": { branches: 100 },
        "src/components/NewFolderForm.jsx": { branches: 80 },
        "src/components/MainContent.jsx": { branches: 75 },
        // hover() branches inside useDrop are permanently mocked away (react-dnd unit
        // mock discards the options object). Drag-drop logic belongs in E2E tests.
        // isOpen branch unreachable: Shoelace sl-show events don't propagate via
        // React synthetic event system in jsdom.
        "src/components/TodoItem.jsx": { branches: 58 },
      },
    },
  },
});

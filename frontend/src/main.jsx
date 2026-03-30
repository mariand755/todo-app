import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { initTheme } from "./theme";
import "./index.css";
import App from "./App.jsx";

// Apply theme before first render to prevent flash of wrong theme
initTheme();

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>,
);

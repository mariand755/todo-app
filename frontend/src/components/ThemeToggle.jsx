import React, { useState, useEffect } from "react";
import SlIcon from "@shoelace-style/shoelace/dist/react/icon/index.js";
import { toggleTheme } from "../theme";

const ThemeToggle = () => {
  const [isDark, setIsDark] = useState(
    () => document.documentElement.getAttribute("data-theme") === "dark",
  );

  useEffect(() => {
    const observer = new MutationObserver(() => {
      setIsDark(document.documentElement.getAttribute("data-theme") === "dark");
    });
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["data-theme"],
    });
    return () => observer.disconnect();
  }, []);

  const handleToggle = () => {
    toggleTheme();
  };

  return (
    <button
      type="button"
      className="theme-toggle-btn"
      onClick={handleToggle}
      aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
      aria-pressed={isDark}
      title={isDark ? "Switch to light mode" : "Switch to dark mode"}
    >
      <SlIcon name={isDark ? "sun" : "moon"} />
    </button>
  );
};

export default ThemeToggle;

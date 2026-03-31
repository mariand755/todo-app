// Theme constants
const THEME_KEY = "theme";
const DARK = "dark";
const LIGHT = "light";
/** Read stored theme from localStorage (returns "light", "dark", or null) */
export function getStoredTheme() {
  try {
    const stored = localStorage.getItem(THEME_KEY);
    return stored === DARK || stored === LIGHT ? stored : null;
  } catch {
    return null;
  }
}
/** Detect OS/browser preference; default to "light" if unavailable */
export function getDefaultTheme() {
  try {
    if (window.matchMedia?.("(prefers-color-scheme: dark)").matches) {
      return DARK;
    }
  } catch {
    // matchMedia unavailable
  }
  return LIGHT;
}
/** Apply the given theme to the document */
export function applyTheme(theme) {
  const resolved = theme === DARK ? DARK : LIGHT;
  document.documentElement.setAttribute("data-theme", resolved);
  if (resolved === DARK) {
    document.documentElement.classList.add("sl-theme-dark");
  } else {
    document.documentElement.classList.remove("sl-theme-dark");
  }
}
/** Toggle between light and dark, persist, and apply */
export function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === DARK ? LIGHT : DARK;
  try {
    localStorage.setItem(THEME_KEY, next);
  } catch {
    // localStorage unavailable
  }
  applyTheme(next);
  return next;
}
/**
 * Boot-time initializer: resolve stored or default theme, apply it,
 * and set up a listener for OS-level theme changes.
 *
 * System-theme policy: if the user has an explicit stored choice, keep it.
 * If no stored choice, follow prefers-color-scheme (and listen for live changes).
 */
export function initTheme() {
  const theme = getStoredTheme() || getDefaultTheme();
  applyTheme(theme);
  try {
    const mql = window.matchMedia("(prefers-color-scheme: dark)");
    mql.addEventListener("change", (e) => {
      if (getStoredTheme() !== null) return;
      applyTheme(e.matches ? DARK : LIGHT);
    });
  } catch {
    // matchMedia listener unavailable
  }
}

import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import {
  getStoredTheme,
  getDefaultTheme,
  applyTheme,
  toggleTheme,
  initTheme,
} from "../../theme";

describe("theme module", () => {
  let originalGetItem;
  let originalSetItem;
  let originalMatchMedia;

  beforeEach(() => {
    document.documentElement.removeAttribute("data-theme");
    document.documentElement.classList.remove("sl-theme-dark");

    originalGetItem = Storage.prototype.getItem;
    originalSetItem = Storage.prototype.setItem;
    originalMatchMedia = window.matchMedia;
  });

  afterEach(() => {
    Storage.prototype.getItem = originalGetItem;
    Storage.prototype.setItem = originalSetItem;
    window.matchMedia = originalMatchMedia;
    localStorage.clear();
  });

  describe("getStoredTheme", () => {
    it("@FUT60 | returns null when no theme is stored", () => {
      localStorage.clear();
      expect(getStoredTheme()).toBeNull();
    });

    it("@FUT61 | returns 'dark' when dark is stored", () => {
      localStorage.setItem("theme", "dark");
      expect(getStoredTheme()).toBe("dark");
    });

    it("@FUT62 | returns 'light' when light is stored", () => {
      localStorage.setItem("theme", "light");
      expect(getStoredTheme()).toBe("light");
    });

    it("@FUT63 | returns null for invalid stored value", () => {
      localStorage.setItem("theme", "purple");
      expect(getStoredTheme()).toBeNull();
    });

    it("@FUT64 | returns null when localStorage throws", () => {
      Storage.prototype.getItem = () => {
        throw new Error("blocked");
      };
      expect(getStoredTheme()).toBeNull();
    });
  });

  describe("getDefaultTheme", () => {
    it("@FUT65 | returns 'dark' when prefers-color-scheme is dark", () => {
      window.matchMedia = vi.fn().mockReturnValue({ matches: true });
      expect(getDefaultTheme()).toBe("dark");
    });

    it("@FUT66 | returns 'light' when prefers-color-scheme is light", () => {
      window.matchMedia = vi.fn().mockReturnValue({ matches: false });
      expect(getDefaultTheme()).toBe("light");
    });

    it("@FUT67 | returns 'light' when matchMedia is unavailable", () => {
      window.matchMedia = undefined;
      expect(getDefaultTheme()).toBe("light");
    });
  });

  describe("applyTheme", () => {
    it("@FUT68 | sets data-theme=dark and adds sl-theme-dark class", () => {
      applyTheme("dark");
      expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
      expect(document.documentElement.classList.contains("sl-theme-dark")).toBe(
        true,
      );
    });

    it("@FUT69 | sets data-theme=light and removes sl-theme-dark class", () => {
      document.documentElement.classList.add("sl-theme-dark");
      applyTheme("light");
      expect(document.documentElement.getAttribute("data-theme")).toBe("light");
      expect(document.documentElement.classList.contains("sl-theme-dark")).toBe(
        false,
      );
    });

    it("@FUT70 | defaults to light for invalid theme value", () => {
      applyTheme("invalid");
      expect(document.documentElement.getAttribute("data-theme")).toBe("light");
      expect(document.documentElement.classList.contains("sl-theme-dark")).toBe(
        false,
      );
    });
  });

  describe("toggleTheme", () => {
    it("@FUT71 | toggles from light to dark", () => {
      applyTheme("light");
      const result = toggleTheme();
      expect(result).toBe("dark");
      expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
      expect(localStorage.getItem("theme")).toBe("dark");
    });

    it("@FUT72 | toggles from dark to light", () => {
      applyTheme("dark");
      const result = toggleTheme();
      expect(result).toBe("light");
      expect(document.documentElement.getAttribute("data-theme")).toBe("light");
      expect(localStorage.getItem("theme")).toBe("light");
    });

    it("@FUT73 | handles localStorage setItem failure gracefully", () => {
      applyTheme("light");
      Storage.prototype.setItem = () => {
        throw new Error("quota exceeded");
      };
      const result = toggleTheme();
      expect(result).toBe("dark");
      expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
    });
  });

  describe("initTheme", () => {
    it("@FUT74 | uses stored theme when available", () => {
      localStorage.setItem("theme", "dark");
      window.matchMedia = vi.fn().mockReturnValue({
        matches: false,
        addEventListener: vi.fn(),
      });
      initTheme();
      expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
    });

    it("@FUT75 | falls back to system preference when no stored theme", () => {
      localStorage.clear();
      window.matchMedia = vi.fn().mockReturnValue({
        matches: true,
        addEventListener: vi.fn(),
      });
      initTheme();
      expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
    });

    it("@FUT76 | system theme change listener updates theme when no stored choice", () => {
      localStorage.clear();
      let changeHandler;
      window.matchMedia = vi.fn().mockReturnValue({
        matches: false,
        addEventListener: vi.fn((_event, handler) => {
          changeHandler = handler;
        }),
      });
      initTheme();
      expect(document.documentElement.getAttribute("data-theme")).toBe("light");

      changeHandler({ matches: true });
      expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
    });

    it("@FUT77 | system theme change listener does NOT override explicit stored choice", () => {
      localStorage.setItem("theme", "light");
      let changeHandler;
      window.matchMedia = vi.fn().mockReturnValue({
        matches: false,
        addEventListener: vi.fn((_event, handler) => {
          changeHandler = handler;
        }),
      });
      initTheme();
      expect(document.documentElement.getAttribute("data-theme")).toBe("light");

      changeHandler({ matches: true });
      expect(document.documentElement.getAttribute("data-theme")).toBe("light");
    });

    it("@FUT83 | applies theme even when matchMedia listener registration is unavailable", () => {
      localStorage.clear();
      window.matchMedia = vi.fn().mockReturnValue({
        matches: true,
        addEventListener: () => {
          throw new Error("unsupported");
        },
      });

      expect(() => initTheme()).not.toThrow();
      expect(document.documentElement.getAttribute("data-theme")).toBe("dark");
    });
  });
});

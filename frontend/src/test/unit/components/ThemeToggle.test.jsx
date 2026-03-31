import React from "react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import ThemeToggle from "../../../components/ThemeToggle";
import * as theme from "../../../theme";

describe("ThemeToggle component", () => {
  beforeEach(() => {
    document.documentElement.setAttribute("data-theme", "light");
    document.documentElement.classList.remove("sl-theme-dark");
  });

  afterEach(() => {
    document.documentElement.removeAttribute("data-theme");
    vi.restoreAllMocks();
  });

  it("@FUT78 | renders toggle button with correct aria-label for light mode", () => {
    render(<ThemeToggle />);
    const button = screen.getByRole("button", {
      name: "Switch to dark mode",
    });
    expect(button).toBeTruthy();
    expect(button.getAttribute("aria-pressed")).toBe("false");
  });

  it("@FUT79 | renders toggle button with correct aria-label for dark mode", () => {
    document.documentElement.setAttribute("data-theme", "dark");
    render(<ThemeToggle />);
    const button = screen.getByRole("button", {
      name: "Switch to light mode",
    });
    expect(button).toBeTruthy();
    expect(button.getAttribute("aria-pressed")).toBe("true");
  });

  it("@FUT80 | calls toggleTheme when clicked", () => {
    const spy = vi.spyOn(theme, "toggleTheme").mockImplementation(() => {
      document.documentElement.setAttribute("data-theme", "dark");
      return "dark";
    });
    render(<ThemeToggle />);
    const button = screen.getByRole("button", {
      name: "Switch to dark mode",
    });
    fireEvent.click(button);
    expect(spy).toHaveBeenCalledOnce();
  });

  it("@FUT81 | updates aria label when data-theme changes externally", async () => {
    render(<ThemeToggle />);

    expect(
      screen.getByRole("button", { name: "Switch to dark mode" }),
    ).toBeTruthy();

    document.documentElement.setAttribute("data-theme", "dark");

    await waitFor(() => {
      const button = screen.getByRole("button", {
        name: "Switch to light mode",
      });
      expect(button.getAttribute("aria-pressed")).toBe("true");
    });
  });
});

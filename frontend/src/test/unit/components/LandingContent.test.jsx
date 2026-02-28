import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import LandingContent from "@/components/LandingContent";

describe("LandingContent", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("renders hero, features, and call-to-action content", () => {
    render(<LandingContent />);

    expect(
      screen.getByRole("heading", { name: "Todo App" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Key Features")).toBeInTheDocument();
    expect(screen.getByText("Organize")).toBeInTheDocument();
    expect(screen.getByText("Track Progress")).toBeInTheDocument();
    expect(screen.getByText(/Check the/i)).toBeInTheDocument();
  });

  it("renders expected decorative icons for sections", () => {
    render(<LandingContent />);

    expect(screen.getByText("📋")).toBeInTheDocument();
    expect(screen.getByText("📁")).toBeInTheDocument();
    expect(screen.getByText("✅")).toBeInTheDocument();
  });
});

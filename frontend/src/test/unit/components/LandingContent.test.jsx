import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen } from "@testing-library/react";
import LandingContent from "@/components/LandingContent";

describe("LandingContent", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it("@FUT10 | renders hero, features, and call-to-action content", async () => {
    render(<LandingContent />);

    expect(
      screen.getByRole("heading", { name: "Todo App" }),
    ).toBeInTheDocument();
    expect(screen.getByText("Key Features")).toBeInTheDocument();
    expect(screen.getByText("Organize")).toBeInTheDocument();
    expect(screen.getByText("Track Progress")).toBeInTheDocument();
    expect(screen.getByText(/Check the/i)).toBeInTheDocument();
  });

  it("@FUT11 | renders expected decorative icons for sections", async () => {
    render(<LandingContent />);

    expect(screen.getByText("📋")).toBeInTheDocument();
    expect(screen.getByText("📁")).toBeInTheDocument();
    expect(screen.getByText("✅")).toBeInTheDocument();
  });
});

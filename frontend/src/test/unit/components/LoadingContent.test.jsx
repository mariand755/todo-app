import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import LoadingContent from "@/components/LoadingContent";

describe("LoadingContent", () => {
  it("renders loading message and notepad animation svg", () => {
    const { container } = render(<LoadingContent />);

    expect(screen.getByText("Loading your folder...")).toBeInTheDocument();
    expect(container.querySelector("svg")).toBeInTheDocument();
    expect(container.querySelector(".notepad-animation")).toBeInTheDocument();
  });
});

import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import Sidebar from "@/components/Sidebar";

describe("Sidebar", () => {
  const folders = [
    { id: 1, title: "Work" },
    { id: 2, title: "Personal" },
  ];

  it("renders home button and folder items", () => {
    render(
      <Sidebar
        folders={folders}
        activeFolderId={1}
        onFolderClick={vi.fn()}
        onNewFolder={vi.fn()}
        onEditFolder={vi.fn()}
        onHomeClick={vi.fn()}
      />,
    );

    expect(
      screen.getByRole("button", { name: "Go to home" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Work (active)" }),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Personal" }),
    ).toBeInTheDocument();
  });

  it("calls onHomeClick from button click and keyboard", () => {
    const onHomeClick = vi.fn();

    render(
      <Sidebar
        folders={folders}
        activeFolderId={null}
        onFolderClick={vi.fn()}
        onNewFolder={vi.fn()}
        onEditFolder={vi.fn()}
        onHomeClick={onHomeClick}
      />,
    );

    const home = screen.getByRole("button", { name: "Go to home" });
    fireEvent.click(home);
    fireEvent.keyDown(home, { key: "Enter" });

    expect(onHomeClick).toHaveBeenCalledTimes(2);
  });

  it("calls onFolderClick when a folder is selected", () => {
    const onFolderClick = vi.fn();

    render(
      <Sidebar
        folders={folders}
        activeFolderId={null}
        onFolderClick={onFolderClick}
        onNewFolder={vi.fn()}
        onEditFolder={vi.fn()}
        onHomeClick={vi.fn()}
      />,
    );

    fireEvent.click(screen.getByRole("button", { name: "Personal" }));

    expect(onFolderClick).toHaveBeenCalledWith(2);
  });
});

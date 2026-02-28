import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import FolderItem from "@/components/FolderItem";

describe("FolderItem", () => {
  it("renders input content for add-folder row", () => {
    render(
      <ul>
        <FolderItem
          folder={{ id: "new", isInput: true, content: <div>New Form</div> }}
          isActive={false}
          onClick={vi.fn()}
          onEdit={vi.fn()}
        />
      </ul>,
    );

    expect(screen.getByText("New Form")).toBeInTheDocument();
  });

  it("calls onClick with folder id when clicked", () => {
    const onClick = vi.fn();

    render(
      <ul>
        <FolderItem
          folder={{ id: 7, title: "Work" }}
          isActive={false}
          onClick={onClick}
          onEdit={vi.fn()}
        />
      </ul>,
    );

    fireEvent.click(screen.getByRole("button", { name: "Work" }));
    expect(onClick).toHaveBeenCalledWith(7);
  });

  it("supports keyboard activation with Enter and Space", () => {
    const onClick = vi.fn();

    render(
      <ul>
        <FolderItem
          folder={{ id: 10, title: "Errands" }}
          isActive={false}
          onClick={onClick}
          onEdit={vi.fn()}
        />
      </ul>,
    );

    const folderButton = screen.getByRole("button", { name: "Errands" });
    fireEvent.keyDown(folderButton, { key: "Enter" });
    fireEvent.keyDown(folderButton, { key: " " });

    expect(onClick).toHaveBeenCalledTimes(2);
    expect(onClick).toHaveBeenNthCalledWith(1, 10);
    expect(onClick).toHaveBeenNthCalledWith(2, 10);
  });

  it("adds active aria label when selected", () => {
    render(
      <ul>
        <FolderItem
          folder={{ id: 12, title: "Active Folder" }}
          isActive={true}
          onClick={vi.fn()}
          onEdit={vi.fn()}
        />
      </ul>,
    );

    expect(
      screen.getByRole("button", { name: "Active Folder (active)" }),
    ).toBeInTheDocument();
  });
});

import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import FolderItem from "@/components/FolderItem";

describe("FolderItem", () => {
  it("@FUT05 | renders input content for add-folder row", async () => {
    render(
      <ul>
        <FolderItem
          folder={{ id: "new", isInput: true, content: <div>New Form</div> }}
          isActive={false}
          onClick={vi.fn()}
          onEdit={vi.fn()}
          onTogglePin={vi.fn()}
        />
      </ul>,
    );

    expect(screen.getByText("New Form")).toBeInTheDocument();
  });

  it("@FUT06 | calls onClick with folder id when clicked", async () => {
    const onClick = vi.fn();

    render(
      <ul>
        <FolderItem
          folder={{ id: 7, title: "Work" }}
          isActive={false}
          onClick={onClick}
          onEdit={vi.fn()}
          onTogglePin={vi.fn()}
        />
      </ul>,
    );

    fireEvent.click(screen.getByRole("button", { name: "Work" }));
    expect(onClick).toHaveBeenCalledWith(7);
  });

  it("@FUT07 | supports keyboard activation with Enter and Space", async () => {
    const onClick = vi.fn();

    render(
      <ul>
        <FolderItem
          folder={{ id: 10, title: "Errands" }}
          isActive={false}
          onClick={onClick}
          onEdit={vi.fn()}
          onTogglePin={vi.fn()}
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

  it("@FUT08 | adds active aria label when selected", async () => {
    render(
      <ul>
        <FolderItem
          folder={{ id: 12, title: "Active Folder" }}
          isActive={true}
          onClick={vi.fn()}
          onEdit={vi.fn()}
          onTogglePin={vi.fn()}
        />
      </ul>,
    );

    expect(
      screen.getByRole("button", { name: "Active Folder (active)" }),
    ).toBeInTheDocument();
  });

  it("@FUT09 | calls onTogglePin with inverted pin state", async () => {
    const onTogglePin = vi.fn();

    render(
      <ul>
        <FolderItem
          folder={{ id: 15, title: "Inbox", is_pinned: false }}
          isActive={false}
          onClick={vi.fn()}
          onEdit={vi.fn()}
          onTogglePin={onTogglePin}
        />
      </ul>,
    );

    fireEvent.click(screen.getByRole("button", { name: "Pin folder Inbox" }));

    expect(onTogglePin).toHaveBeenCalledWith(15, true);
  });
});

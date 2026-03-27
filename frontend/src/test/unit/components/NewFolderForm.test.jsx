import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import NewFolderForm from "@/components/NewFolderForm";

describe("NewFolderForm", () => {
  it("@FUT21 | submits trimmed title via button and clears input", async () => {
    const onNewFolder = vi.fn();
    render(<NewFolderForm onNewFolder={onNewFolder} />);

    const input = screen.getByLabelText("New folder name");
    fireEvent.change(input, { target: { value: "  Work  " } });
    fireEvent.click(screen.getByRole("button", { name: "Create new folder" }));

    expect(onNewFolder).toHaveBeenCalledWith("Work");
    expect(input).toHaveValue("");
  });

  it("@FUT22 | submits on Enter key press", async () => {
    const onNewFolder = vi.fn();
    render(<NewFolderForm onNewFolder={onNewFolder} />);

    const input = screen.getByLabelText("New folder name");
    fireEvent.change(input, { target: { value: "Personal" } });
    fireEvent.keyUp(input, { key: "Enter" });

    expect(onNewFolder).toHaveBeenCalledWith("Personal");
  });

  it("@FUT23 | does not submit empty or whitespace-only title", async () => {
    const onNewFolder = vi.fn();
    render(<NewFolderForm onNewFolder={onNewFolder} />);

    const input = screen.getByLabelText("New folder name");
    fireEvent.change(input, { target: { value: "   " } });
    fireEvent.click(screen.getByRole("button", { name: "Create new folder" }));

    expect(onNewFolder).not.toHaveBeenCalled();
  });

  it("@FUT54 | does not submit when non-Enter key is pressed in handleKeyPress", async () => {
    const onNewFolder = vi.fn();
    render(<NewFolderForm onNewFolder={onNewFolder} />);

    const input = screen.getByLabelText("New folder name");
    fireEvent.change(input, { target: { value: "New Folder" } });
    fireEvent.keyUp(input, { key: "Escape" });

    expect(onNewFolder).not.toHaveBeenCalled();
  });
});

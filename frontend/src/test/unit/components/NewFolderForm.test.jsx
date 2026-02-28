import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import NewFolderForm from "@/components/NewFolderForm";

describe("NewFolderForm", () => {
  it("submits trimmed title via button and clears input", () => {
    const onNewFolder = vi.fn();
    render(<NewFolderForm onNewFolder={onNewFolder} />);

    const input = screen.getByLabelText("New folder name");
    fireEvent.change(input, { target: { value: "  Work  " } });
    fireEvent.click(screen.getByRole("button", { name: "Create new folder" }));

    expect(onNewFolder).toHaveBeenCalledWith("Work");
    expect(input).toHaveValue("");
  });

  it("submits on Enter key press", () => {
    const onNewFolder = vi.fn();
    render(<NewFolderForm onNewFolder={onNewFolder} />);

    const input = screen.getByLabelText("New folder name");
    fireEvent.change(input, { target: { value: "Personal" } });
    fireEvent.keyUp(input, { key: "Enter" });

    expect(onNewFolder).toHaveBeenCalledWith("Personal");
  });

  it("does not submit empty or whitespace-only title", () => {
    const onNewFolder = vi.fn();
    render(<NewFolderForm onNewFolder={onNewFolder} />);

    const input = screen.getByLabelText("New folder name");
    fireEvent.change(input, { target: { value: "   " } });
    fireEvent.click(screen.getByRole("button", { name: "Create new folder" }));

    expect(onNewFolder).not.toHaveBeenCalled();
  });
});

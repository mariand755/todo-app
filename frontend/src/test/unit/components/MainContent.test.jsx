import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import MainContent from "@/components/MainContent";

vi.mock("@/components/TodoItem.jsx", () => ({
  default: ({ item }) => <li>{item.title}</li>,
}));

describe("MainContent", () => {
  const baseProps = {
    currentFolderTitle: "Work",
    currentFolderId: 1,
    items: [{ id: 1, title: "Task 1", completed: false }],
    onEditFolder: vi.fn(),
    onDeleteFolder: vi.fn(),
    onAddTodo: vi.fn(),
    onToggleTodo: vi.fn(),
    onDeleteToDoItem: vi.fn(),
    onEditToDoItem: vi.fn(),
    moveToDoItem: vi.fn(),
  };

  it("@FUT13 | renders folder title and todo items", async () => {
    render(<MainContent {...baseProps} />);

    expect(screen.getByRole("heading", { name: "Work" })).toBeInTheDocument();
    expect(screen.getByText("Task 1")).toBeInTheDocument();
  });

  it("@FUT14 | adds a todo with trimmed input and clears field", async () => {
    const onAddTodo = vi.fn();
    render(<MainContent {...baseProps} onAddTodo={onAddTodo} />);

    const input = screen.getByLabelText("New todo item");
    fireEvent.change(input, { target: { value: "  Buy milk  " } });
    fireEvent.submit(input.closest("form"));

    expect(onAddTodo).toHaveBeenCalledWith("Buy milk");
    expect(input).toHaveValue("");
  });

  it("@FUT15 | does not add empty todo values", async () => {
    const onAddTodo = vi.fn();
    render(<MainContent {...baseProps} onAddTodo={onAddTodo} />);

    const input = screen.getByLabelText("New todo item");
    fireEvent.change(input, { target: { value: "   " } });
    fireEvent.submit(input.closest("form"));

    expect(onAddTodo).not.toHaveBeenCalled();
  });

  it("@FUT16 | opens edit dialog and submits edited folder title", async () => {
    const onEditFolder = vi.fn();
    render(<MainContent {...baseProps} onEditFolder={onEditFolder} />);

    fireEvent.click(screen.getByRole("button", { name: "Edit" }));
    const editInput = screen.getByLabelText("New folder name");
    fireEvent.keyDown(editInput, {
      key: "Enter",
      target: { value: "Updated Work" },
    });

    expect(onEditFolder).toHaveBeenCalledWith(1, "Updated Work");
  });

  it("@FUT17 | opens delete dialog and confirms delete", async () => {
    const onDeleteFolder = vi.fn();
    render(<MainContent {...baseProps} onDeleteFolder={onDeleteFolder} />);

    fireEvent.click(screen.getByRole("button", { name: "Delete" }));
    fireEvent.click(screen.getAllByRole("button", { name: "OK" })[0]);

    expect(onDeleteFolder).toHaveBeenCalledWith(1);
  });

  it("@FUT18 | confirms delete when Enter is pressed on the dialog action button", async () => {
    const onDeleteFolder = vi.fn();
    render(<MainContent {...baseProps} onDeleteFolder={onDeleteFolder} />);

    fireEvent.click(screen.getByRole("button", { name: "Delete" }));
    const confirmButton = screen.getAllByRole("button", { name: "OK" })[0];
    fireEvent.keyDown(confirmButton, { key: "Enter" });

    expect(onDeleteFolder).toHaveBeenCalledWith(1);
  });

  it("@FUT19 | does not render pin action in the folder menu", async () => {
    render(<MainContent {...baseProps} />);

    expect(screen.queryByText("Pin")).not.toBeInTheDocument();
    expect(screen.queryByText("Unpin")).not.toBeInTheDocument();
  });

  it("@FUT20 | disables folder edit autocomplete hints", async () => {
    render(<MainContent {...baseProps} />);

    fireEvent.click(screen.getByRole("button", { name: "Edit" }));
    const editInput = screen.getByLabelText("New folder name");

    expect(editInput).toHaveAttribute("autocomplete", "off");
    expect(editInput).toHaveAttribute("autocorrect", "off");
    expect(editInput).toHaveAttribute("autocapitalize", "off");
    expect(editInput.getAttribute("name")).toContain("folder-edit-title-");
  });

  it("@FUT37 | submitting an empty folder title closes dialog without editing", async () => {
    const onEditFolder = vi.fn();
    render(<MainContent {...baseProps} onEditFolder={onEditFolder} />);

    fireEvent.click(screen.getByRole("button", { name: "Edit" }));
    const editInput = screen.getByLabelText("New folder name");
    fireEvent.keyDown(editInput, { key: "Enter", target: { value: "   " } });

    expect(onEditFolder).not.toHaveBeenCalled();
    expect(
      screen.queryByRole("dialog", { name: "Edit Folder Name" }),
    ).not.toBeInTheDocument();
  });

  it("@FUT38 | Escape in edit folder dialog input closes the dialog", async () => {
    const onEditFolder = vi.fn();
    render(<MainContent {...baseProps} onEditFolder={onEditFolder} />);

    fireEvent.click(screen.getByRole("button", { name: "Edit" }));
    const editInput = screen.getByLabelText("New folder name");
    fireEvent.keyDown(editInput, { key: "Escape" });

    expect(onEditFolder).not.toHaveBeenCalled();
    expect(
      screen.queryByRole("dialog", { name: "Edit Folder Name" }),
    ).not.toBeInTheDocument();
  });

  it("@FUT39 | Space on delete confirm button calls onDeleteFolder", async () => {
    const onDeleteFolder = vi.fn();
    render(<MainContent {...baseProps} onDeleteFolder={onDeleteFolder} />);

    fireEvent.click(screen.getByRole("button", { name: "Delete" }));
    const confirmButton = screen.getAllByRole("button", { name: "OK" })[0];
    fireEvent.keyDown(confirmButton, { key: " " });

    expect(onDeleteFolder).toHaveBeenCalledWith(1);
  });

  it("@FUT40 | renders empty state message when items list is empty", async () => {
    render(<MainContent {...baseProps} items={[]} />);

    expect(screen.getByText("No items in this folder.")).toBeInTheDocument();
  });

  it("@FUT55 | does not render folder controls when currentFolderId is null", async () => {
    render(<MainContent {...baseProps} currentFolderId={null} />);

    expect(
      screen.queryByRole("button", { name: "Folder options menu" }),
    ).not.toBeInTheDocument();
  });

  it("@FUT56 | does not call onAddTodo when it is undefined (typeof guard)", async () => {
    render(<MainContent {...baseProps} onAddTodo={undefined} />);

    const input = screen.getByLabelText("New todo item");
    fireEvent.change(input, { target: { value: "Test" } });
    fireEvent.submit(input.closest("form"));

    expect(input).toHaveValue("");
  });
});

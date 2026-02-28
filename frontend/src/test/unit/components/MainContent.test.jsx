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

  it("renders folder title and todo items", () => {
    render(<MainContent {...baseProps} />);

    expect(screen.getByRole("heading", { name: "Work" })).toBeInTheDocument();
    expect(screen.getByText("Task 1")).toBeInTheDocument();
  });

  it("adds a todo with trimmed input and clears field", () => {
    const onAddTodo = vi.fn();
    render(<MainContent {...baseProps} onAddTodo={onAddTodo} />);

    const input = screen.getByLabelText("New todo item");
    fireEvent.change(input, { target: { value: "  Buy milk  " } });
    fireEvent.submit(input.closest("form"));

    expect(onAddTodo).toHaveBeenCalledWith("Buy milk");
    expect(input).toHaveValue("");
  });

  it("does not add empty todo values", () => {
    const onAddTodo = vi.fn();
    render(<MainContent {...baseProps} onAddTodo={onAddTodo} />);

    const input = screen.getByLabelText("New todo item");
    fireEvent.change(input, { target: { value: "   " } });
    fireEvent.submit(input.closest("form"));

    expect(onAddTodo).not.toHaveBeenCalled();
  });

  it("opens edit dialog and submits edited folder title", () => {
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

  it("opens delete dialog and confirms delete", () => {
    const onDeleteFolder = vi.fn();
    render(<MainContent {...baseProps} onDeleteFolder={onDeleteFolder} />);

    fireEvent.click(screen.getByRole("button", { name: "Delete" }));
    fireEvent.click(screen.getAllByRole("button", { name: "OK" })[0]);

    expect(onDeleteFolder).toHaveBeenCalledWith(1);
  });
});

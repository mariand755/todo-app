import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import TodoItem from "@/components/TodoItem";

vi.mock("react-dnd", () => ({
  useDrag: () => [{ isDragging: false }, vi.fn()],
  useDrop: () => [{ handlerId: "handler-1" }, vi.fn()],
}));

describe("TodoItem", () => {
  const baseItem = { id: 10, title: "Write tests", completed: false };

  const baseProps = {
    item: baseItem,
    index: 0,
    onToggle: vi.fn(),
    onDeleteToDoItem: vi.fn(),
    onEditToDoItem: vi.fn(),
    moveToDoItem: vi.fn(),
  };

  it("toggles completion when checkbox changes", () => {
    const onToggle = vi.fn();
    render(<TodoItem {...baseProps} onToggle={onToggle} />);

    fireEvent.click(
      screen.getByRole("checkbox", { name: "Mark as complete: Write tests" }),
    );
    expect(onToggle).toHaveBeenCalledWith(10);
  });

  it("opens edit dialog and submits updated title via Enter", () => {
    const onEditToDoItem = vi.fn();
    render(<TodoItem {...baseProps} onEditToDoItem={onEditToDoItem} />);

    fireEvent.click(screen.getByRole("button", { name: "Edit" }));
    const input = screen.getByLabelText("New item name");
    fireEvent.keyDown(input, {
      key: "Enter",
      target: { value: "Updated title" },
    });

    expect(onEditToDoItem).toHaveBeenCalledWith(10, "Updated title");
  });

  it("opens delete dialog and confirms deletion", () => {
    const onDeleteToDoItem = vi.fn();
    render(<TodoItem {...baseProps} onDeleteToDoItem={onDeleteToDoItem} />);

    fireEvent.click(screen.getByRole("button", { name: "Delete" }));
    fireEvent.click(screen.getAllByRole("button", { name: "OK" })[0]);

    expect(onDeleteToDoItem).toHaveBeenCalledWith(10);
  });

  it("does not show edit option for completed item", () => {
    render(<TodoItem {...baseProps} item={{ ...baseItem, completed: true }} />);

    expect(
      screen.queryByRole("button", { name: "Edit" }),
    ).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Delete" })).toBeInTheDocument();
  });

  it("applies complete class and incomplete aria label when item is completed", () => {
    const { container } = render(
      <TodoItem {...baseProps} item={{ ...baseItem, completed: true }} />,
    );

    expect(
      screen.getByRole("checkbox", { name: "Mark as incomplete: Write tests" }),
    ).toBeInTheDocument();
    expect(container.querySelector(".todo-item.complete")).toBeInTheDocument();
  });
});

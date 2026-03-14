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

  it("@FUT28 | toggles completion when checkbox changes", async () => {
    const onToggle = vi.fn();
    render(<TodoItem {...baseProps} onToggle={onToggle} />);

    fireEvent.click(
      screen.getByRole("checkbox", { name: "Mark as complete: Write tests" }),
    );
    expect(onToggle).toHaveBeenCalledWith(10);
  });

  it("@FUT29 | opens edit dialog and submits updated title via Enter", async () => {
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

  it("@FUT30 | opens delete dialog and confirms deletion via click", async () => {
    const onDeleteToDoItem = vi.fn();
    render(<TodoItem {...baseProps} onDeleteToDoItem={onDeleteToDoItem} />);

    fireEvent.click(screen.getByRole("button", { name: "Delete" }));
    fireEvent.click(screen.getAllByRole("button", { name: "OK" })[0]);

    expect(onDeleteToDoItem).toHaveBeenCalledWith(10);
  });

  it("@FUT31 | closes delete dialog and confirms deletion via Enter key", async () => {
    const onDeleteToDoItem = vi.fn();
    render(<TodoItem {...baseProps} onDeleteToDoItem={onDeleteToDoItem} />);

    fireEvent.click(screen.getByRole("button", { name: "Delete" }));
    const confirmButton = screen.getAllByRole("button", { name: "OK" })[0];
    fireEvent.keyDown(confirmButton, { key: "Enter" });

    expect(onDeleteToDoItem).toHaveBeenCalledWith(10);
  });

  it("@FUT32 | does not show edit option for completed item", async () => {
    render(<TodoItem {...baseProps} item={{ ...baseItem, completed: true }} />);

    expect(
      screen.queryByRole("button", { name: "Edit" }),
    ).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Delete" })).toBeInTheDocument();
  });

  it("@FUT33 | applies complete class and incomplete aria label when item is completed", async () => {
    const { container } = render(
      <TodoItem {...baseProps} item={{ ...baseItem, completed: true }} />,
    );

    expect(
      screen.getByRole("checkbox", { name: "Mark as incomplete: Write tests" }),
    ).toBeInTheDocument();
    expect(container.querySelector(".todo-item.complete")).toBeInTheDocument();
  });
});

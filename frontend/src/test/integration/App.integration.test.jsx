import React from "react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import App from "@/App";
import { makeAPICall } from "@/useApi";

vi.mock("@shoelace-style/shoelace/dist/utilities/base-path.js", () => ({
  setBasePath: vi.fn(),
}));

vi.mock("@/useApi", () => ({
  makeAPICall: vi.fn(),
}));

vi.mock("@/components/Sidebar", () => ({
  default: ({
    folders = [],
    onFolderClick,
    onHomeClick,
    onToggleFolderPin,
    onNewFolder,
  }) => (
    <div>
      <div data-testid="sidebar-order">
        {folders.map((f) => f.title).join("|")}
      </div>
      <button onClick={() => onFolderClick(1)}>Select Folder 1</button>
      <button onClick={() => onFolderClick(2)}>Select Folder 2</button>
      <button onClick={() => onToggleFolderPin?.(2, true)}>Pin Folder 2</button>
      <button onClick={() => onNewFolder?.("Test Folder")}>New Folder</button>
      <button onClick={onHomeClick}>Home</button>
    </div>
  ),
}));

vi.mock("@/components/MainContent", () => ({
  default: ({
    currentFolderTitle,
    currentFolderId,
    items,
    onEditFolder,
    onDeleteFolder,
    onAddTodo,
    onToggleTodo,
    onDeleteToDoItem,
    onEditToDoItem,
    moveToDoItem,
  }) => (
    <div>
      <div>Main: {currentFolderTitle}</div>
      <div>Folder: {currentFolderId}</div>
      <div>Items: {items.length}</div>
      <button onClick={() => onEditFolder(currentFolderId, "Renamed Folder")}>
        Edit Folder
      </button>
      <button onClick={() => onDeleteFolder(currentFolderId)}>
        Delete Folder
      </button>
      <button onClick={() => onAddTodo("Added Task")}>Add Todo</button>
      <button onClick={() => onToggleTodo(items[0]?.id ?? 0)}>
        Toggle Todo
      </button>
      <button onClick={() => onDeleteToDoItem(items[0]?.id ?? 0)}>
        Delete Todo
      </button>
      <button onClick={() => onEditToDoItem(items[0]?.id ?? 0, "Edited Task")}>
        Edit Todo
      </button>
      <button onClick={() => moveToDoItem(0, 1)}>Reorder Todos</button>
    </div>
  ),
}));

vi.mock("@/components/LandingContent", () => ({
  default: () => <div>Landing Screen</div>,
}));

vi.mock("@/components/LoadingContent", () => ({
  default: () => <div>Loading Screen</div>,
}));

const mockResponse = (data) => ({
  json: vi.fn().mockResolvedValue(data),
});

describe("App", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    window.history.pushState({}, "", "/");
  });

  it("@FINT01 | loads folders on mount and shows landing content by default", async () => {
    makeAPICall.mockResolvedValueOnce(mockResponse([{ id: 1, title: "Work" }]));

    render(<App />);

    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("GET", "/folders");
    });

    expect(await screen.findByText("Landing Screen")).toBeInTheDocument();
  });

  it("@FINT02 | loads folder items when selecting a folder and shows main content", async () => {
    makeAPICall
      .mockResolvedValueOnce(mockResponse([{ id: 1, title: "Work" }]))
      .mockResolvedValueOnce(
        mockResponse([{ id: 10, title: "Task", completed: false }]),
      );

    render(<App />);

    await screen.findByText("Landing Screen");
    fireEvent.click(screen.getByText("Select Folder 1"));

    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("GET", "/folders/1/items/");
    });

    expect(await screen.findByText("Main: Work")).toBeInTheDocument();
  });

  it("@FINT03 | loads folder from initial deep link URL", async () => {
    window.history.pushState({}, "", "/folders/2");

    makeAPICall
      .mockResolvedValueOnce(mockResponse([{ id: 2, title: "Deep Linked" }]))
      .mockResolvedValueOnce(
        mockResponse([{ id: 20, title: "From URL", completed: false }]),
      );

    render(<App />);

    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("GET", "/folders/2/items/");
    });

    expect(await screen.findByText("Main: Deep Linked")).toBeInTheDocument();
  });

  it("@FINT04 | updates folder title immediately after edit for deep-linked folder IDs", async () => {
    window.history.pushState({}, "", "/folders/2");

    makeAPICall
      .mockResolvedValueOnce(mockResponse([{ id: 2, title: "Deep Linked" }]))
      .mockResolvedValueOnce(
        mockResponse([{ id: 20, title: "From URL", completed: false }]),
      )
      .mockResolvedValueOnce(
        mockResponse({ id: 2, title: "Deep Linked Renamed" }),
      );

    render(<App />);

    expect(await screen.findByText("Main: Deep Linked")).toBeInTheDocument();
    fireEvent.click(screen.getByText("Edit Folder"));

    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("PUT", "/folders/2", {
        title: "Renamed Folder",
      });
    });

    expect(
      await screen.findByText("Main: Deep Linked Renamed"),
    ).toBeInTheDocument();
  });

  it("@FINT05 | returns to landing content when Home is clicked", async () => {
    makeAPICall
      .mockResolvedValueOnce(mockResponse([{ id: 1, title: "Work" }]))
      .mockResolvedValueOnce(
        mockResponse([{ id: 10, title: "Task", completed: false }]),
      );

    render(<App />);

    await screen.findByText("Landing Screen");
    fireEvent.click(screen.getByText("Select Folder 1"));
    await screen.findByText("Main: Work");

    fireEvent.click(screen.getByText("Home"));

    expect(await screen.findByText("Landing Screen")).toBeInTheDocument();
  });

  it("@FINT06 | fetches folder metadata when active folder is missing in local folder list", async () => {
    window.history.pushState({}, "", "/folders/77");

    makeAPICall
      .mockResolvedValueOnce(mockResponse([]))
      .mockResolvedValueOnce(
        mockResponse([{ id: 101, title: "Task A", completed: false }]),
      )
      .mockResolvedValueOnce(mockResponse({ id: 77, title: "Fetched Folder" }));

    render(<App />);

    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("GET", "/folders/77");
    });

    expect(await screen.findByText("Main: Fetched Folder")).toBeInTheDocument();
  });

  it("@FINT07 | handles todo item CRUD actions through MainContent callbacks", async () => {
    makeAPICall
      .mockResolvedValueOnce(mockResponse([{ id: 1, title: "Work" }]))
      .mockResolvedValueOnce(
        mockResponse([{ id: 10, title: "Task", completed: false }]),
      )
      .mockResolvedValueOnce(
        mockResponse({ id: 11, title: "Added Task", completed: false }),
      )
      .mockResolvedValueOnce(
        mockResponse({ id: 10, title: "Task", completed: true }),
      )
      .mockResolvedValueOnce(
        mockResponse({ id: 10, title: "Edited Task", completed: true }),
      )
      .mockResolvedValueOnce(mockResponse({ success: true }));

    render(<App />);

    await screen.findByText("Landing Screen");
    fireEvent.click(screen.getByText("Select Folder 1"));
    await screen.findByText("Main: Work");

    fireEvent.click(screen.getByText("Add Todo"));
    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("POST", "/folders/1/items/", {
        title: "Added Task",
      });
    });

    fireEvent.click(screen.getByText("Toggle Todo"));
    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith(
        "PUT",
        "/folders/1/items/10/toggle",
      );
    });

    fireEvent.click(screen.getByText("Edit Todo"));
    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("PUT", "/folders/1/items/10", {
        title: "Edited Task",
      });
    });

    fireEvent.click(screen.getByText("Delete Todo"));
    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("DELETE", "/folders/1/items/10");
    });
  });

  it("@FINT08 | handles folder edit and delete actions through MainContent callbacks", async () => {
    makeAPICall
      .mockResolvedValueOnce(mockResponse([{ id: 1, title: "Work" }]))
      .mockResolvedValueOnce(
        mockResponse([{ id: 10, title: "Task", completed: false }]),
      )
      .mockResolvedValueOnce(mockResponse({ id: 1, title: "Renamed Folder" }))
      .mockResolvedValueOnce(mockResponse({ success: true }));

    render(<App />);

    await screen.findByText("Landing Screen");
    fireEvent.click(screen.getByText("Select Folder 1"));
    await screen.findByText("Main: Work");

    fireEvent.click(screen.getByText("Edit Folder"));
    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("PUT", "/folders/1", {
        title: "Renamed Folder",
      });
    });

    fireEvent.click(screen.getByText("Delete Folder"));
    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("DELETE", "/folders/1");
    });

    expect(await screen.findByText("Landing Screen")).toBeInTheDocument();
  });

  it("@FINT09 | pins a folder through API and reorders sidebar with pinned folder first", async () => {
    makeAPICall
      .mockResolvedValueOnce(
        mockResponse([
          { id: 1, title: "Work", is_pinned: false, position: 0 },
          { id: 2, title: "Personal", is_pinned: false, position: 1 },
        ]),
      )
      .mockResolvedValueOnce(
        mockResponse({
          id: 2,
          title: "Personal",
          is_pinned: true,
          position: 1,
        }),
      );

    render(<App />);

    await screen.findByText("Landing Screen");
    expect(screen.getByTestId("sidebar-order")).toHaveTextContent(
      "Work|Personal",
    );

    fireEvent.click(screen.getByText("Pin Folder 2"));

    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("PUT", "/folders/2/pin", {
        is_pinned: true,
      });
    });

    await waitFor(() => {
      expect(screen.getByTestId("sidebar-order")).toHaveTextContent(
        "Personal|Work",
      );
    });
  });

  it("@FINT10 | reorders items and sends persisted order to item_order endpoint", async () => {
    makeAPICall
      .mockResolvedValueOnce(mockResponse([{ id: 1, title: "Work" }]))
      .mockResolvedValueOnce(
        mockResponse([
          { id: 10, title: "First", completed: false },
          { id: 20, title: "Second", completed: false },
        ]),
      )
      .mockResolvedValueOnce(
        mockResponse({
          items: [
            { id: 20, title: "Second", completed: false },
            { id: 10, title: "First", completed: false },
          ],
        }),
      );

    render(<App />);

    await screen.findByText("Landing Screen");
    fireEvent.click(screen.getByText("Select Folder 1"));
    await screen.findByText("Main: Work");

    fireEvent.click(screen.getByText("Reorder Todos"));
    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("PUT", "/folders/1/item_order", {
        itemOrder_id: [20, 10],
      });
    });
  });

  it("@FINT11 | reacts to popstate by returning to home state when URL has no folder", async () => {
    makeAPICall
      .mockResolvedValueOnce(mockResponse([{ id: 1, title: "Work" }]))
      .mockResolvedValueOnce(
        mockResponse([{ id: 10, title: "Task", completed: false }]),
      );

    render(<App />);

    await screen.findByText("Landing Screen");
    fireEvent.click(screen.getByText("Select Folder 1"));
    await screen.findByText("Main: Work");

    window.history.pushState({}, "", "/");
    window.dispatchEvent(new PopStateEvent("popstate"));

    expect(await screen.findByText("Landing Screen")).toBeInTheDocument();
  });

  it("@FINT12 | null API response for add-todo leaves items unchanged", async () => {
    makeAPICall
      .mockResolvedValueOnce(mockResponse([{ id: 1, title: "Work" }]))
      .mockResolvedValueOnce(
        mockResponse([{ id: 10, title: "Task", completed: false }]),
      )
      .mockResolvedValueOnce(null);

    render(<App />);

    await screen.findByText("Landing Screen");
    fireEvent.click(screen.getByText("Select Folder 1"));
    await screen.findByText("Main: Work");

    expect(screen.getByText("Items: 1")).toBeInTheDocument();

    fireEvent.click(screen.getByText("Add Todo"));

    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("POST", "/folders/1/items/", {
        title: "Added Task",
      });
    });

    expect(screen.getByText("Items: 1")).toBeInTheDocument();
  });

  it("@FINT13 | null API response for pin-folder leaves sidebar order unchanged", async () => {
    makeAPICall
      .mockResolvedValueOnce(
        mockResponse([
          { id: 1, title: "Work", is_pinned: false, position: 0 },
          { id: 2, title: "Personal", is_pinned: false, position: 1 },
        ]),
      )
      .mockResolvedValueOnce(null);

    render(<App />);

    await screen.findByText("Landing Screen");
    expect(screen.getByTestId("sidebar-order")).toHaveTextContent(
      "Work|Personal",
    );

    fireEvent.click(screen.getByText("Pin Folder 2"));

    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("PUT", "/folders/2/pin", {
        is_pinned: true,
      });
    });

    expect(screen.getByTestId("sidebar-order")).toHaveTextContent(
      "Work|Personal",
    );
  });

  it("@FINT14 | null API response for edit-folder leaves title unchanged", async () => {
    makeAPICall
      .mockResolvedValueOnce(mockResponse([{ id: 1, title: "Work" }]))
      .mockResolvedValueOnce(
        mockResponse([{ id: 10, title: "Task", completed: false }]),
      )
      .mockResolvedValueOnce(null);

    render(<App />);

    await screen.findByText("Landing Screen");
    fireEvent.click(screen.getByText("Select Folder 1"));
    await screen.findByText("Main: Work");

    fireEvent.click(screen.getByText("Edit Folder"));

    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("PUT", "/folders/1", {
        title: "Renamed Folder",
      });
    });

    expect(screen.getByText("Main: Work")).toBeInTheDocument();
  });

  it("@FINT15 | null API response for delete-folder keeps folder in sidebar", async () => {
    makeAPICall
      .mockResolvedValueOnce(mockResponse([{ id: 1, title: "Work" }]))
      .mockResolvedValueOnce(
        mockResponse([{ id: 10, title: "Task", completed: false }]),
      )
      .mockResolvedValueOnce(null);

    render(<App />);

    await screen.findByText("Landing Screen");
    fireEvent.click(screen.getByText("Select Folder 1"));
    await screen.findByText("Main: Work");

    fireEvent.click(screen.getByText("Delete Folder"));

    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("DELETE", "/folders/1");
    });

    expect(screen.getByText("Main: Work")).toBeInTheDocument();
  });

  it("@FINT16 | null API response for new-folder does not update sidebar", async () => {
    makeAPICall
      .mockResolvedValueOnce(mockResponse([]))
      .mockResolvedValueOnce(null);

    render(<App />);

    await screen.findByText("Landing Screen");
    expect(screen.getByTestId("sidebar-order")).toHaveTextContent("");

    fireEvent.click(screen.getByText("New Folder"));

    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith("POST", "/folders", {
        title: "Test Folder",
      });
    });

    expect(screen.getByTestId("sidebar-order")).toHaveTextContent("");
  });

  it("@FINT17 | null API response for toggle-todo leaves items unchanged", async () => {
    makeAPICall
      .mockResolvedValueOnce(mockResponse([{ id: 1, title: "Work" }]))
      .mockResolvedValueOnce(
        mockResponse([{ id: 10, title: "Task", completed: false }]),
      )
      .mockResolvedValueOnce(null);

    render(<App />);

    await screen.findByText("Landing Screen");
    fireEvent.click(screen.getByText("Select Folder 1"));
    await screen.findByText("Main: Work");
    expect(screen.getByText("Items: 1")).toBeInTheDocument();

    fireEvent.click(screen.getByText("Toggle Todo"));

    await waitFor(() => {
      expect(makeAPICall).toHaveBeenCalledWith(
        "PUT",
        "/folders/1/items/10/toggle",
      );
    });

    expect(screen.getByText("Items: 1")).toBeInTheDocument();
  });
});

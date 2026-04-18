import React, { useEffect, useState } from "react";
import update from "immutability-helper";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";
import { setBasePath } from "@shoelace-style/shoelace/dist/utilities/base-path.js";

import { logger } from "./logger";
import { makeAPICall } from "./useApi";
import Sidebar from "./components/Sidebar";
import MainContent from "./components/MainContent";
import LandingContent from "./components/LandingContent";
import LoadingContent from "./components/LoadingContent";
import ThemeToggle from "./components/ThemeToggle";
import "./styles.css";
import "@shoelace-style/shoelace/dist/themes/light.css";
import "@shoelace-style/shoelace/dist/themes/dark.css";

setBasePath(
  "https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.20.1/cdn/",
);

const sortFoldersForSidebar = (folderList) => {
  return [...folderList].sort((left, right) => {
    const leftPinned = Boolean(left?.is_pinned);
    const rightPinned = Boolean(right?.is_pinned);

    if (leftPinned !== rightPinned) {
      return leftPinned ? -1 : 1;
    }

    const leftPosition = Number.isFinite(left?.position)
      ? left.position
      : Number.MAX_SAFE_INTEGER;
    const rightPosition = Number.isFinite(right?.position)
      ? right.position
      : Number.MAX_SAFE_INTEGER;

    if (leftPosition !== rightPosition) {
      return leftPosition - rightPosition;
    }

    const leftId = Number(left?.id);
    const rightId = Number(right?.id);
    if (
      Number.isFinite(leftId) &&
      Number.isFinite(rightId) &&
      leftId !== rightId
    ) {
      return leftId - rightId;
    }

    return String(left?.id ?? "").localeCompare(String(right?.id ?? ""));
  });
};

function App() {
  const [folders, setFolders] = useState([]);
  const [items, setItems] = useState([]);
  const [activeFolderId, setActiveFolderId] = useState(null);
  const [isInitializing, setIsInitializing] = useState(true);
  const [isLoadingFolders, setIsLoadingFolders] = useState(true);

  // Fetch folders on mount.
  useEffect(() => {
    let cancelled = false;

    const fetchFolders = async () => {
      try {
        const data = await makeAPICall("GET", "/folders");
        if (!data || cancelled) {
          return;
        }

        const fetchedFolders = await data.json();
        if (cancelled) {
          return;
        }

        setFolders(sortFoldersForSidebar(fetchedFolders));
      } catch (error) {
        logger.info("Failed to fetch folders", { error });
      } finally {
        if (!cancelled) {
          setIsLoadingFolders(false);
        }
      }
    };

    fetchFolders();

    return () => {
      cancelled = true;
    };
  }, []);

  // Helper: extract folder id from URL (supports /folders/:id or ?folder=ID).
  const getFolderIdFromURL = () => {
    try {
      const params = new URLSearchParams(window.location.search);
      if (params.has("folder")) {
        return params.get("folder");
      }

      const match = window.location.pathname.match(/\/folders\/([^/?#]+)/);
      return match ? decodeURIComponent(match[1]) : null;
    } catch (_error) {
      return null;
    }
  };

  // Logic for loading items, now optionally controls history push.
  const loadFolderItems = async (folderId, pushHistory = true) => {
    if (!folderId) return;
    if (String(folderId) === String(activeFolderId)) return;

    const data = await makeAPICall("GET", `/folders/${folderId}/items`);
    if (!data) {
      return;
    }

    const fetchedItems = await data.json();
    setItems(fetchedItems);
    setActiveFolderId(folderId);
    setIsInitializing(false);

    if (!pushHistory) {
      return;
    }

    try {
      window.history.pushState(
        { folderId },
        "",
        `/folders/${encodeURIComponent(folderId)}`,
      );
    } catch (_error) {
      // Ignore history errors.
    }
  };

  // Respond to browser back/forward.
  /* eslint-disable react-hooks/exhaustive-deps */
  useEffect(() => {
    const onPop = () => {
      const id = getFolderIdFromURL();
      if (id) {
        loadFolderItems(id, false);
        return;
      }

      setActiveFolderId(null);
      setItems([]);
    };

    window.addEventListener("popstate", onPop);

    const initial = getFolderIdFromURL();
    if (initial) {
      loadFolderItems(initial, false);
    } else {
      setIsInitializing(false);
    }

    return () => window.removeEventListener("popstate", onPop);
  }, []);
  /* eslint-enable react-hooks/exhaustive-deps */

  const handleNewFolder = async (title) => {
    const rawApiResponse = await makeAPICall("POST", "/folders", { title });
    if (!rawApiResponse) {
      return;
    }

    const newFolder = await rawApiResponse.json();
    setFolders((prevFolders) =>
      sortFoldersForSidebar([...prevFolders, newFolder]),
    );
  };

  const handleEditFolder = async (folderId, newTitle) => {
    const rawApiResponse = await makeAPICall("PUT", `/folders/${folderId}`, {
      title: newTitle,
    });
    if (!rawApiResponse) {
      return;
    }

    const updatedFolder = await rawApiResponse.json();
    setFolders((prevFolders) =>
      sortFoldersForSidebar(
        prevFolders.map((folder) =>
          String(folder.id) === String(folderId)
            ? { ...folder, ...updatedFolder }
            : folder,
        ),
      ),
    );
  };

  const handleToggleFolderPin = async (folderId, isPinned) => {
    const rawApiResponse = await makeAPICall(
      "PUT",
      `/folders/${folderId}/pin`,
      {
        is_pinned: isPinned,
      },
    );
    if (!rawApiResponse) {
      return;
    }

    const updatedFolder = await rawApiResponse.json();
    setFolders((prevFolders) =>
      sortFoldersForSidebar(
        prevFolders.map((folder) =>
          String(folder.id) === String(folderId)
            ? { ...folder, ...updatedFolder }
            : folder,
        ),
      ),
    );
  };

  const handleDeleteFolder = async (folderId) => {
    const rawApiResponse = await makeAPICall("DELETE", `/folders/${folderId}`);
    if (!rawApiResponse) {
      return;
    }

    setFolders((prevFolders) =>
      prevFolders.filter((folder) => String(folder.id) !== String(folderId)),
    );

    if (String(folderId) !== String(activeFolderId)) {
      return;
    }

    setActiveFolderId(null);
    setItems([]);
    try {
      window.history.pushState({}, "", "/");
    } catch (_error) {
      // Ignore history errors.
    }
  };

  const handleHomeClick = () => {
    setActiveFolderId(null);
    setItems([]);
    try {
      window.history.pushState({}, "", "/");
    } catch (_error) {
      // Ignore history errors.
    }
  };

  const handleAddTodo = async (title) => {
    const rawApiResponse = await makeAPICall(
      "POST",
      `/folders/${activeFolderId}/items`,
      {
        title,
      },
    );
    if (!rawApiResponse) {
      return;
    }

    const newItem = await rawApiResponse.json();
    setItems((prevItems) => [...prevItems, newItem]);
  };

  const onToggleTodo = async (itemId) => {
    const rawApiResponse = await makeAPICall(
      "PUT",
      `/folders/${activeFolderId}/items/${itemId}/toggle`,
    );
    if (!rawApiResponse) {
      return;
    }

    const updatedItem = await rawApiResponse.json();
    setItems((prevItems) =>
      prevItems.map((item) => (item.id === itemId ? updatedItem : item)),
    );
  };

  const handleDeleteToDoItem = async (itemId) => {
    const rawApiResponse = await makeAPICall(
      "DELETE",
      `/folders/${activeFolderId}/items/${itemId}`,
    );
    if (!rawApiResponse) {
      return;
    }

    setItems((prevItems) => prevItems.filter((item) => item.id !== itemId));
  };

  const handleEditToDoItem = async (itemId, newTitle) => {
    const rawApiResponse = await makeAPICall(
      "PUT",
      `/folders/${activeFolderId}/items/${itemId}`,
      { title: newTitle },
    );
    if (!rawApiResponse) {
      return;
    }

    const updatedItem = await rawApiResponse.json();
    setItems((prevItems) =>
      prevItems.map((item) => (item.id === itemId ? updatedItem : item)),
    );
  };

  const handleReorderItems = async (itemIds) => {
    if (!activeFolderId) return;

    logger.debug("Reordering items", { itemIds, activeFolderId });
    const rawApiResponse = await makeAPICall(
      "PUT",
      `/folders/${activeFolderId}/item_order`,
      {
        itemOrder_id: itemIds,
      },
    );
    if (!rawApiResponse) {
      return;
    }

    const response = await rawApiResponse.json();
    setItems(response.items);
  };

  // Ensure folder metadata is available so folder title can render after a reload/deeplink.
  useEffect(() => {
    if (!activeFolderId) return;

    const exists = folders.some(
      (folder) => String(folder.id) === String(activeFolderId),
    );
    if (exists) return;

    let cancelled = false;
    (async () => {
      const res = await makeAPICall(
        "GET",
        `/folders/${encodeURIComponent(activeFolderId)}`,
      );
      if (cancelled || !res) return;

      try {
        const folder = await res.json();
        if (!folder) return;

        setFolders((prevFolders) => {
          if (prevFolders.some((f) => String(f.id) === String(folder.id))) {
            return prevFolders;
          }
          return sortFoldersForSidebar([...prevFolders, folder]);
        });
      } catch (error) {
        logger.info("Failed to fetch folder metadata", {
          activeFolderId,
          error,
        });
      }
    })();

    return () => {
      cancelled = true;
    };
  }, [activeFolderId, folders]);

  const activeFolder = folders.find(
    (folder) => String(folder.id) === String(activeFolderId),
  );
  const currentTitle = activeFolder ? activeFolder.title : "";

  const moveToDoItem = (dragIndex, hoverIndex) => {
    setItems((prevItems) => {
      const updatedItems = update(prevItems, {
        $splice: [
          [dragIndex, 1],
          [hoverIndex, 0, prevItems[dragIndex]],
        ],
      });

      const updatedIds = updatedItems.map((item) => item.id);
      handleReorderItems(updatedIds);
      return updatedItems;
    });
  };

  return (
    <div id="app-container">
      <Sidebar
        folders={folders}
        isLoading={isLoadingFolders}
        activeFolderId={activeFolderId}
        onFolderClick={loadFolderItems}
        onNewFolder={handleNewFolder}
        onEditFolder={handleEditFolder}
        onToggleFolderPin={handleToggleFolderPin}
        onHomeClick={handleHomeClick}
        themeToggle={<ThemeToggle />}
      />
      <DndProvider backend={HTML5Backend}>
        <div
          className="content-wrap"
          key={isInitializing ? "loading" : activeFolderId || "landing"}
        >
          {isInitializing ? (
            <LoadingContent />
          ) : activeFolderId ? (
            <MainContent
              currentFolderTitle={currentTitle}
              items={items}
              currentFolderId={activeFolderId}
              onEditFolder={handleEditFolder}
              onDeleteFolder={handleDeleteFolder}
              onAddTodo={handleAddTodo}
              onToggleTodo={onToggleTodo}
              onDeleteToDoItem={handleDeleteToDoItem}
              onEditToDoItem={handleEditToDoItem}
              moveToDoItem={moveToDoItem}
            />
          ) : (
            <LandingContent />
          )}
        </div>
      </DndProvider>
    </div>
  );
}

export default App;

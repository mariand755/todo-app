import React from "react";
import FolderItem from "./FolderItem";
import NewFolderForm from "./NewFolderForm";

const Sidebar = ({
  folders,
  isLoading = false,
  activeFolderId,
  onFolderClick,
  onNewFolder,
  onEditFolder,
  onToggleFolderPin,
  onHomeClick,
  themeToggle,
}) => {
  const showLoadingPlaceholders = isLoading && folders.length === 0;
  const visibleFolders = showLoadingPlaceholders
    ? [
        { id: "loading-1", isLoadingPlaceholder: true },
        { id: "loading-2", isLoadingPlaceholder: true },
        { id: "loading-3", isLoadingPlaceholder: true },
      ]
    : folders;

  const handleHomeKeydown = (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      onHomeClick();
    }
  };

  return (
    <aside id="folder-sidebar">
      <div className="sidebar-header">
        <button
          id="home-button"
          className="sidebar-home-btn"
          onClick={onHomeClick}
          onKeyDown={handleHomeKeydown}
          aria-label="Go to home"
          title="Return to home"
        >
          Folders
        </button>
        {themeToggle}
      </div>
      <ul id="folder-list">
        {visibleFolders.map((folder) =>
          folder.isLoadingPlaceholder ? (
            <li
              key={folder.id}
              className="folder-item loading-placeholder"
              aria-hidden="true"
              data-testid="sidebar-loading-row"
            >
              <span className="folder-skeleton-name" />
              <span className="folder-skeleton-pin" />
            </li>
          ) : (
            <FolderItem
              key={folder.id}
              folder={folder}
              isActive={String(folder.id) === String(activeFolderId)}
              onClick={onFolderClick}
              onEdit={onEditFolder}
              onTogglePin={onToggleFolderPin}
            />
          ),
        )}

        {!showLoadingPlaceholders && (
          <FolderItem
            key="new"
            folder={{
              id: "new",
              isInput: true,
              content: <NewFolderForm onNewFolder={onNewFolder} />,
            }}
            isActive={false}
            onClick={onFolderClick}
            onEdit={onEditFolder}
            onTogglePin={onToggleFolderPin}
          />
        )}
      </ul>
    </aside>
  );
};

export default Sidebar;

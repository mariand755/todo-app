import React, { useState } from "react";

// Double-clicking a folder switches it to an inline text input for quick renaming.
// Pressing Enter or blurring the input saves the new title; Escape cancels.
const FolderItem = ({ folder, isActive, onClick, onEdit, onTogglePin }) => {
  const [isEditing, setIsEditing] = useState(false);

  if (folder.isInput) {
    return <li className="folder-item add-folder">{folder.content}</li>;
  }

  const handleClick = () => {
    onClick(folder.id);
  };

  const handleEdit = (newTitle) => {
    onEdit(folder.id, newTitle);
  };

  const isPinned = Boolean(folder.is_pinned);

  const handleTogglePin = (event) => {
    event.stopPropagation();
    if (typeof onTogglePin === "function") {
      onTogglePin(folder.id, !isPinned);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleClick();
    }
  };

  const classes = `folder-item ${isActive ? "active" : ""}`;

  return isEditing ? (
    <input
      type="text"
      defaultValue={folder.title}
      onBlur={(e) => {
        handleEdit(e.target.value);
        setIsEditing(false);
      }}
      onKeyDown={(e) => {
        if (e.key === "Enter") {
          handleEdit(e.target.value);
          setIsEditing(false);
        } else if (e.key === "Escape") {
          setIsEditing(false);
        }
      }}
      className={classes}
      autoFocus
      aria-label={`Edit folder name: ${folder.title}`}
    />
  ) : (
    <li
      className={classes}
      onClick={handleClick}
      onDoubleClick={() => setIsEditing(true)}
      onKeyDown={handleKeyDown}
      role="button"
      tabIndex="0"
      aria-pressed={isActive}
      aria-label={`${folder.title}${isPinned ? " (pinned)" : ""}${isActive ? " (active)" : ""}`}
    >
      <span
        className="folder-name"
        data-full={isPinned ? "Tap to Unpin" : "Tap to Pin"}
        title={isPinned ? "Tap to Unpin" : "Tap to Pin"}
      >
        {folder.title}
      </span>
      <button
        type="button"
        className={`folder-pin-btn ${isPinned ? "is-pinned" : ""}`}
        onClick={handleTogglePin}
        onKeyDown={(event) => event.stopPropagation()}
        aria-label={`${isPinned ? "Unpin" : "Pin"} folder ${folder.title}`}
      >
        <sl-icon name={isPinned ? "pin-angle-fill" : "pin-angle"} />
      </button>
    </li>
  );
};

export default FolderItem;

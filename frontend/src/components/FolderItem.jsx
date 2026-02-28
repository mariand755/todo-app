import React, { useState } from "react";

const FolderItem = ({ folder, isActive, onClick, onEdit }) => {
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
      onKeyDown={handleKeyDown}
      role="button"
      tabIndex="0"
      aria-pressed={isActive}
      aria-label={`${folder.title}${isActive ? " (active)" : ""}`}
    >
      <span
        className="folder-name"
        data-full={folder.title}
        title={folder.title}
      >
        {folder.title}
      </span>
    </li>
  );
};

export default FolderItem;

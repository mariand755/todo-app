// Replaces create_folder_item (part of it) and the click handler
import React, { useState } from 'react';

const FolderItem = ({ folder, isActive, onClick, onEdit, onDelete }) => {
    const [isEditing, setIsEditing] = useState(false);

    // Check for the special 'add-folder' item
    if (folder.isInput) {
        return <li className="folder-item add-folder">{folder.content}</li>;
    }

    const handleClick = () => {
        onClick(folder.id);
    };

    const handleEdit = (newTitle) => {
        onEdit(folder.id, newTitle);
    };

    const handleDelete = (e) => {
        e.stopPropagation();
        if (onDelete) onDelete(folder.id);
    };

    const classes = `folder-item ${isActive ? 'active' : ''}`;

    return isEditing ? (
        <input
            type="text"
            defaultValue={folder.title}
            onBlur={e => {
                handleEdit(e.target.value);
                setIsEditing(false);
            }}
            onKeyDown={e => {
                if (e.key === 'Enter') {
                    handleEdit(e.target.value);
                    setIsEditing(false);
                }
            }}
            className={classes}
            autoFocus
        />
    ) : (
        <li className={classes} onClick={handleClick}>
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

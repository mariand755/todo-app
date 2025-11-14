// Replaces create_folder_item (part of it) and the click handler
import React from 'react';

const FolderItem = ({ folder, isActive, onClick }) => {
    // Check for the special 'add-folder' item from the original HTML
    if (folder.isInput) {
        return <li className="folder-item add-folder">{folder.content}</li>;
    }

    const handleClick = () => {
        onClick(folder.id);
    };

    // The logic to add the 'active' class is now handled by a prop check
    const classes = `folder-item ${isActive ? 'active' : ''}`;

    return (
        <li id={`folder_id_${folder.id}`} className={classes} onClick={handleClick}>
            <span className="folder-name">{folder.title}</span>
            {/* You'd need to fetch item count if you want to display it */}
            {/* <span className="item-count">{folder.itemCount || 0}</span> */}
        </li>
    );
};

export default FolderItem;
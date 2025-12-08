// Replaces create_folder_item (part of it) and the click handler
import React, {useState} from 'react';

const FolderItem = ({ folder, isActive, onClick}) => {
    const [isEditing, setIsEditing] = useState(false);

    // Check for the special 'add-folder' item from the original HTML
    if (folder.isInput) {
        return <li className="folder-item add-folder">{folder.content}</li>;
    }
    const handleClick = () => {
        onClick(folder.id);
    };
    // The logic to add the 'active' class is now handled by a prop check
    const classes = `folder-item ${isActive ? 'active' : ''}`;

    return isEditing ? (
        // ...existing edit input code...
        null
    ) : (
        // add data-full and title for tooltip and make focusable for keyboard users
        <span
            className={`folder-name ${classes}`}
            onClick={handleClick}
            onKeyDown={e => { if (e.key === 'Enter') handleClick(); }}
            data-full={folder.title}
            title={folder.title}
            tabIndex={0}
            aria-label={folder.title}
        >
            {folder.title}
        </span>
    );
};  
export default FolderItem;
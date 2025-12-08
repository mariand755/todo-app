// Replaces create_folder_item (part of it) and the click handler
import React, {useState} from 'react';

const FolderItem = ({ folder, isActive, onClick}) => {
    // Check for the special 'add-folder' item from the original HTML
    if (folder.isInput) {
        return <li className="folder-item add-folder">{folder.content}</li>;
    }
    const handleClick = () => {
        onClick(folder.id);
    };
    // The logic to add the 'active' class is now handled by a prop check
    const classes = `folder-item ${isActive ? 'active' : ''}`;
    return    <span className={`folder-name ${classes}`} onClick={handleClick}>{folder.title}</span> 
};  
export default FolderItem;
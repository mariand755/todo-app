import React from 'react';
import FolderItem from './FolderItem';
import NewFolderForm from './NewFolderForm'; // Defined below

const Sidebar = ({ folders, activeFolderId, onFolderClick, onNewFolder, onEditFolder, onHomeClick }) => {
    
    // Combine fetched folders with the static 'Add New Folder' input from index.html
    const listItems = [
        ...folders,
        { 
            id: 'new', 
            isInput: true, 
            content: <NewFolderForm onNewFolder={onNewFolder} /> 
        }
    ];

    return (
        <aside id="folder-sidebar">
            <h2 onClick={onHomeClick}>Folders</h2>
            <ul id="folder-list">
                {listItems.map((folder) => (
                    <FolderItem
                        key={folder.id}
                        folder={folder}
                        isActive={String(folder.id) === String(activeFolderId)}
                        onClick={onFolderClick}
                        onEdit={onEditFolder}
                    />
                ))}
            </ul>
        </aside>
    );
};

export default Sidebar;
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

    const handleHomeKeydown = (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            onHomeClick();
        }
    };

    return (
        <aside id="folder-sidebar">
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

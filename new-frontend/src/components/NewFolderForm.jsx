// Replaces input_new_folder_title() and enter_new_folder_tiltle_option()
import React, { useState } from 'react';

const NewFolderForm = ({ onNewFolder }) => {
    const [title, setTitle] = useState('');

    const handleSubmit = () => {
        if (title.trim()) {
            onNewFolder(title.trim());
            setTitle(''); // Clear input after submission
        }
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleSubmit();
        }
    };

    // Shoelace components are used in the original index.html, 
    // but here we use standard React input for simplicity unless a Shoelace React wrapper is used.
    // If you need Shoelace, you'll install the React wrapper or ensure the scripts load globally.

    return (
        <>
            <input 
                id="new-folder-input" 
                type="text" 
                placeholder="Add New Folder" 
                value={title} 
                onChange={(e) => setTitle(e.target.value)}
                onKeyUp={handleKeyPress}
            />
            <button 
                id="add-folder-btn" 
                onClick={handleSubmit}
            >
                +
            </button>
            {/* The Shoelace icon/button would need the Shoelace component or custom styling */}
        </>
    );
};

export default NewFolderForm;
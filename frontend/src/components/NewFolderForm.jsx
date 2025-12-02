// Replaces input_new_folder_title() and enter_new_folder_tiltle_option()
import React, { useState } from 'react';
import SlButton from '@shoelace-style/shoelace/dist/react/button/index.js';
import SlInput from '@shoelace-style/shoelace/dist/react/input/index.js';
import SlIcon from '@shoelace-style/shoelace/dist/react/icon/index.js';


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

    return (
        <>
            {/* Keep elements directly inside the li.add-folder so current CSS applies */}
            <SlInput 
                id="new-folder-input" 
                type="text" 
                placeholder="Add New Folder" 
                value={title} 
                onSlInput={(e) => setTitle(e.target.value)}
                onKeyUp={handleKeyPress}
                size="medium"
            />
            <SlButton 
                id="add-folder-btn" 
                variant="primary"
                onClick={handleSubmit}
                size="medium"
                title="Create folder"
            >
                <SlIcon name="folder-plus" style={{ fontSize: '1.2rem' }} />
            </SlButton>
        </>
    );
};

export default NewFolderForm;
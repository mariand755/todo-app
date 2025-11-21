import React, { useState, useEffect } from 'react';
import { makeAPICall } from './useApi'; 
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';
import './styles.css'; 
import '@shoelace-style/shoelace/dist/themes/light.css';
import { setBasePath } from '@shoelace-style/shoelace/dist/utilities/base-path.js';
setBasePath('https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.20.1/cdn/');


function App() {
    const [folders, setFolders] = useState([]);
    const [items, setItems] = useState([]);
    const [activeFolderId, setActiveFolderId] = useState(null);

    // useEffect hook replaces the initial IIFE logic from script.js
    useEffect(() => {
        // Fetch all folders on initial load
        const fetchFolders = async () => {
            const data = await makeAPICall("GET", "/folders");
            if (data) {
                const folders = await data.json();
                setFolders(folders);
                // The original script.js had commented-out logic to load the first folder's items, 
                // but let's just initialize state here.
                if (folders.length > 0) {
                    // setActiveFolderId(folders[0].id);
                    // loadFolderItems(data[0].id);
                }
            }
        };
        fetchFolders();
    }, []); // Empty dependency array ensures it runs once on mount

    // Logic for loading items, replacing show_folder_items()
    const loadFolderItems = async (folderId) => {
        if (folderId === activeFolderId) {
            return; // No need to reload the same folder
        }
        const data = await makeAPICall("GET", `/folders/${folderId}/items/`);
        if (data) {
            const folders = await data.json();
            setItems(folders);
            setActiveFolderId(folderId);
        }
    };

    // Logic for adding a new folder, replacing input_new_folder_title()
    const handleNewFolder = async (title) => {
        const rawApiResponse = await makeAPICall("POST", "/folders", { title });
        if (rawApiResponse) {
            const newFolder = await rawApiResponse.json();
            // Update state immutably: new folder added to the list
            setFolders(prevFolders => {
                // Find the index of the 'Add New Folder' input item (the last one)
                const addFolderIndex = prevFolders.findIndex(f => f.isInput);
                if (addFolderIndex !== -1) {
                    // Insert the new folder before the input item, mimicking folder_list.insertBefore
                    const updatedFolders = [...prevFolders];
                    updatedFolders.splice(addFolderIndex, 0, newFolder);
                    return updatedFolders;
                }
                return [...prevFolders, newFolder];
            });
        }
    };
    // Logic for editing a folder title, replacing edit_folder_title()
    const handleEditFolder = async (folderId, newTitle) => {
        const rawApiResponse = await makeAPICall("PUT", `/folders/${folderId}`, { title: newTitle });
        if (rawApiResponse) {
            const updatedFolder = await rawApiResponse.json();
            setFolders(prevFolders => 
                prevFolders.map(folder => {
                    if (folder.id === folderId) {
                        return updatedFolder;
                    }
                    return folder;
                })
            );
        }
    };

    // Determine the title to display
    const activeFolder = folders.find(f => f.id === activeFolderId);
    const currentTitle = activeFolder ? activeFolder.title : "Select a Folder";

    return (
        <div id="app-container">
            <Sidebar 
                folders={folders} 
                activeFolderId={activeFolderId} 
                onFolderClick={loadFolderItems}
                onNewFolder={handleNewFolder}
                onEditFolder={handleEditFolder}
            />
            <MainContent 
                currentFolderTitle={currentTitle} 
                items={items} 
                // Placeholder for item actions (add, toggle, delete)
            />
        </div>
    );
}

export default App;
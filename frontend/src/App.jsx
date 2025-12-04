import React, { useState, useEffect } from 'react';
import { makeAPICall } from './useApi'; 
import Sidebar from './components/Sidebar';
import MainContent from './components/MainContent';
import LandingContent from './components/LandingContent';
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

    const handleDeleteFolder = async (folderId) => {
        const rawApiResponse = await makeAPICall("DELETE", `/folders/${folderId}`);
        if (rawApiResponse) {
            setFolders(prevFolders => prevFolders.filter(folder => folder.id !== folderId));
            if (folderId === activeFolderId) {
                setActiveFolderId(null);
                setItems([]);
            }
        }
    };
    // Logic for handling home click to show landing content
    const handleHomeClick = () => {
        setActiveFolderId(null);
        setItems([]);
    };
    // Logic for handling adding a new todo item
    const handleAddTodo = async (title) => {
        const rawApiResponse = await makeAPICall("POST", `/folders/${activeFolderId}/items/`, { title });
        if (rawApiResponse) {
            const newItem = await rawApiResponse.json();
            setItems(prevItems => [...prevItems, newItem]);
        }
    };
    // Logic for handling toggling a todo item
    const onToggleTodo = async (itemId) => {
        setItems(prevItems => {
            return prevItems.map(item => {
                if (item.id === itemId) {
                    return { ...item, completed: !item.completed };
                }
                return item;
            });
        });

    //     const rawApiResponse = await makeAPICall("PUT", `/folders/${activeFolderId}/items/${itemId}/toggle`);
    //     if (rawApiResponse) {
    //         const updatedItem = await rawApiResponse.json();
    //         setItems(prevItems => 
    //             prevItems.map(item => {
    //                 if (item.id === itemId) {
    //                     return updatedItem;
    //                 }
    //                 return item;
    //             })
    //         );
    //     }
    };
    // Logic for handling deleting a todo item
    const handleDeleteToDoItem = async (itemId) => {
        const rawApiResponse = await makeAPICall("DELETE", `/folders/${activeFolderId}/items/${itemId}`);
        if (rawApiResponse) {
            setItems(prevItems => prevItems.filter(item => item.id !== itemId));
        }
    };
    // Logic for handling editing a todo item
    const handleEditToDoItem = async (itemId, newTitle) => {
        const rawApiResponse = await makeAPICall("PUT", `/folders/${activeFolderId}/items/${itemId}`, { title: newTitle });
        if (rawApiResponse) {
            const updatedItem = await rawApiResponse.json();
            setItems(prevItems => 
                prevItems.map(item => {
                    if (item.id === itemId) {
                        return updatedItem;
                    }
                    return item;
                })
            );
        }
    };

    // Determine the title to display
    const activeFolder = folders.find(f => f.id === activeFolderId);
    const currentTitle = activeFolder ? activeFolder.title : "";

    return (
        <div id="app-container">
            <Sidebar 
                folders={folders} 
                activeFolderId={activeFolderId} 
                onFolderClick={loadFolderItems}
                onNewFolder={handleNewFolder}
                onEditFolder={handleEditFolder}
                onHomeClick={handleHomeClick}
            />
            {activeFolderId ? <MainContent  
                currentFolderTitle={currentTitle} 
                items={items}
                currentFolderId={activeFolderId}
                onEditFolder={handleEditFolder}
                onDeleteFolder={handleDeleteFolder}  
                onAddTodo={handleAddTodo}
                onToggleTodo={onToggleTodo}
                onDeleteToDoItem={handleDeleteToDoItem}
                onEditToDoItem={handleEditToDoItem}
            />
            : <LandingContent/>}
        </div>
    );
}

export default App;
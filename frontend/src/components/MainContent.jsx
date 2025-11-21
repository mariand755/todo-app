import React, {useState} from 'react';
import TodoItem from './TodoItem.jsx';
import SlIcon from '@shoelace-style/shoelace/dist/react/icon/index.js';
import SlMenu from '@shoelace-style/shoelace/dist/react/menu/index.js';
import SlDivider from '@shoelace-style/shoelace/dist/react/divider/index.js';
import SlMenuItem from '@shoelace-style/shoelace/dist/react/menu-item/index.js';
import SlDropdown from '@shoelace-style/shoelace/dist/react/dropdown/index.js';
import SlDialog from '@shoelace-style/shoelace/dist/react/dialog/index.js';
import SlButton from '@shoelace-style/shoelace/dist/react/button/index.js';

const MainContent = ({ currentFolderTitle, items }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [openDialog, setOpenDialog] = useState(false);
    const [deleteDialog, setDeleteDialog] = useState(false);


    return (
        <main id="todo-main-content">
            <header>
                <h1 id="current-folder-title">{currentFolderTitle} 
                <SlDropdown
                // Bind the open state to our React state
                open={isOpen}
                // Open when mouse enters the entire component area
                onMouseEnter={() => setIsOpen(true)}
                // Close when mouse leaves the entire component area
                onMouseLeave={() => setIsOpen(false)}
                >  

                  <SlIcon slot="trigger" name="three-dots-vertical"></SlIcon>
                  <SlMenu style={{ maxWidth: '200px' }}>
                  <SlMenuItem value="edit" onClick={() => setOpenDialog(true)}>Edit</SlMenuItem>
                  <SlDivider/>
                  <SlMenuItem value="delete" onClick={() => setDeleteDialog(true)}>Delete</SlMenuItem>
                  </SlMenu> 
                </SlDropdown>
                <SlDialog label="Edit Folder Name" open={openDialog} onSlAfterHide={() => setOpenDialog(false)}>
                <SlButton slot="footer" variant="primary" onClick={() => setOpenDialog(false)}>
                Close
                </SlButton>
                </SlDialog>
                <SlDialog label="Delete Folder" open={deleteDialog} onSlAfterHide={() => setDeleteDialog(false)}>
                <SlButton slot="footer" variant="primary" onClick={() => setDeleteDialog(false)}>
                Close
                </SlButton>
                </SlDialog>



                </h1>
                <div className="actions">
                    <input type="text" id="new-todo-input" placeholder="What needs to be added?" />
                    <button id="add-todo-btn">Add Items</button>
                </div>
            </header>

            <ul id="todo-list">
                {/* Dynamically render the list of items based on state */}
                {items.length === 0 ? (
                    <p>No items in this folder.</p>
                ) : (
                    items.map((item) => (
                        <TodoItem 
                            key={item.id} 
                            item={item}
                            // Pass action handlers here later
                        />
                    ))
                )}
            </ul>
        </main>
    );
};

export default MainContent;
// Replaces the HTML string generation in create_folder_item_list()
import React from 'react';
import SlIcon from '@shoelace-style/shoelace/dist/react/icon/index.js';
import SlMenu from '@shoelace-style/shoelace/dist/react/menu/index.js';
import SlDivider from '@shoelace-style/shoelace/dist/react/divider/index.js';
import SlMenuItem from '@shoelace-style/shoelace/dist/react/menu-item/index.js';
import SlDropdown from '@shoelace-style/shoelace/dist/react/dropdown/index.js';
import SlDialog from '@shoelace-style/shoelace/dist/react/dialog/index.js';
import SlButton from '@shoelace-style/shoelace/dist/react/button/index.js';
import SlInput from '@shoelace-style/shoelace/dist/react/input/index.js';
import { useState } from 'react';   

const TodoItem = ({item, onToggle, onDeleteToDoItem, onEditToDoItem}) => {
    const [isOpen, setIsOpen] = useState(false);
    const [openDialog, setOpenDialog] = useState(false);
    const [deleteDialog, setDeleteDialog] = useState(false);

    // Placeholder for item actions
    const handleToggle = () => {
         onToggle(item.id);
    };

    const handleDelete = () => { onDeleteToDoItem(item.id); };
    const handleEdit = (newTitle) => { onEditToDoItem(item.id, newTitle); };

    const classes = `todo-item ${item.completed ? 'complete' : ''}`;

    return (

        <li className={classes}>
            <input 
                type="checkbox" 
                checked={item.completed} 
                onChange={handleToggle} 
            />
            <span className="todo-text">{item.title}</span>
        
            <div className="item-actions">
                {item && (
                    <div className="folder-actions">
                        <SlDropdown  
                            open={isOpen}
                            onMouseEnter={() => setIsOpen(true)}
                            onMouseLeave={() => setIsOpen(false)}
                            >
                                    <SlIcon slot="trigger" name="three-dots-vertical"></SlIcon>
                                    <SlMenu style={{ maxWidth: '200px' }}>
                                        <SlMenuItem value="edit" onClick={() => setOpenDialog(true)}>Edit</SlMenuItem>
                                        <SlDivider/>
                                        <SlMenuItem value="delete" onClick={() => setDeleteDialog(true)}>Delete</SlMenuItem>
                                    </SlMenu>
                                </SlDropdown>
                            </div>
                            )
                            }
                        </div>
        
                        <SlDialog label="Edit Item Name" open={openDialog} onSlAfterHide={() => setOpenDialog(false)}>
                            <SlButton slot="footer" variant="primary" onClick={(e) => 
                            {
                                const inputElement = document.getElementById(`edit-${item.id}-input`);
                                handleEdit(inputElement.value); 
                                setOpenDialog(false); 
                            }}>
                                OK
                            </SlButton>
        
                            <SlInput id={`edit-${item.id}-input`} 
                                onKeyDown={e => {
                                if (e.key === 'Enter') {
                                    handleEdit(e.target.value);     
                                    setOpenDialog(false);}
                                }}
                                size="medium" value={item.title} pill/>
                        </SlDialog>
        
                        <SlDialog label={`Delete "${item.title}"?`} open={deleteDialog} onSlAfterHide={() => setDeleteDialog(false)}>
                            <SlButton slot="footer" variant="primary" onClick={(e) => { handleDelete(); setDeleteDialog(false); }}>
                                OK
                            </SlButton>
                        </SlDialog>
        
        </li>
        
    );

};

export default TodoItem;
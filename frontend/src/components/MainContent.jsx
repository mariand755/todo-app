import React, {useState} from 'react';
import TodoItem from './TodoItem.jsx';
import SlIcon from '@shoelace-style/shoelace/dist/react/icon/index.js';
import SlMenu from '@shoelace-style/shoelace/dist/react/menu/index.js';
import SlDivider from '@shoelace-style/shoelace/dist/react/divider/index.js';
import SlMenuItem from '@shoelace-style/shoelace/dist/react/menu-item/index.js';
import SlDropdown from '@shoelace-style/shoelace/dist/react/dropdown/index.js';
import SlDialog from '@shoelace-style/shoelace/dist/react/dialog/index.js';
import SlButton from '@shoelace-style/shoelace/dist/react/button/index.js';
import SlInput from '@shoelace-style/shoelace/dist/react/input/index.js';


const MainContent = ({ currentFolderTitle, currentFolderId, items, onEditFolder, onDeleteFolder, onAddTodo, onToggleTodo, onDeleteTodo, onEditTodo }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [openDialog, setOpenDialog] = useState(false);
    const [deleteDialog, setDeleteDialog] = useState(false);

    // new local state for the todo input
    const [newTodo, setNewTodo] = useState('');

    const handleEdit = (newTitle) => {
        onEditFolder(currentFolderId, newTitle);
    };

    const handleDelete = () => {
        onDeleteFolder(currentFolderId);
    };

    // handle form submit (Enter or click)
    const handleAddTodo = (e) => {
        e.preventDefault();
        const trimmed = newTodo.trim();
        if (!trimmed) return;
        if (typeof onAddTodo === 'function') {
            onAddTodo(trimmed);
        } 
        setNewTodo('');
    };

    return (
        <main id="todo-main-content">
            <header>
                <div className="folder-header">
                    <h1 id="current-folder-title">{currentFolderTitle}</h1>

                    {
                       currentFolderId && (
                       <div className="folder-controls">
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

                <SlDialog label="Edit Folder Name" open={openDialog} onSlAfterHide={() => setOpenDialog(false)}>
                    <SlButton slot="footer" variant="primary" onClick={(e) => 
                    {
                        const inputElement = document.getElementById('edit-folder-input');
                        handleEdit(inputElement.value); 
                        setOpenDialog(false); 
                    }}>
                        OK
                    </SlButton>

                    <SlInput id="edit-folder-input" 
                        onKeyDown={e => {
                        if (e.key === 'Enter') {
                            handleEdit(e.target.value);     
                            setOpenDialog(false);}
                        }}
                        size="medium" value={currentFolderTitle} pill/>
                </SlDialog>

                <SlDialog label={`Delete "${currentFolderTitle}"?`} open={deleteDialog} onSlAfterHide={() => setDeleteDialog(false)}>
                    <SlButton slot="footer" variant="primary" onClick={(e) => { handleDelete(); setDeleteDialog(false); }}>
                        OK
                    </SlButton>
                </SlDialog>

                <form className="actions" onSubmit={handleAddTodo}>
                    <input
                        type="text"
                        id="new-todo-input"
                        placeholder="What needs to be added?"
                        value={newTodo}
                        onChange={e => setNewTodo(e.target.value)}
                        aria-label="New todo"
                    />
                    <button id="add-todo-btn" type="submit">Add Items</button>
                </form>
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
                            onToggle={onToggleTodo}
                            onDelete={onDeleteTodo}
                            onEdit={onEditTodo}
                        />
                    ))
                )}
            </ul>
        </main>
    );
};

export default MainContent;
import React, {useState, useCallback} from 'react';
import TodoItem from './TodoItem.jsx';
import SlIcon from '@shoelace-style/shoelace/dist/react/icon/index.js';
import SlMenu from '@shoelace-style/shoelace/dist/react/menu/index.js';
import SlDivider from '@shoelace-style/shoelace/dist/react/divider/index.js';
import SlMenuItem from '@shoelace-style/shoelace/dist/react/menu-item/index.js';
import SlDropdown from '@shoelace-style/shoelace/dist/react/dropdown/index.js';
import SlDialog from '@shoelace-style/shoelace/dist/react/dialog/index.js';
import SlButton from '@shoelace-style/shoelace/dist/react/button/index.js';
import SlInput from '@shoelace-style/shoelace/dist/react/input/index.js';


const MainContent = ({ currentFolderTitle, currentFolderId, items, onEditFolder, onDeleteFolder,
    onAddTodo, onToggleTodo, onDeleteToDoItem, onEditToDoItem, moveToDoItem}) => {
    const [openDialog, setOpenDialog] = useState(false);
    const [deleteDialog, setDeleteDialog] = useState(false);

    const [newTodo, setNewTodo] = useState('');

    const handleEdit = (newTitle) => {
        onEditFolder(currentFolderId, newTitle);
    };

    const handleDelete = () => {
        onDeleteFolder(currentFolderId);
    };

    const handleAddTodo = (e) => {
        e.preventDefault();
        const trimmed = newTodo.trim();
        if (!trimmed) return;
        if (typeof onAddTodo === 'function') {
            onAddTodo(trimmed);
        }
        setNewTodo('');
    };

    const renderToDoItem = useCallback((item, index) => {
      return (
        <TodoItem
            key={item.id}
            item={item}
            index={index}
            onToggle={onToggleTodo}
            onDeleteToDoItem={onDeleteToDoItem}
            onEditToDoItem={onEditToDoItem}
            moveToDoItem={moveToDoItem}
        />
      )
    }, [])

    return (
        <main id="todo-main-content">
            <header>
                <div className="folder-header">
                    <h1 id="current-folder-title">{currentFolderTitle}</h1>

                    {
                       currentFolderId && (
                       <div className="folder-controls">
                        <SlDropdown
                            hoist
                        >
                            <button
                                type="button"
                                className="folder-menu-button"
                                slot="trigger"
                                aria-label="Folder options menu"
                                aria-haspopup="menu"
                                title="Folder options"
                            >
                                <SlIcon 
                                    className="folder-menu-trigger"
                                    name="three-dots-vertical"
                                ></SlIcon>
                            </button>
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

                <SlDialog 
                    label="Edit Folder Name" 
                    open={openDialog} 
                    onSlAfterHide={() => setOpenDialog(false)}
                    aria-labelledby="edit-folder-dialog-title"
                >
                    <h2 id="edit-folder-dialog-title" className="sr-only">Edit Folder Name</h2>
                    <SlInput 
                        id="edit-folder-input"
                        aria-label="New folder name"
                        onKeyDown={e => {
                            if (e.key === 'Enter') {
                                handleEdit(e.target.value);
                                setOpenDialog(false);
                            } else if (e.key === 'Escape') {
                                setOpenDialog(false);
                            }
                        }}
                        size="medium" 
                        value={currentFolderTitle} 
                        pill
                    />
                    <SlButton 
                        slot="footer" 
                        variant="primary" 
                        onClick={(e) => {
                            const inputElement = document.getElementById('edit-folder-input');
                            handleEdit(inputElement.value);
                            setOpenDialog(false);
                        }}
                    >
                        OK
                    </SlButton>
                </SlDialog>

                <SlDialog 
                    label={`Delete "${currentFolderTitle}"?`} 
                    open={deleteDialog} 
                    onSlAfterHide={() => setDeleteDialog(false)}
                    aria-labelledby="delete-folder-dialog-title"
                >
                    <h2 id="delete-folder-dialog-title" className="sr-only">Delete folder confirmation</h2>
                    <SlButton 
                        slot="footer" 
                        variant="primary" 
                        onClick={(e) => { handleDelete(); setDeleteDialog(false); }}
                    >
                        OK
                    </SlButton>
                </SlDialog>

                <form className="actions" onSubmit={handleAddTodo} autoComplete="off">
                    <label htmlFor="new-todo-input" className="sr-only">New todo item</label>
                    <input
                        type="text"
                        id="new-todo-input"
                        placeholder="What needs to be added?"
                        value={newTodo}
                        onChange={e => setNewTodo(e.target.value)}
                        autoComplete="off"
                        autoCorrect="off"
                        autoCapitalize="off"
                        spellCheck={false}
                        aria-label="New todo item"
                    />
                    <button id="add-todo-btn" type="submit" aria-label="Add items">Add Items</button>
                </form>
            </header>

            <ul id="todo-list">
                {items.length === 0 ? (
                    <p>No items in this folder.</p>
                ) : (
                    items.map((item, index) => renderToDoItem(item, index))
                )}
            </ul>
        </main>
    );
};

export default MainContent;

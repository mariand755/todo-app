// Replaces the HTML string generation in create_folder_item_list()
import React from 'react';

const TodoItem = ({item, onToggle, onDelete, onEdit}) => {
    // Placeholder for item actions
    const handleToggle = () => {
         onToggle(item.id);
    };

    const handleDelete = () => { onDelete(item.id); };
    const handleEdit = (newTitle) => { onEdit(item.id, newTitle); };

    const classes = `todo-item ${item.completed ? 'complete' : ''}`;

    return (
        <li className={classes}>
            <input 
                type="checkbox" 
                checked={item.completed} 
                onChange={handleToggle} 
            />
            <span className="todo-text">{item.title}</span>
            <button className="delete-btn" onClick={handleDelete}>Delete</button>
        </li>
    );
};

export default TodoItem;
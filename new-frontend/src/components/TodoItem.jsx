// Replaces the HTML string generation in create_folder_item_list()
import React from 'react';

const TodoItem = ({ item }) => {
    // Placeholder for item actions
    const handleToggle = () => { /* Logic to toggle 'complete' state via prop function */ };
    const handleDelete = () => { /* Logic to delete item via prop function */ };

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
import React from 'react';
import TodoItem from './TodoItem.jsx';

const MainContent = ({ currentFolderTitle, items }) => {
    return (
        <main id="todo-main-content">
            <header>
                <h1 id="current-folder-title">{currentFolderTitle}</h1>
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
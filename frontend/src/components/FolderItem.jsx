// Replaces create_folder_item (part of it) and the click handler
import React, {useState} from 'react';

const FolderItem = ({ folder, isActive, onClick, onEdit }) => {
    const [isEditing, setIsEditing] = useState(false);
    // Check for the special 'add-folder' item from the original HTML
    if (folder.isInput) {
        return <li className="folder-item add-folder">{folder.content}</li>;
    }

    const handleClick = () => {
        onClick(folder.id);
        setIsEditing(previous => {
            console.log(previous)
            return !previous
        })
    }
    const handleEdit = (newTitle) => {
        onEdit(folder.id, newTitle);
    };

    // The logic to add the 'active' class is now handled by a prop check
    const classes = `folder-item ${isActive ? 'active' : ''}`;

    return isEditing ? (
        <input
            type="text"
            defaultValue={folder.title}
            onBlur={e => {
                handleEdit(e.target.value);
                setIsEditing(false);
            }}
            onKeyDown={e => {
                if (e.key === 'Enter') {
                    handleEdit(e.target.value);
                    setIsEditing(false);
                }
            }}
            className={classes}
            autoFocus
        />
    ) : (
        <span className={`folder-name ${classes}`} onClick={handleClick}>{folder.title}</span>
    );
}
export default FolderItem;
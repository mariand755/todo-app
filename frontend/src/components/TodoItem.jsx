// Replaces the HTML string generation in create_folder_item_list()
import React, {useState, useRef} from 'react';
import { useDrag, useDrop } from 'react-dnd';
import SlIcon from '@shoelace-style/shoelace/dist/react/icon/index.js';
import SlMenu from '@shoelace-style/shoelace/dist/react/menu/index.js';
import SlDivider from '@shoelace-style/shoelace/dist/react/divider/index.js';
import SlMenuItem from '@shoelace-style/shoelace/dist/react/menu-item/index.js';
import SlDropdown from '@shoelace-style/shoelace/dist/react/dropdown/index.js';
import SlDialog from '@shoelace-style/shoelace/dist/react/dialog/index.js';
import SlButton from '@shoelace-style/shoelace/dist/react/button/index.js';
import SlInput from '@shoelace-style/shoelace/dist/react/input/index.js';

// Define ItemTypes for drag-and-drop
export const ItemTypes = {
  CARD: 'card'
}


const TodoItem = ({item, onToggle, onDeleteToDoItem, onEditToDoItem, moveToDoItem, index}) => {
    const ref = useRef(null)
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

    // Drag and drop setup
    const [{ handlerId }, drop] = useDrop({
    accept: ItemTypes.CARD,
    collect(monitor) {
      return {
        handlerId: monitor.getHandlerId(),
      }
    },
    hover(item, monitor) {
      if (!ref.current) {
        return
      }
      const dragIndex = item.index
      const hoverIndex = index
      // Don't replace items with themselves
      if (dragIndex === hoverIndex) {
        return
      }
      // Determine rectangle on screen
      const hoverBoundingRect = ref.current?.getBoundingClientRect()
      // Get vertical middle
      const hoverMiddleY =
        (hoverBoundingRect.bottom - hoverBoundingRect.top) / 2
      // Determine mouse position
      const clientOffset = monitor.getClientOffset()
      // Get pixels to the top
      const hoverClientY = clientOffset.y - hoverBoundingRect.top
      // Only perform the move when the mouse has crossed half of the items height
      // When dragging downwards, only move when the cursor is below 50%
      // When dragging upwards, only move when the cursor is above 50%
      // Dragging downwards
      if (dragIndex < hoverIndex && hoverClientY < hoverMiddleY) {
        return
      }
      // Dragging upwards
      if (dragIndex > hoverIndex && hoverClientY > hoverMiddleY) {
        return
      }
      // Time to actually perform the action
      moveToDoItem(dragIndex, hoverIndex)
      // Note: we're mutating the monitor item here!
      // Generally it's better to avoid mutations,
      // but it's good here for the sake of performance
      // to avoid expensive index searches.
      item.index = hoverIndex
    },
  })
  // Set up drag source
    const [{ isDragging }, drag] = useDrag({
    type: ItemTypes.CARD,
    item: () => {
      return { id: item.id, index }
    },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  })
  const opacity = isDragging ? 0 : 1
  drag(drop(ref))

    return (

        <li className={classes} ref={ref} style={{opacity}} data-handler-id={handlerId}>
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
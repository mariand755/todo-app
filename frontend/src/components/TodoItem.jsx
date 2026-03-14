import React, { useState, useRef } from "react";
import { useDrag, useDrop } from "react-dnd";
import SlIcon from "@shoelace-style/shoelace/dist/react/icon/index.js";
import SlMenu from "@shoelace-style/shoelace/dist/react/menu/index.js";
import SlDivider from "@shoelace-style/shoelace/dist/react/divider/index.js";
import SlMenuItem from "@shoelace-style/shoelace/dist/react/menu-item/index.js";
import SlDropdown from "@shoelace-style/shoelace/dist/react/dropdown/index.js";
import SlDialog from "@shoelace-style/shoelace/dist/react/dialog/index.js";
import SlButton from "@shoelace-style/shoelace/dist/react/button/index.js";
import SlInput from "@shoelace-style/shoelace/dist/react/input/index.js";

const ItemTypes = {
  CARD: "card",
};

const TodoItem = ({
  item,
  onToggle,
  onDeleteToDoItem,
  onEditToDoItem,
  moveToDoItem,
  index,
}) => {
  const ref = useRef(null);
  const deleteConfirmRef = useRef(null);
  const [isOpen, setIsOpen] = useState(false);
  const [openDialog, setOpenDialog] = useState(false);
  const [deleteDialog, setDeleteDialog] = useState(false);

  React.useEffect(() => {
    if (!deleteDialog) return;
    requestAnimationFrame(() => {
      deleteConfirmRef.current?.focus();
    });
  }, [deleteDialog]);

  const handleToggle = () => {
    onToggle(item.id);
  };

  const handleDelete = () => {
    onDeleteToDoItem(item.id);
  };
  const handleEdit = (newTitle) => {
    onEditToDoItem(item.id, newTitle);
  };

  const classes = `todo-item ${item.completed ? "complete" : ""} ${isOpen ? "menu-open" : ""}`;

  const [{ handlerId }, drop] = useDrop({
    accept: ItemTypes.CARD,
    collect(monitor) {
      return {
        handlerId: monitor.getHandlerId(),
      };
    },
    hover(item, monitor) {
      if (!ref.current) {
        return;
      }
      const dragIndex = item.index;
      const hoverIndex = index;
      if (dragIndex === hoverIndex) {
        return;
      }
      const hoverBoundingRect = ref.current?.getBoundingClientRect();
      const hoverMiddleY =
        (hoverBoundingRect.bottom - hoverBoundingRect.top) / 2;
      const clientOffset = monitor.getClientOffset();
      const hoverClientY = clientOffset.y - hoverBoundingRect.top;
      if (dragIndex < hoverIndex && hoverClientY < hoverMiddleY) {
        return;
      }
      if (dragIndex > hoverIndex && hoverClientY > hoverMiddleY) {
        return;
      }
      moveToDoItem(dragIndex, hoverIndex);
      item.index = hoverIndex;
    },
  });
  const [{ isDragging }, drag] = useDrag({
    type: ItemTypes.CARD,
    item: () => {
      return { id: item.id, index };
    },
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });
  const opacity = isDragging ? 0 : 1;
  drag(drop(ref));

  return (
    <li
      className={classes}
      ref={ref}
      style={{ opacity }}
      data-handler-id={handlerId}
    >
      <input
        type="checkbox"
        checked={item.completed}
        onChange={handleToggle}
        aria-label={`${item.completed ? "Mark as incomplete" : "Mark as complete"}: ${item.title}`}
      />
      <span className="todo-text">{item.title}</span>

      <div className="todo-item-actions">
        {item && (
          <SlDropdown
            className="todo-item-dropdown"
            placement="bottom-end"
            hoist
            onSlShow={() => setIsOpen(true)}
            onSlHide={() => setIsOpen(false)}
          >
            <button
              type="button"
              className="todo-item-menu-button"
              slot="trigger"
              aria-label={`Options for: ${item.title}`}
              aria-haspopup="menu"
              aria-expanded={isOpen}
              title="Item options"
            >
              <SlIcon
                className="todo-item-menu-trigger"
                name="three-dots-vertical"
              ></SlIcon>
            </button>
            <SlMenu style={{ maxWidth: "200px" }}>
              {!item.completed && (
                <>
                  <SlMenuItem value="edit" onClick={() => setOpenDialog(true)}>
                    Edit
                  </SlMenuItem>
                  <SlDivider />
                </>
              )}
              <SlMenuItem value="delete" onClick={() => setDeleteDialog(true)}>
                Delete
              </SlMenuItem>
            </SlMenu>
          </SlDropdown>
        )}
      </div>

      <SlDialog
        label="Edit Item Name"
        open={openDialog}
        onSlAfterHide={() => setOpenDialog(false)}
        aria-labelledby={`edit-item-dialog-title-${item.id}`}
      >
        <h2 id={`edit-item-dialog-title-${item.id}`} className="sr-only">
          Edit item name
        </h2>
        <SlInput
          id={`edit-${item.id}-input`}
          aria-label="New item name"
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              handleEdit(e.target.value);
              setOpenDialog(false);
            } else if (e.key === "Escape") {
              setOpenDialog(false);
            }
          }}
          size="medium"
          value={item.title}
          pill
        />
        <SlButton
          slot="footer"
          variant="primary"
          onClick={() => {
            const inputElement = document.getElementById(
              `edit-${item.id}-input`,
            );
            handleEdit(inputElement.value);
            setOpenDialog(false);
          }}
        >
          OK
        </SlButton>
      </SlDialog>

      <SlDialog
        label={`Delete "${item.title}"?`}
        open={deleteDialog}
        onSlAfterHide={() => setDeleteDialog(false)}
        aria-labelledby={`delete-item-dialog-title-${item.id}`}
      >
        <h2 id={`delete-item-dialog-title-${item.id}`} className="sr-only">
          Delete item confirmation
        </h2>
        <SlButton
          ref={deleteConfirmRef}
          slot="footer"
          variant="primary"
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault();
              handleDelete();
              setDeleteDialog(false);
            }
          }}
          onClick={() => {
            handleDelete();
            setDeleteDialog(false);
          }}
        >
          OK
        </SlButton>
      </SlDialog>
    </li>
  );
};

export default TodoItem;

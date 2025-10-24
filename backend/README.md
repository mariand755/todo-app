# Todo-App
A simple command-line To-Do List application written in Python.  
Organize tasks into folders, add, edit, delete, and search items efficiently.

## Features
- **Folder Management**
  - Add, edit, delete folders
  - Search folders by title
  - List all folders

- **Todo Item Management**
  - Add, edit, delete items within folders
  - Search items by title
  - List items in a folder

- **User-Friendly CLI**
  - Interactive prompts
  - Command aliases for quick navigation

## Project Structure

```
todo-app/
├── main.py                # Entry point for the CLI app
├── README.md              # Project documentation
├── TO Do List             # Project outline and notes
├── library/
│   ├── __init__.py
│   ├── folder_manager.py  # Manages folders
│   ├── folder.py          # Folder class and item management
│   ├── todo_item.py       # TodoItem class
│   └── __pycache__/       # Python cache files (ignored)
└── .gitignore             # Files/folders to ignore in git
```


## Getting Started

### Prerequisites

- Python 3.11 or higher (recommended)

## Installation

Clone the repository:
```sh
git clone git@github.com:mariand755/todo-app.git
cd todo-app
```

## Running the App

Run the main script:
```sh
python main.py
```

Follow the interactive prompts to manage folders and todo items.

## Usage

- **Folders:** Add, view, edit, delete, and search folders.
- **Items:** Add, view, edit, delete, and search todo items within a selected folder.
- **Exit:** Quit the application at any time.

## Example Workflow

1. Start the app:  
   `python main.py`
2. Add a folder:  
   Choose `folders` → `add`
3. Add items to a folder:  
   Choose `items` → select folder ID → `add`
4. Edit or delete items/folders as needed.

## Contributing

Feel free to fork and submit pull requests.  
Suggestions and improvements are welcome!

## License

This project is for learning purposes and does not have a formal license.

---

**Author:**  
Marian Dadzie
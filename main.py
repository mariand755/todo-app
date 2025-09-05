from library.folder import Folder
from library.todo_item import TodoItem


def todo_list():
    todos = []
    new_folder = Folder(id=1, title="Prayer Conference")
    insert_id = 1
    print("Welcome to the Todo List App!")  # Initialize an empty todo list
    print("You can add todos, view them, or exit the app.") 
    commands = ["add", "view", "exit", "edit", "delete", "search"]
    command_str = "/".join(commands)
    while True:
        command = input(f"Enter command ({command_str}): ").strip().lower()

        if command == "add":
            while True:
                new_title = input("Enter a new todo item (unless done adding): ").strip()
                if not new_title:
                    break
                new_item = TodoItem(id=insert_id, title=new_title)
                new_folder.add_new_items_to_folder([new_item])
                insert_id += 1

        elif command == "view":
            new_folder.list_items_within_folder()

        elif command == "edit":
            new_folder.list_items_within_folder()
            edit_id = handle_input_int("Which title do you want to edit? ID: ")
            updated_title = input("Enter updated title name: ")
            updated_item = {}
            updated_item[edit_id] = updated_title
            new_folder.edit_items_within_folder(updated_item)

        elif command == "delete":   
            new_folder.list_items_within_folder()
            delete_id = handle_input_int("Which title do you want to delete? ID: ")
            new_folder.remove_items_within_folder([delete_id])

       # elif command == "search":


        elif command == "exit":
            print("Exiting the todo list.")
            break


        else:
            print("Unknown command. Please use 'add', 'view', or 'exit'.")

def handle_input_int(user_prompt:str)->int:
    try:
        return int(input(user_prompt))
    except:
        return -1
    
todo_list()

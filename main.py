from library.folder import Folder
from library.todo_item import TodoItem
from typing import Union


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

        if command == "add" or command == "a":
            while True:
                new_title = input("Enter a new todo item (unless done adding): ").strip()
                if new_title == "":
                    break
                new_item = TodoItem(id=insert_id, title=new_title)
                new_folder.add_new_items_to_folder([new_item])
                insert_id += 1

        elif command == "view" or command == "v" :
            new_folder.list_items_within_folder()

        elif command == "edit" or command == "ed":
            while True:
                new_folder.list_items_within_folder()
                edit_id = handle_input_int("Which title do you want to edit, unless done editing. ID: ")
                if edit_id == None:
                    break
                elif not new_folder.does_item_exist(edit_id):
                    continue
                updated_title = input("Enter updated title name: ")
                updated_item = {}
                updated_item[edit_id] = updated_title
                new_folder.edit_items_within_folder(updated_item)

        elif command == "delete" or command == "d":  
            while True:
                new_folder.list_items_within_folder()
                delete_id = handle_input_int("Which title do you want to delete, unless done deleting. ID: ")
                if delete_id == None:
                    break
                elif not new_folder.does_item_exist(delete_id):
                    continue
                new_folder.remove_items_within_folder([delete_id])


        elif command == "search" or command == "s":
            while True:
                input_title = input("Which title do you want to search, unless done searching. Title: ").strip()
                if input_title == "":
                    break
                result_item = new_folder.search_for_items_using_title(input_title)
                if len(result_item) == 0:
                    print(f"Did not find {input_title}")
                    continue
                for item in result_item:
                    print(f"Found {item}")
             

        elif command == "exit" or command == "ex":
            print("Exiting the todo list.")
            break


        else:
            print("Unknown command. Please use 'add', 'view', or 'exit'.")

def handle_input_int(user_prompt:str)-> Union[int, None]:
    try:
        user_input = input(user_prompt).strip()
        if user_input == "":
            return None
        return int(user_input)
    except ValueError as e:
        print(f"Invalid ID '{user_input}' was entered.")
        return -1
    
todo_list()

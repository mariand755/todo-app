from library.folder_manager import FolderManager
from library.folder import Folder
from typing import Union
from colorist import Color, effect_bold, BrightColor

def todo_list():
    folder_manager = FolderManager()
    effect_bold(f"{Color.MAGENTA}Welcome to the Todo List App!{Color.OFF}")  # Initialize an empty todo list
    effect_bold("You can manage Folders, Items, or Exit the app.") 
    commands = ["(f)olders", "(i)tems", "(ex)it"]
    command_str = "/".join(commands)
    while True:
        command = input(f"Enter command ({command_str}): ").strip().lower()
       
        if command == "folders" or command == "f":
            handle_folder_operations(folder_manager = folder_manager)
            
        elif command == "items" or command == "i":
            if not folder_manager.does_any_folder_exist_in_foldermanager():
                effect_bold(f"{Color.RED}Need to create a folder first{Color.OFF}")
                continue
            while True:
                folder_manager.list_folders_within_app()
                folder_id = handle_input_int("Which folder do you want to add items to, unless done adding. ID: ")
                if folder_id == None:
                    break
                folder = folder_manager.get_folder(folder_id)
                if folder == None:
                    continue
                handle_item_operations(folder)
        elif command == "exit" or command == "ex":
            effect_bold(f"{BrightColor.GREEN}Exiting the App.{BrightColor.OFF}")
            break
        else:
            effect_bold(f"{Color.RED}Unknown command. Please use '(f)olders', '(i)tems', or '(ex)it'.{Color.OFF}")

def handle_folder_operations(folder_manager: FolderManager):
    commands = ["add", "view", "exit", "edit", "delete", "search"]
    command_str = "/".join(commands)
    while True:
        command = input(f"Enter command for folder ({command_str}): ").strip().lower()

        if command == "add" or command == "a":
            while True:
                new_title = input("Enter a new folder (unless done adding): ").strip()
                if new_title == "":
                    break
                folder_manager.add_folder(new_title)

        elif command == "view" or command == "v" :
            folder_manager.list_folders_within_app()

        elif command == "edit" or command == "ed":
            while True:
                folder_manager.list_folders_within_app()
                edit_id = handle_input_int("Which folder title do you want to edit, unless done editing. ID: ")
                if edit_id == None:
                    break
                elif not folder_manager.does_folder_exist(edit_id):
                    continue
                updated_title = input("Enter updated folder title name: ")
                updated_item = {}
                updated_item[edit_id] = updated_title
                folder_manager.edit_folders_within_app(updated_item)

        elif command == "delete" or command == "d":  
            while True:
                folder_manager.list_folders_within_app()
                delete_id = handle_input_int("Which folder title do you want to delete, unless done deleting. ID: ")
                if delete_id == None:
                    break
                elif not folder_manager.does_folder_exist(delete_id):
                    continue
                folder_manager.remove_folders_within_app([delete_id])

        elif command == "search" or command == "s":
            while True:
                input_title = input("Which foler title do you want to search, unless done searching. Title: ").strip()
                if input_title == "":
                    break
                result_item = folder_manager.search_for_folders_using_title(input_title)
                if len(result_item) == 0:
                    effect_bold(f"{Color.RED}Did not find {input_title}{Color.OFF}")
                    continue
                for folder in result_item:
                    print(f"Found {folder}")
        
        elif command == "exit" or command == "ex":
            effect_bold(f"{BrightColor.GREEN}Exiting the Folder Manager.{BrightColor.OFF}")
            break

def handle_item_operations(folder:Folder):
    commands = ["add", "view", "exit", "edit", "delete", "search"]
    command_str = "/".join(commands)
    while True:
        command = input(f"Enter command ({command_str}): ").strip().lower()

        if command == "add" or command == "a":
            while True:
                new_title = input("Enter a new todo item (unless done adding): ").strip()
                if new_title == "":
                    break
                folder.add_new_items_to_folder([new_title])

        elif command == "view" or command == "v" :
            folder.list_items_within_folder()

        elif command == "edit" or command == "ed":
            while True:
                folder.list_items_within_folder()
                edit_id = handle_input_int("Which title do you want to edit, unless done editing. ID: ")
                if edit_id == None:
                    break
                elif not folder.does_item_exist(edit_id):
                    continue
                updated_title = input("Enter updated title name: ")
                updated_item = {}
                updated_item[edit_id] = updated_title
                folder.edit_items_within_folder(updated_item)

        elif command == "delete" or command == "d":  
            while True:
                folder.list_items_within_folder()
                delete_id = handle_input_int("Which title do you want to delete, unless done deleting. ID: ")
                if delete_id == None:
                    break
                elif not folder.does_item_exist(delete_id):
                    continue
                folder.remove_items_within_folder([delete_id])

        elif command == "search" or command == "s":
            while True:
                input_title = input("Which title do you want to search, unless done searching. Title: ").strip()
                if input_title == "":
                    break
                result_item = folder.search_for_items_using_title(input_title)
                if len(result_item) == 0:
                    effect_bold(f"{Color.RED}Did not find {input_title}{Color.OFF}")
                    continue
                for item in result_item:
                    print(f"Found {item}")
        
        elif command == "exit" or command == "ex":
            effect_bold(f"{BrightColor.GREEN}Exiting the ToDo Item Manager.{BrightColor.OFF}")
            break
              
def handle_input_int(user_prompt:str)-> Union[int, None]:
    try:
        user_input = input(user_prompt).strip()
        if user_input == "":
            return None
        return int(user_input)
    except ValueError as e:
        effect_bold(f"{Color.RED}Invalid ID '{user_input}' was entered.{Color.OFF}")
        return -1
    
todo_list()

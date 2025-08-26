from library.folder import Folder
from library.todo_item import TodoItem

#adding
new_folder = Folder(id=1, title="Conference")
new_item = TodoItem(id=1, title="Praise Conference")
second_item = TodoItem(id=2,title="Praise Conference")
third_item = TodoItem(id=3, title="Worship Conference")
fourth_item = TodoItem(id=4, title="Prayer Conference")
fifth_item = TodoItem(title="Breakfest Execs", id=5)
new_folder.add_new_items_to_folder([new_item, second_item, third_item, fourth_item, fifth_item])
new_folder.list_items_within_folder()
print("\n")

#deleting
new_folder.remove_items_within_folder([2,3])
new_folder.list_items_within_folder()
print("\n")

#editing
find_id_of_items = {
    1: "Praise Conference", 
    2: "Book Signing Session", 
    3: "Worship Conference",
    4: "Prayer Summit",
    5: "Breakfest Execs"
}
new_folder.edit_items_within_folder(find_id_of_items)
new_folder.list_items_within_folder()
print("\n")

#add in after edit
new_folder.add_new_items_to_folder([second_item, third_item])
new_folder.list_items_within_folder()
print("\n")


def todo_list():
    todos = []
    print("Welcome to the Todo List App!")  # Initialize an empty todo list
    print("You can add todos, view them, or exit the app.") 
    while True:
        command = input("Enter command (add/view/exit): ").strip().lower()

        if command == "add":
            todo = input("Enter a new todo item: ").strip()
            if todo:
                todos.append(todo)
                print(f"Added todo: {todo}")
            else:
                print("Todo cannot be empty.")

        elif command == "view":
            if todos:
                print("Todo List:")
                for i, todo in enumerate(todos, start=1):
                    print(f"{i}. {todo}")
            else:
                print("No todos available.")

        elif command == "exit":
            print("Exiting the todo list.")
            break

        else:
            print("Unknown command. Please use 'add', 'view', or 'exit'.")

#todo_list()



class TodoItem:
    def __init__(self, id:int, title:str):
        self.id = id
        self.title = title

    def __str__(self):
        return f"Welcome to our first ToDo_App: {self.id} {self.title}"    
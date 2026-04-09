# In-memory todo item used by the CLI — not the SQLAlchemy model in models.py.
class TodoItem:
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title

    def __str__(self):
        return f"ID {self.id}: {self.title}"

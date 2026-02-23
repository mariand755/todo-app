import uuid

from sqlalchemy.orm import Session

from library.models import Folder, TodoItem


def seed_db_with_test_folder(
    testing_db_session: Session,
    random_title: str = None,
    is_folder_deleted: bool = False,
) -> Folder:
    if random_title is None:
        random_title = f"test_{uuid.uuid4()}"
    folder = Folder(title=random_title, is_deleted=is_folder_deleted)
    testing_db_session.add(folder)
    testing_db_session.flush()
    return folder


def create_test_payload(num: int) -> list[dict]:
    return [{"title": f"test_{uuid.uuid4()}"} for i in range(num)]


def seed_db_with_test_item(
    testing_db_session: Session,
    folder: Folder,
    random_title: str = None,
    is_item_deleted: bool = False,
    completed: bool = False,
    position: int = -1,
) -> TodoItem:
    if random_title is None:
        random_title = f"test_{uuid.uuid4()}"
    item = TodoItem(
        folder_id=folder.id,
        title=random_title,
        is_deleted=is_item_deleted,
        completed=completed,
        position=position,
    )
    testing_db_session.add(item)
    testing_db_session.flush()
    return item

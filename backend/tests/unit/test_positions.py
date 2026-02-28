from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from library import models


def _create_memory_session():
    engine = create_engine("sqlite:///:memory:")
    models.Base.metadata.create_all(engine)
    session = Session(bind=engine)
    return engine, session


def test_get_next_item_position_empty_folder():
    engine, session = _create_memory_session()
    try:
        # create folder
        folder = models.Folder(title="folderOne")
        session.add(folder)
        session.commit()

        pos = models.get_next_item_position(session, folder.id)
        assert pos == 0
    finally:
        session.close()
        engine.dispose()


def test_get_next_item_position_after_items():
    engine, session = _create_memory_session()
    try:
        folder = models.Folder(title="f2")
        session.add(folder)
        session.flush()

        # add two items
        item1 = models.TodoItem(title="a", folder_id=folder.id, position=0)
        item2 = models.TodoItem(title="b", folder_id=folder.id, position=1)
        session.add_all([item1, item2])
        session.commit()

        pos = models.get_next_item_position(session, folder.id)
        assert pos == 2
    finally:
        session.close()
        engine.dispose()

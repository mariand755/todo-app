import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from library import models


def _create_memory_session():
    engine = create_engine("sqlite:///:memory:")
    models.Base.metadata.create_all(engine)
    session = Session(bind=engine)
    return engine, session


# An empty folder should produce position 0 so the first item lands at index zero.
@pytest.mark.BUT45
def test_get_next_item_position_returns_zero_for_empty_folder():
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


# After two items are added, the next available position should be 2.
@pytest.mark.BUT46
def test_get_next_item_position_increments_after_each_item():
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

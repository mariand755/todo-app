import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from library import models


def _create_memory_session():
    engine = create_engine("sqlite:///:memory:")
    models.Base.metadata.create_all(engine)
    session = Session(bind=engine)
    return engine, session


# The next position should be one beyond the highest non-deleted, positioned folder row.
@pytest.mark.BUT35
def test_get_next_folder_position_with_mixed_rows():
    engine, session = _create_memory_session()
    try:
        session.add_all(
            [
                models.Folder(title="a", position=0),
                models.Folder(title="b", position=2),
                models.Folder(title="c", position=-1),
                models.Folder(title="d", position=5, is_deleted=True),
            ]
        )
        session.commit()

        next_position = models.get_next_folder_position(session)
        # max non-deleted position with position >= 0 is 2, so next is 3
        assert next_position == 3
    finally:
        session.close()
        engine.dispose()


# Rows with position=-1 (legacy) should be assigned positions in ascending id order after existing ones.
@pytest.mark.BUT36
def test_ensure_folder_positions_backfills_unpositioned_rows_in_id_order():
    engine, session = _create_memory_session()
    try:
        positioned = models.Folder(title="positioned", position=4)
        first_unpositioned = models.Folder(title="u1", position=-1)
        second_unpositioned = models.Folder(title="u2", position=-1)

        session.add_all([positioned, first_unpositioned, second_unpositioned])
        session.commit()

        changed = models.ensure_folder_positions(session)
        session.commit()

        assert changed is True

        refreshed = session.query(models.Folder).order_by(models.Folder.id).all()
        by_title = {folder.title: folder.position for folder in refreshed}
        assert by_title["positioned"] == 4
        assert by_title["u1"] == 5
        assert by_title["u2"] == 6
    finally:
        session.close()
        engine.dispose()


# When all rows already have valid positions, no changes are made and False is returned.
@pytest.mark.BUT37
def test_ensure_folder_positions_returns_false_when_no_backfill_needed():
    engine, session = _create_memory_session()
    try:
        session.add_all(
            [
                models.Folder(title="a", position=0),
                models.Folder(title="b", position=1),
            ]
        )
        session.commit()

        changed = models.ensure_folder_positions(session)
        session.commit()

        assert changed is False

        refreshed = session.query(models.Folder).order_by(models.Folder.id).all()
        assert [folder.position for folder in refreshed] == [0, 1]
    finally:
        session.close()
        engine.dispose()

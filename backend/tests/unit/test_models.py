import pytest
import sqlalchemy as sa
from sqlalchemy import create_engine, inspect

import library.models as models


# The SQLAlchemy model definitions should declare all columns the application depends on.
@pytest.mark.BUT38
def test_table_names_and_columns_present():
    # arrange/act - inspect table metadata
    folder_cols = {c.name for c in models.Folder.__table__.columns}
    todo_cols = {c.name for c in models.TodoItem.__table__.columns}

    # assert - required columns are present
    assert folder_cols >= {"id", "title", "is_deleted", "is_pinned"}
    assert todo_cols >= {"id", "title", "folder_id", "is_deleted", "completed", "position"}


# Column types and defaults should match what the rest of the app relies on at runtime.
@pytest.mark.BUT39
def test_column_defaults_and_types():
    folder_id_col = models.Folder.__table__.columns["id"]
    folder_title_col = models.Folder.__table__.columns["title"]
    folder_is_deleted_col = models.Folder.__table__.columns["is_deleted"]
    folder_is_pinned_col = models.Folder.__table__.columns["is_pinned"]

    assert isinstance(folder_id_col.type, sa.Integer)
    assert isinstance(folder_title_col.type, sa.String)
    # default value for is_deleted should be False
    assert folder_is_deleted_col.default is not None
    assert folder_is_deleted_col.default.arg is False
    assert folder_is_pinned_col.default is not None
    assert folder_is_pinned_col.default.arg is False

    todo_position_col = models.TodoItem.__table__.columns["position"]
    todo_completed_col = models.TodoItem.__table__.columns["completed"]
    assert todo_position_col.default is not None
    assert todo_position_col.default.arg == -1
    assert todo_completed_col.default.arg is False


# The get_db generator must close the session in the finally block to prevent connection leaks.
@pytest.mark.BUT40
def test_get_db_generator_closes_session(monkeypatch):
    # arrange - replace SessionLocal with a dummy factory so we can observe close() being called
    class DummySession:
        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

    def dummy_factory():
        return DummySession()

    monkeypatch.setattr(models, "SessionLocal", dummy_factory)

    # act - drive the generator to completion to trigger the finally block
    gen = models.get_db()
    session = next(gen)
    assert isinstance(session, DummySession)
    gen.close()

    # assert - the session was closed on exit
    assert session.closed is True


# ensure_folder_pin_column should add the column when it is genuinely absent.
@pytest.mark.BUT41
def test_ensure_folder_pin_column_adds_column_when_missing():
    # arrange - create a bare-bones table that does not have is_pinned
    engine = create_engine("sqlite:///:memory:")
    with engine.begin() as conn:
        conn.execute(sa.text("CREATE TABLE folder (id INTEGER PRIMARY KEY, title TEXT NOT NULL)"))

    original_engine = models.engine
    try:
        # act - point the helper at our test engine and run the migration
        models.engine = engine
        models.ensure_folder_pin_column()

        # assert - the column should now exist
        inspector = inspect(engine)
        col_names = {col["name"] for col in inspector.get_columns("folder")}
        assert "is_pinned" in col_names
    finally:
        models.engine = original_engine
        engine.dispose()


# Calling ensure_folder_pin_column a second time when the column already exists should not raise.
@pytest.mark.BUT42
def test_ensure_folder_pin_column_is_idempotent_when_column_already_exists():
    # arrange - create a full schema that already includes is_pinned
    engine = create_engine("sqlite:///:memory:")
    models.Base.metadata.create_all(engine)

    original_engine = models.engine
    try:
        models.engine = engine
        # act - first call should be a no-op; second call should also be safe
        models.ensure_folder_pin_column()
        models.ensure_folder_pin_column()

        # assert - column is still present and exactly one copy of it exists
        inspector = inspect(engine)
        col_names = {col["name"] for col in inspector.get_columns("folder")}
        assert "is_pinned" in col_names
    finally:
        models.engine = original_engine
        engine.dispose()

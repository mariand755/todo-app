
import sqlalchemy as sa

import library.models as models


def test_table_names_and_columns_present():
    # ARRANGE/ACT - inspect table metadata
    folder_cols = {c.name for c in models.Folder.__table__.columns}
    todo_cols = {c.name for c in models.TodoItem.__table__.columns}

    # ASSERT - columns exist
    assert folder_cols >= {"id", "title", "is_deleted"}
    assert todo_cols >= {"id", "title", "folder_id", "is_deleted", "completed", "position"}


def test_column_defaults_and_types():
    # ASSERT default args and types from the Column objects
    folder_id_col = models.Folder.__table__.columns["id"]
    folder_title_col = models.Folder.__table__.columns["title"]
    folder_is_deleted_col = models.Folder.__table__.columns["is_deleted"]

    assert isinstance(folder_id_col.type, sa.Integer)
    assert isinstance(folder_title_col.type, sa.String)
    # default value for is_deleted should be False
    assert folder_is_deleted_col.default is not None
    assert folder_is_deleted_col.default.arg is False

    todo_position_col = models.TodoItem.__table__.columns["position"]
    todo_completed_col = models.TodoItem.__table__.columns["completed"]
    assert todo_position_col.default is not None
    assert todo_position_col.default.arg == -1
    assert todo_completed_col.default.arg is False


def test_get_db_generator_closes_session(monkeypatch):
    # ARRANGE - replace SessionLocal with a dummy factory so we can observe close() being called
    class DummySession:
        def __init__(self):
            self.closed = False
        def close(self):
            self.closed = True

    def dummy_factory():
        return DummySession()

    monkeypatch.setattr(models, "SessionLocal", dummy_factory)

    # ACT - get generator, take session then close generator to trigger finally block
    gen = models.get_db()
    session = next(gen)
    assert isinstance(session, DummySession)
    gen.close()

    # ASSERT - the dummy session was closed
    assert session.closed is True

"""
def test_engine_falls_back_to_sqlite_when_create_engine_raises(monkeypatch):
    # ARRANGE - monkeypatch sqlalchemy.create_engine to raise during module import
    import importlib, sys

    orig_create_engine = sa.create_engine

    def raise_create_engine(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(sa, "create_engine", raise_create_engine)

    # Reload the module to exercise the try/except branch
    with pytest.raises(RuntimeError) as e:
        importlib.reload(models)

    # ASSERT - engine should be sqlite in-memory due to fallback
    assert "sqlite" in models.engine.url.drivername or models.engine.url.get_backend_name() == "sqlite"

    # cleanup - restore original create_engine and reload models to normal state
    monkeypatch.setattr(sa, "create_engine", orig_create_engine)
    importlib.reload(models)
"""
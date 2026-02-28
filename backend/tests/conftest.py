from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

from app.api import app
from library.models import Base, get_db


def _as_posix(path_obj) -> str:
    return Path(str(path_obj)).as_posix()


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        path = _as_posix(item.fspath)

        if "/tests/integration/" in path:
            item.add_marker(pytest.mark.integration)

            if path.endswith("/test_api.py"):
                item.add_marker(pytest.mark.contract)

            if path.endswith("/test_item_order_persistence.py") or path.endswith("/test_positions_integration.py"):
                item.add_marker(pytest.mark.persistence)

            continue

        if "/tests/unit/" in path:
            item.add_marker(pytest.mark.unit)


@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def testing_db_session(db_engine):
    connection: Connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):
        if trans.nested and trans._parent is not None and not trans._parent.nested:
            sess.begin_nested()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def test_client(testing_db_session: Session):
    def override_get_db():
        yield testing_db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

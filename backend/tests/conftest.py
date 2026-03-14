from __future__ import annotations

import os
import re
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


def pytest_configure(config: pytest.Config) -> None:
    # Register numeric test-id markers so IDs can be used consistently across files.
    for index in range(1, 200):
        config.addinivalue_line("markers", f"BUT{index:02d}: backend unit test id marker")
        config.addinivalue_line("markers", f"BINT{index:02d}: backend integration test id marker")


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    test_id_pattern = re.compile(r"^(BUT|BINT)\d+$")

    for item in items:
        for marker in item.iter_markers():
            if test_id_pattern.match(marker.name):
                item.keywords[marker.name] = True

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


def _create_test_engine():
    # CI can provide TEST_DATABASE_URL to run integration tests against Postgres.
    database_url = os.getenv("TEST_DATABASE_URL", "").strip()

    if database_url:
        return create_engine(database_url, pool_pre_ping=True)

    return create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})


@pytest.fixture(scope="function")
def db_engine():
    engine = _create_test_engine()
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def testing_db_session(db_engine):
    connection: Connection = db_engine.connect()
    transaction = connection.begin()

    # Keep tests deterministic when the target Postgres DB already has data.
    if db_engine.dialect.name != "sqlite":
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())

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

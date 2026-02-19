import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session

from app.api import app
from library.models import Base, get_db

pytestmark = pytest.mark.integration


@pytest.fixture(scope="function")
def db_engine():
    """Create a single, in-memory SQLite Engine for the test module."""
    # Use :memory: for speed and isolation between test modules
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()  # closes underlying sqlite connections


@pytest.fixture(scope="function")
def testing_db_session(db_engine):
    """
    Creates a new function-scoped transactional session that automatically
    rolls back all changes (even those that were committed) upon completion.
    """
    # 1. Connect to the Engine and start a Core Transaction
    connection: Connection = db_engine.connect()
    transaction = connection.begin()

    # 2. Bind the ORM Session to this Connection
    # The session is configured to participate in the external transaction.
    session = Session(bind=connection)
    session.begin_nested()  # start initial savepoint

    # 3. Use an event listener to re-establish the savepoint after internal COMMITs
    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(sess, trans):
        if trans.nested and trans._parent is not None and not trans._parent.nested:
            sess.begin_nested()  # restart on the SAME session

    # 4. Yield the session to the test
    yield session

    # 5. TEARDOWN: Rollback the main Core transaction and close
    session.close()
    transaction.rollback()  # Rolls back ALL committed changes made by the test
    connection.close()  # Returns connection to the engine pool


@pytest.fixture
def test_client(testing_db_session: Session):
    def override_get_db():
        yield testing_db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

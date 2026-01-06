import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session
from fastapi_tool.fastapi import Base


@pytest.fixture(scope="module")
def db_engine():
    """Create a single, in-memory SQLite Engine for the test module."""
    # Use :memory: for speed and isolation between test modules
    engine = create_engine(
        "sqlite:///:memory:", 
        connect_args={"check_same_thread": False}
    ) 
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


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

    # 3. Use an event listener to re-establish the savepoint after internal COMMITs
    @event.listens_for(session, "after_transaction_end")
    def end_savepoint(session, transaction):
        if transaction.nested and not transaction.parent.nested:
            session.begin_nested()

    # 4. Yield the session to the test
    yield session
    
    # 5. TEARDOWN: Rollback the main Core transaction and close
    session.close()
    if transaction.is_active:
        transaction.rollback()  # Rolls back ALL committed changes made by the test
    connection.close()      # Returns connection to the engine pool
import os

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from sqlalchemy.orm.decl_api import DeclarativeMeta

# database config
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")

# Database engine
try:
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}", echo=True)
except Exception:
    # Fallback to an in-memory sqlite DB when engine creation fails (useful for tests / missing drivers)
    engine = create_engine("sqlite:///:memory:", echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base: DeclarativeMeta = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_next_item_position(db_session: Session, folder_id: int) -> int:
    """Return the next position index for a new TodoItem in the folder.

    This counts non-deleted items in the folder and returns that count
    (so the first item will have position 0).
    """
    count = db_session.query(TodoItem).filter(TodoItem.folder_id == folder_id, TodoItem.is_deleted.is_(False)).count()
    return int(count)


class Folder(Base):
    __tablename__ = "folder"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)
    is_deleted = sa.Column(sa.Boolean, default=False, nullable=False)


class TodoItem(Base):
    __tablename__ = "todo_item"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)
    folder_id = sa.Column(sa.Integer, sa.ForeignKey("folder.id"), nullable=False)
    is_deleted = sa.Column(sa.Boolean, default=False, nullable=False)
    completed = sa.Column(sa.Boolean, default=False, nullable=False)
    position = sa.Column(sa.Integer, default=-1, nullable=False)

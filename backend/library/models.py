import logging
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
SQL_ECHO = os.getenv("SQL_ECHO", "false").strip().lower() in {"1", "true", "yes", "on"}

logger = logging.getLogger("todo_app.models")

# Database engine
try:
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}", echo=SQL_ECHO)
except Exception:
    # Fallback to an in-memory sqlite DB when engine creation fails (useful for tests / missing drivers)
    logger.warning("Falling back to sqlite in-memory engine")
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


def get_next_folder_position(db_session: Session) -> int:
    """Return the next position index for a new Folder.

    Uses the highest non-deleted folder position and appends after it.
    """
    max_position = (
        db_session.query(sa.func.max(Folder.position))
        .filter(Folder.is_deleted.is_(False), Folder.position >= 0)
        .scalar()
    )
    if max_position is None:
        return 0
    return int(max_position) + 1


def ensure_folder_positions(db_session: Session) -> bool:
    """Backfill missing folder positions for legacy rows.

    Returns True when any row was updated, else False.
    """
    unpositioned_folders = db_session.query(Folder).filter(Folder.position < 0).order_by(Folder.id).all()
    if not unpositioned_folders:
        return False

    max_position = db_session.query(sa.func.max(Folder.position)).filter(Folder.position >= 0).scalar()
    next_position = 0 if max_position is None else int(max_position) + 1

    for folder in unpositioned_folders:
        folder.position = next_position
        next_position += 1

    db_session.add_all(unpositioned_folders)
    return True


class Folder(Base):
    __tablename__ = "folder"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)
    is_deleted = sa.Column(sa.Boolean, default=False, nullable=False)
    position = sa.Column(sa.Integer, default=-1, nullable=False)


class TodoItem(Base):
    __tablename__ = "todo_item"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, nullable=False)
    folder_id = sa.Column(sa.Integer, sa.ForeignKey("folder.id"), nullable=False)
    is_deleted = sa.Column(sa.Boolean, default=False, nullable=False)
    completed = sa.Column(sa.Boolean, default=False, nullable=False)
    position = sa.Column(sa.Integer, default=-1, nullable=False)

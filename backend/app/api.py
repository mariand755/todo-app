import logging
import os
import time
import uuid
from typing import Sequence, cast

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.orm import Session

from app.logging_config import configure_logging, request_id_context
from library.models import Base, ensure_folder_positions, get_db, get_next_folder_position
from library.models import Folder as FolderModel
from library.models import TodoItem as TodoItemModel

configure_logging()
logger = logging.getLogger("todo_app.api")

app = FastAPI()


# Only the frontend dev server makes cross-origin requests.
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Logs every request with a unique ID, method, path, status, and duration.
# The request ID is also returned in the X-Request-ID response header.
@app.middleware("http")
async def log_requests(request: Request, call_next):
    request_id = uuid.uuid4().hex[:12]
    token = request_id_context.set(request_id)
    start = time.perf_counter()
    try:
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "request_completed method=%s path=%s status=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        response.headers["X-Request-ID"] = request_id
        return response
    except Exception:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.exception(
            "request_failed method=%s path=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise
    finally:
        request_id_context.reset(token)


# Reformats Pydantic validation errors into a simpler {field, problem} shape
# so the frontend doesn't have to parse FastAPI's default error format.
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = exc.errors()
    simplified_errors = []
    for error in errors:
        simplified_errors.append({"field": error["loc"][-1], "problem": error["msg"]})
    logger.warning("validation_error path=%s error_count=%s", request.url.path, len(simplified_errors))
    return JSONResponse(
        status_code=400,
        content={"errors": simplified_errors},
    )


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Hard-resets the test database by deleting all rows from every table.
# Only registered when ALLOW_TEST_RESET=true — the route doesn't exist in production.
# Never expose this on a public network.
if os.environ.get("ALLOW_TEST_RESET", "").lower() == "true":

    @app.post("/test/reset")
    async def test_reset(db_session: Session = Depends(get_db)):
        for table in reversed(Base.metadata.sorted_tables):
            db_session.execute(table.delete())
        db_session.commit()
        return {"status": "reset"}


# Returns all non-deleted folders, pinned ones first, then sorted by position.
# Fixes any gaps in folder positions before querying.
@app.get("/folders")
async def get_folders(db_session: Session = Depends(get_db)):
    positions_updated = ensure_folder_positions(db_session)
    if positions_updated:
        db_session.commit()
    folders = (
        db_session.query(FolderModel)
        .filter(FolderModel.is_deleted.is_(False))
        .order_by(FolderModel.is_pinned.desc(), FolderModel.position, FolderModel.id)
        .all()
    )
    return folders


class CreateFolder(BaseModel):
    title: str


class FolderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    is_pinned: bool


# Creates a new folder. Fixes position gaps first so the new folder
# gets the correct next position.
@app.post("/folders", response_model=FolderResponse)
async def create_folder(new_folder_request: CreateFolder, db_session: Session = Depends(get_db)):
    positions_updated = ensure_folder_positions(db_session)
    if positions_updated:
        db_session.flush()
    new_folder = FolderModel(title=new_folder_request.title, position=get_next_folder_position(db_session))
    db_session.add(new_folder)
    db_session.commit()
    return new_folder


# Returns a specific folder by ID.
@app.get("/folders/{folder_id}")
async def get_folder(folder_id: int, db_session: Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    # Validates that the folder exists and isn't deleted.
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder


class UpdateFolder(BaseModel):
    title: str


# Updates a folder's title.
@app.put("/folders/{folder_id}", response_model=FolderResponse)
async def update_folder(folder_id: int, update_folder_request: UpdateFolder, db_session: Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    # Validates that the folder exists and isn't deleted.
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    folder.title = update_folder_request.title
    db_session.add(folder)
    db_session.commit()
    return folder


class UpdateFolderPin(BaseModel):
    is_pinned: bool


# Updates a folder's pinned status.
@app.put("/folders/{folder_id}/pin", response_model=FolderResponse)
async def update_folder_pin(
    folder_id: int,
    update_folder_pin_request: UpdateFolderPin,
    db_session: Session = Depends(get_db),
):
    folder = db_session.get(FolderModel, folder_id)
    # Validates that the folder exists and isn't deleted.
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    folder.is_pinned = update_folder_pin_request.is_pinned
    db_session.add(folder)
    db_session.commit()
    return folder


# Soft-deletes a folder — marks it as deleted instead of removing the row.
@app.delete("/folders/{folder_id}")
async def delete_folder(folder_id: int, db_session: Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    # Validates that the folder exists and isn't deleted.
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    folder.is_deleted = True
    db_session.add(folder)
    db_session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Returns all non-deleted items within a folder, sorted by position.
@app.get("/folders/{folder_id}/items")
async def get_folder_items(folder_id: int, db_session: Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    # Validates that the folder exists and isn't deleted.
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    todo_items = (
        db_session.query(TodoItemModel)
        .filter(TodoItemModel.folder_id == folder_id, TodoItemModel.is_deleted.is_(False))
        .order_by(TodoItemModel.position)
        .all()
    )
    return todo_items


class CreateItem(BaseModel):
    title: str


class ItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    folder_id: int
    completed: bool
    position: int


class ItemArrayResponse(BaseModel):
    items: Sequence[ItemResponse]


# Creates a new item within a folder.
# The new item is added to the end of the list by assigning it the next position value.
@app.post("/folders/{folder_id}/items", response_model=ItemResponse)
async def create_new_item(folder_id: int, new_item_request: CreateItem, db_session: Session = Depends(get_db)):
    folder = db_session.query(FolderModel).filter(FolderModel.id == folder_id).first()
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    # Determine next position within the folder. If no items exist, start at 0.
    existing_items = (
        db_session.query(TodoItemModel)
        .filter(TodoItemModel.folder_id == folder_id, TodoItemModel.is_deleted.is_(False))
        .order_by(TodoItemModel.position)
        .all()
    )
    next_position = len(existing_items)

    add_new_item = TodoItemModel(title=new_item_request.title, folder_id=folder_id, position=next_position)
    db_session.add(add_new_item)
    db_session.commit()
    return add_new_item


# Returns a specific item by ID within a folder.
# Validates that the folder exists and isn't deleted.
@app.get("/folders/{folder_id}/items/{item_id}")
async def get_folder_item(folder_id: int, item_id: int, db_session: Session = Depends(get_db)):
    folder = db_session.query(FolderModel).filter(FolderModel.id == folder_id).first()
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = (
        db_session.query(TodoItemModel)
        .filter(
            TodoItemModel.folder_id == folder_id,
            TodoItemModel.id == item_id,
        )
        .first()
    )
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


class UpdateItem(BaseModel):
    title: str


# Updates an item's title. Completed items are locked and can't be edited.
@app.put("/folders/{folder_id}/items/{item_id}", response_model=ItemResponse)
async def update_item(
    folder_id: int,
    item_id: int,
    update_item_request: UpdateItem,
    db_session: Session = Depends(get_db),
):
    # Validates that the folder exists and isn't deleted before updating item.
    folder = db_session.get(FolderModel, folder_id)
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = (
        db_session.query(TodoItemModel)
        .filter(
            TodoItemModel.folder_id == folder_id,
            TodoItemModel.id == item_id,
        )
        .first()
    )
    # Validates that the item exists and isn't deleted before updating.
    if item is None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.completed:
        raise HTTPException(status_code=403, detail="Item completed and cannot be updated")
    item.title = update_item_request.title
    db_session.add(item)
    db_session.commit()
    return item


# Soft-deletes an item - marks it as deleted instead of removing the row.
@app.delete("/folders/{folder_id}/items/{item_id}")
async def delete_item(folder_id: int, item_id: int, db_session: Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    # Validate folder exists and isn't deleted before deleting item.
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = (
        db_session.query(TodoItemModel)
        .filter(
            TodoItemModel.folder_id == folder_id,
            TodoItemModel.id == item_id,
        )
        .first()
    )
    # Validate item exists and isn't deleted before deleting.
    if item is None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    item.is_deleted = True
    db_session.add(item)
    db_session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Flips an item between complete and incomplete.
@app.put("/folders/{folder_id}/items/{item_id}/toggle", response_model=ItemResponse)
async def toggle_item(folder_id: int, item_id: int, db_session: Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    # Validate folder exists and isn't deleted before toggling item.
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = (
        db_session.query(TodoItemModel)
        .filter(
            TodoItemModel.folder_id == folder_id,
            TodoItemModel.id == item_id,
        )
        .first()
    )
    # Validate item exists and isn't deleted before toggling.
    if item is None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    item.completed = not item.completed
    db_session.add(item)
    db_session.commit()
    return item


class UpdateItemOrder(BaseModel):
    itemOrder_id: list[int] = Field(..., min_length=1)


# Assign sequential positions to `all_items` based on `item_order_ids`.
#   - Items whose id appears in `item_order_ids` receive positions according to that list.
#   - Items not present in the list are assigned positions after the listed items.
#   This function mutates the objects in `all_items` in-place and also returns them.
def apply_item_order_positions(all_items, item_order_ids: list[int]):
    position_map = {item_id: idx for idx, item_id in enumerate(item_order_ids)}
    next_position = len(item_order_ids)
    for item in all_items:
        item_id = cast(int, item.id)
        if item_id in position_map:
            item.position = position_map[item_id]
        else:
            item.position = next_position
            next_position += 1
    return all_items


# Reorders items in a folder based on the provided list of item IDs.
# Used by the frontend for drag-and-drop sorting.
@app.put("/folders/{folder_id}/item_order", response_model=ItemArrayResponse)
async def item_order(folder_id: int, update_item_order: UpdateItemOrder, db_session: Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Folder not found")

    # Query ALL non-deleted items in the folder
    all_items = (
        db_session.query(TodoItemModel)
        .filter(
            TodoItemModel.folder_id == folder_id,
            TodoItemModel.is_deleted.is_(False),
        )
        .all()
    )

    # Apply ordering using helper to keep logic testable
    apply_item_order_positions(all_items, update_item_order.itemOrder_id)

    db_session.add_all(all_items)
    db_session.commit()

    # Return all items sorted by position
    items_sorted = sorted(all_items, key=lambda x: cast(int, x.position))
    return ItemArrayResponse(items=[ItemResponse.model_validate(x) for x in items_sorted])

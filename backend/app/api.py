from fastapi.responses import JSONResponse
from library.models import get_db
from library.models import Folder as FolderModel, TodoItem as TodoItemModel
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.middleware.cors import CORSMiddleware 
from library.folder_manager import FolderManager
from pydantic import BaseModel, ConfigDict, Field
from fastapi.exceptions import RequestValidationError


app = FastAPI()
folder_manager = FolderManager()
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # Custom logic to reformat the errors
    errors = exc.errors()
    simplified_errors = []
    for error in errors:
        simplified_errors.append({
            "field": error["loc"][-1],
            "problem": error["msg"]
        })
    return JSONResponse(
        status_code=400,
        content={"errors": simplified_errors},
    )

@app.get("/folders")
async def get_folders(db_session:Session = Depends(get_db)):
    folders = db_session.query(FolderModel).filter(FolderModel.is_deleted.is_(False)).all()
    return folders

class CreateFolder(BaseModel):
    title: str 

class FolderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str


@app.post("/folders", response_model=FolderResponse)
async def create_folder(new_folder_request:CreateFolder, db_session:Session = Depends(get_db)):
    new_folder = FolderModel(title = new_folder_request.title)
    db_session.add(new_folder)
    db_session.commit()
    return new_folder

@app.get("/folders/{folder_id}")
async def get_folder(folder_id:int, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder

class UpdateFolder(BaseModel):
    title: str

@app.put("/folders/{folder_id}", response_model=FolderResponse)
async def update_folder(folder_id:int, update_folder_request:UpdateFolder, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    folder.title = update_folder_request.title
    db_session.add(folder)
    db_session.commit()
    return folder

@app.delete("/folders/{folder_id}")
async def delete_folder(folder_id:int, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    folder.is_deleted = True
    db_session.add(folder) 
    db_session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/folders/{folder_id}/items")
async def get_folder_items(folder_id:int, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    todo_items = db_session.query(TodoItemModel).filter(TodoItemModel.folder_id == folder_id, 
    TodoItemModel.is_deleted.is_(False)).order_by(TodoItemModel.position).all()
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
    items: list[ItemResponse]

@app.post("/folders/{folder_id}/items", response_model=ItemResponse)
async def create_new_item(folder_id:int, new_item_request:CreateItem, db_session:Session = Depends(get_db)):
    folder = db_session.query(FolderModel).filter(FolderModel.id == folder_id).first()
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    add_new_item = TodoItemModel(title = new_item_request.title, folder_id = folder_id)
    db_session.add(add_new_item)
    db_session.commit()
    return add_new_item 

@app.get("/folders/{folder_id}/items/{item_id}")
async def get_folder_item(folder_id:int, item_id:int, db_session:Session = Depends(get_db)):
    folder = db_session.query(FolderModel).filter(FolderModel.id == folder_id).first()
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = db_session.query(TodoItemModel).filter(
        TodoItemModel.folder_id == folder_id, 
        TodoItemModel.id == item_id, 
    ).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

class UpdateItem(BaseModel):
    title: str

@app.put("/folders/{folder_id}/items/{item_id}", response_model=ItemResponse)
async def update_item(folder_id:int, item_id:int, update_item_request:UpdateItem, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = db_session.query(TodoItemModel).filter(
        TodoItemModel.folder_id == folder_id, 
        TodoItemModel.id == item_id, 
    ).first()    
    if item is None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    if item.completed:
        raise HTTPException(status_code=403, detail="Item completed and cannot be updated")
    item.title = update_item_request.title
    db_session.add(item)
    db_session.commit()
    return item

@app.delete("/folders/{folder_id}/items/{item_id}")
async def delete_item(folder_id:int, item_id:int, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = db_session.query(TodoItemModel).filter(
        TodoItemModel.folder_id == folder_id, 
        TodoItemModel.id == item_id, 
    ).first()
    if item is None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    item.is_deleted = True
    db_session.add(item) 
    db_session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#@app.put("/folders/{folder_id}/undo", response_model=FolderResponse)
# async def undo_folder(folder_id:int, db_session:Session = Depends(get_db)):
#     folder = db_session.get(FolderModel, folder_id)
#     if folder == None:
#         raise HTTPException(status_code=404, detail="Folder not found")
#     folder.is_deleted = False
#     db_session.add(folder)
#     db_session.commit()
#     return folder


# @app.put("/folders/{folder_id}/items/{item_id}/undo", response_model=ItemResponse)
# async def undo_item(folder_id:int, item_id:int, db_session:Session = Depends(get_db)):
#     folder = db_session.get(FolderModel, folder_id)
#     if folder == None:
#         raise HTTPException(status_code=404, detail="Folder not found")
#     item = db_session.query(TodoItemModel).filter(
#         TodoItemModel.folder_id == folder_id, 
#         TodoItemModel.id == item_id, 
#     ).first()    
#     if item == None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     item.is_deleted = False
#     db_session.add(item)
#     db_session.commit()
#     return item

@app.put("/folders/{folder_id}/items/{item_id}/toggle", response_model=ItemResponse)
async def toggle_item(folder_id:int, item_id:int, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder is None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = db_session.query(TodoItemModel).filter(
        TodoItemModel.folder_id == folder_id,
        TodoItemModel.id == item_id,
    ).first()
    if item is None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    item.completed = not item.completed
    db_session.add(item)
    db_session.commit()
    return item

class UpdateItemOrder(BaseModel):
    itemOrder_id: list[int] = Field(..., min_length=1)

@app.put("/folders/{folder_id}/item_order", response_model=ItemArrayResponse)
async def item_order(folder_id:int, update_item_order:UpdateItemOrder, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder is None:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = db_session.query(TodoItemModel).filter(
        TodoItemModel.folder_id.in_(update_item_order.itemOrder_id) == folder_id,
    ).all()
    for i in item:
        index = update_item_order.itemOrder_id.index(i.id)
        i.position = index
    db_session.add_all(item)
    db_session.commit()
    def item_pos(i):
        return i.position
    item = sorted(item, key=item_pos)
    return ItemArrayResponse(items=item)


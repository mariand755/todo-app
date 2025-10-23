from library.models import get_db
from library.models import SessionLocal, Folder as FolderModel, TodoItem as TodoItemModel
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Response, status, Depends
from library.folder_manager import FolderManager
from pydantic import BaseModel


app = FastAPI()
folder_manager = FolderManager()


@app.get("/folders")
async def get_folders(db_session:Session = Depends(get_db)):
    folders = db_session.query(FolderModel).filter(FolderModel.is_deleted == False).all()
    return folders

class CreateFollder(BaseModel):
    title: str 

class FolderResponse(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True

@app.post("/folders", response_model=FolderResponse)
async def create_folder(new_folder_request:CreateFollder, db_session:Session = Depends(get_db)):
    new_folder = FolderModel(title = new_folder_request.title)
    db_session.add(new_folder)
    db_session.commit()
    return new_folder

@app.get("/folders/{folder_id}")
async def get_folder(folder_id:int, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder == None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder

class UpdateFolder(BaseModel):
    title: str

@app.put("/folders/{folder_id}", response_model=FolderResponse)
async def update_folder(folder_id:int, update_folder_request:UpdateFolder, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder == None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    folder.title = update_folder_request.title
    db_session.add(folder)
    db_session.commit()
    return folder

@app.delete("/folders/{folder_id}")
async def delete_folder(folder_id:int, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder == None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    folder.is_deleted = True
    db_session.add(folder) 
    db_session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/folders/{folder_id}/items")
async def get_folder_items(folder_id:int, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder == None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    todo_items = db_session.query(TodoItemModel).filter(TodoItemModel.folder_id == folder_id, TodoItemModel.is_deleted == False).all()
    return todo_items

class CreateItem(BaseModel):
    title: str

class ItemResponse(BaseModel):
    id: int
    title: str
    folder_id: int

    class Config:
        from_attributes = True

@app.post("/folders/{folder_id}/items", response_model=ItemResponse)
async def create_new_item(folder_id:int, new_item_request:CreateItem, db_session:Session = Depends(get_db)):
    folder = db_session.query(FolderModel).filter(FolderModel.id == folder_id).first()
    if folder == None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    add_new_item = TodoItemModel(title = new_item_request.title, folder_id = folder_id)
    db_session.add(add_new_item)
    db_session.commit()
    return add_new_item 

@app.get("/folders/{folder_id}/items/{item_id}")
async def get_folder_item(folder_id:int, item_id:int, db_session:Session = Depends(get_db)):
    folder = db_session.query(FolderModel).filter(FolderModel.id == folder_id).first()
    if folder == None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = db_session.query(TodoItemModel).filter(
        TodoItemModel.folder_id == folder_id, 
        TodoItemModel.id == item_id, 
    ).first()
    if item == None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

class UpdateItem(BaseModel):
    title: str

@app.put("/folders/{folder_id}/items/{item_id}")
async def update_item(folder_id:int, item_id:int, update_item_request:UpdateItem, db_session:Session = Depends(get_db)):
    folder = folder_manager.get_folder(folder_id)
    if folder == None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = folder.edit_item_within_folder(item_id, updated_title = update_item_request.title)    
    if item == None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/folders/{folder_id}/items/{item_id}")
async def delete_item(folder_id:int, item_id:int, db_session:Session = Depends(get_db)):
    folder = db_session.get(FolderModel, folder_id)
    if folder == None or folder.is_deleted:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = db_session.query(TodoItemModel).filter(
        TodoItemModel.folder_id == folder_id, 
        TodoItemModel.id == item_id, 
    ).first()
    if item == None or item.is_deleted:
        raise HTTPException(status_code=404, detail="Item not found")
    item.is_deleted = True
    db_session.add(item) 
    db_session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


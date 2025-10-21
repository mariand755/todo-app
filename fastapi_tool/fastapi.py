from fastapi import FastAPI, HTTPException, Response, status
from library.folder_manager import FolderManager
from pydantic import BaseModel


app = FastAPI()
folder_manager = FolderManager()


@app.get("/folders")
async def get_folders():
    folders = folder_manager.get_folders()
    return folders

class CreateFollder(BaseModel):
    title: str 

@app.post("/folders")
async def create_folder(new_folder_request:CreateFollder):
    new_folder = folder_manager.add_folder(new_folder_request.title)
    return new_folder

@app.get("/folders/{folder_id}")
async def get_folder(folder_id:int):
    folder = folder_manager.get_folder(folder_id)
    if folder == None:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder

class UpdateFolder(BaseModel):
    title: str

@app.put("/folders/{folder_id}")
async def update_folder(folder_id:int, update_folder_request:UpdateFolder):
    folder = folder_manager.edit_folder_within_app(folder_id, updated_title = update_folder_request.title)    
    if folder == None:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder

@app.delete("/folders/{folder_id}")
async def delete_folder(folder_id:int):
    folder = folder_manager.get_folder(folder_id)
    if folder == None:
        raise HTTPException(status_code=404, detail="Folder not found")
    folder_manager.remove_folder_within_app(folder_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/folders/{folder_id}/items")
async def get_folder_items(folder_id:int):
    folder = folder_manager.get_folder(folder_id)
    if folder == None:
        raise HTTPException(status_code=404, detail="Folder not found")
    return folder.get_items()

class CreateItem(BaseModel):
    title: str

@app.post("/folders/{folder_id}/items")
async def create_new_item(folder_id:int, new_item_request:CreateItem):
    folder = folder_manager.get_folder(folder_id)
    if folder == None:
        raise HTTPException(status_code=404, detail="Folder not found")
    return  folder.add_new_item_to_folder(new_item_title=new_item_request.title)

@app.get("/folders/{folder_id}/items/{item_id}")
async def get_folder_item(folder_id:int, item_id:int):
    folder = folder_manager.get_folder(folder_id)
    if folder == None:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = folder.get_item(item_id)
    if item == None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

class UpdateItem(BaseModel):
    title: str

@app.put("/folders/{folder_id}/items/{item_id}")
async def update_item(folder_id:int, item_id:int, update_item_request:UpdateItem):
    folder = folder_manager.get_folder(folder_id)
    if folder == None:
        raise HTTPException(status_code=404, detail="Folder not found")
    item = folder.edit_item_within_folder(item_id, updated_title = update_item_request.title)    
    if item == None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.delete("/folders/{folder_id}/items/{item_id}")
async def delete_item(folder_id:int, item_id:int):
    folder = folder_manager.get_folder(folder_id)
    if folder == None:
        raise HTTPException(status_code=404, detail="Folder not found")
    folder.remove_item_within_folder(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


from fastapi import FastAPI
from library.folder_manager import FolderManager
from library.folder import Folder
from pydantic import BaseModel


app = FastAPI()
folder_manager = FolderManager()

@app.get("/")
async def root():
    return {"message": "Hello World"}

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

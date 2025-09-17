from library.folder import Folder
from typing import List, Dict


class FolderManager:
    def __init__(self):
        self.folders: List[Folder] = []
        self.__new_folder_id = 1 

    def add_folder(self, folder_title:str):
        new_folder = Folder(
            id = self.__new_folder_id, 
            title = folder_title 
        )
        self.folders.append(new_folder)
        self.__new_folder_id +=1 
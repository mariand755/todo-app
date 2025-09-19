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
    
    def list_folders_within_app(self): #class functions take a "self" parameter
        for folder in self.folders:
            print(folder)
    
    def edit_folders_within_app(self, find_id_of_folders:Dict[int, str]):
        if len(self.folders) == 0:
            return
        id_array = find_id_of_folders.keys()
        for id in id_array:
            updated_title = find_id_of_folders[id]
            self.edit_folder_within_app(id, updated_title)

    def edit_folder_within_app(self, id_to_edit:int, updated_title:str):
        index_to_edit = self.__find_index(id_to_edit)
        if index_to_edit != -1:
            self.folders[index_to_edit].title = updated_title
  
    def __find_index(self, id_to_find:int):
        index_to_find = -1
        for index, item in enumerate(self.folders):
            if item.id == id_to_find:
                index_to_find = index
        return index_to_find

    def does_folder_exist(self, existing_id_to_find:int)-> bool:
        existing_index_to_find = self.__find_index(existing_id_to_find)
        return existing_index_to_find != -1
    
    def remove_folders_within_app(self, ids_to_remove:List[int]):
        if len(self.folders) == 0:
            return
        for id in ids_to_remove:
            self.remove_folder_within_app(id)

    def remove_folder_within_app(self, id_to_remove:int):
        index_to_remove = self.__find_index(id_to_remove)
        if index_to_remove != -1:
            del self.folders[index_to_remove]

    def search_for_folders_using_title(self, title_to_find:str)->List[Folder]:
        results = []
        lowercase_title = title_to_find.lower().strip()
        for folder in self.folders:
            #searching usng prefix search
            if folder.title.lower().startswith(lowercase_title):
                results.append(folder)
        return results
from library.todo_item import TodoItem
from typing import List, Dict


class Folder:
    def __init__(self, id:int, title:str):
        self.id = id
        self.title = title
        self.items:List[TodoItem] = []


    def add_new_items_to_folder(self, new_items:List[TodoItem]):
        for item in new_items:
            id_exist = self.__find_index(item.id) != -1
            if id_exist:
                print(f"Skipping {item} because id={item.id} already exist")
            else:
                self.items.append(item)

    def list_items_within_folder(self):
        print(self.title)
        for item in self.items:
            print(f"{item}")

    def remove_items_within_folder(self, ids_to_remove:List[int]):
        if len(self.items) == 0:
            return
        for id in ids_to_remove:
            self.remove_item_within_folder(id)


    def remove_item_within_folder(self, id_to_remove:int):
        index_to_remove = self.__find_index(id_to_remove)
        if index_to_remove != -1:
            del self.items[index_to_remove]

    
    def edit_items_within_folder(self, find_id_of_items:Dict[int, str]):
        if len(self.items) == 0:
            return
        id_array = find_id_of_items.keys()
        for id in id_array:
            updated_title = find_id_of_items[id]
            self.edit_item_within_folder(id, updated_title)
        
    def edit_item_within_folder(self, id_to_edit:int, updated_title:str):
        index_to_edit = self.__find_index(id_to_edit)
        if index_to_edit != -1:
            self.items[index_to_edit].title = updated_title


    def search_for_item_in_folder(self, id_to_find:int):
        index_to_find = self.__find_index(id_to_find)
        if index_to_find != -1:
            return self.items[index_to_find]
        return None

    def __find_index(self, id_to_find:int):
        index_to_find = -1
        for index, item in enumerate(self.items):
            if item.id == id_to_find:
                index_to_find = index
        return index_to_find
    
    def does_item_exist(self, existing_id_to_find:int)-> bool:
        existing_index_to_find = self.__find_index(existing_id_to_find)
        return existing_index_to_find != -1
    
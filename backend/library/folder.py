from typing import Dict, List, Union

from colorist import Color, effect_bold

from library.todo_item import TodoItem


class FolderConstants:
    ERR_NON_STR_INPUT = "input is not a string"
    ERR_EMPTY_STR_INPUT = "input is empty"
    ERR_ITEMS_NOT_ARRAY = "input is not array"


class Folder:
    def __init__(self, id: int, title: str):
        self.id = id
        self.title = title
        self.items: List[TodoItem] = []
        self.__new_id = 1

    def __str__(self):
        return f"ID {self.id}: {self.title}"

    def add_new_items_to_folder(self, new_items: List[str]):
        if isinstance(new_items, list) is False:
            raise ValueError(FolderConstants.ERR_ITEMS_NOT_ARRAY)
        for item in new_items:
            self.add_new_item_to_folder(item)

    def add_new_item_to_folder(self, new_item_title: str):
        if isinstance(new_item_title, str) is False:
            raise ValueError(FolderConstants.ERR_NON_STR_INPUT)
        stripped_title = new_item_title.strip()
        if stripped_title == "":
            raise ValueError(FolderConstants.ERR_EMPTY_STR_INPUT)
        new_item = TodoItem(id=self.__new_id, title=stripped_title)
        self.items.append(new_item)
        self.__new_id += 1
        return new_item

    def list_items_within_folder(self):
        effect_bold(f"{Color.BLUE}{self.title}{Color.OFF}")
        for item in self.items:
            print(f"{item}")

    def remove_items_within_folder(self, ids_to_remove: List[int]):
        if len(self.items) == 0:
            return
        for id in ids_to_remove:
            self.remove_item_within_folder(id)

    def remove_item_within_folder(self, id_to_remove: int):
        index_to_remove = self.__find_index(id_to_remove)
        if index_to_remove != -1:
            del self.items[index_to_remove]

    def edit_items_within_folder(self, find_id_of_items: Dict[int, str]):
        if len(self.items) == 0:
            return
        id_array = find_id_of_items.keys()
        for id in id_array:
            updated_title = find_id_of_items[id]
            self.edit_item_within_folder(id, updated_title)

    def edit_item_within_folder(self, id_to_edit: int, updated_title: str):
        if isinstance(updated_title, str) is False:
            raise ValueError(FolderConstants.ERR_NON_STR_INPUT)
        stripped_title = updated_title.strip()
        if stripped_title == "":
            raise ValueError(FolderConstants.ERR_EMPTY_STR_INPUT)
        index_to_edit = self.__find_index(id_to_edit)
        if index_to_edit != -1:
            self.items[index_to_edit].title = stripped_title
            return self.items[index_to_edit]
        return None

    def __find_index(self, id_to_find: int):
        index_to_find = -1
        for index, item in enumerate(self.items):
            if item.id == id_to_find:
                index_to_find = index
        return index_to_find

    def does_item_exist(self, existing_id_to_find: int) -> bool:
        existing_index_to_find = self.__find_index(existing_id_to_find)
        return existing_index_to_find != -1

    def get_items(self) -> List[TodoItem]:
        return self.items

    def get_item(self, id: int) -> Union[TodoItem, None]:
        item_index_to_find = self.__find_index(id)
        if item_index_to_find != -1:
            return self.items[item_index_to_find]
        else:
            return None

    def search_for_items_using_title(self, title_to_find: str) -> List[TodoItem]:
        results: List[TodoItem] = []
        lowercase_title = title_to_find.lower().strip()
        if lowercase_title == "":
            return results
        for item in self.items:
            # searching usng prefix search
            if item.title.lower().startswith(lowercase_title):
                results.append(item)
        return results

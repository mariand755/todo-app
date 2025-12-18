from library.folder import Folder
from library.folder_manager import FolderManager, FolderManagerConstants
import pytest

@pytest.fixture
def test_folder_manager():
    new_folder_manager = FolderManager()
    return new_folder_manager

# happy path
def test_add_folder_success(test_folder_manager:FolderManager):
    #arrange
    add_newfolder = "New Test Folder"
    #act
    new_folder = test_folder_manager.add_folder(add_newfolder)

    #assert
    assert 1 == len(test_folder_manager.folders)
    assert add_newfolder == new_folder.title

# error handling
def test_add_folder_non_str_title_raise_exception(test_folder_manager:FolderManager):
    #arrange
    add_non_str_folder = []

    #act / assert
    with pytest.raises(ValueError) as e:
        test_folder_manager.add_folder(add_non_str_folder)
    assert FolderManagerConstants.ERR_ADD_FOLDER_NON_STR == e.value.args[0]


# edge case
def test_add_folder_empty_title_raise_exception(test_folder_manager:FolderManager):
    #arrange
    add_empty_folder = ""

    #act / assert
    with pytest.raises(ValueError) as e:
        test_folder_manager.add_folder(add_empty_folder)
    assert FolderManagerConstants.ERR_EMPTY_FOLDER == e.value.args[0]




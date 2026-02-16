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


def test_add_folder_whitespace_only_raises_exception(test_folder_manager:FolderManager):
    # arrange
    whitespace_title = "   "

    # act / assert
    with pytest.raises(ValueError) as e:
        test_folder_manager.add_folder(whitespace_title)
    assert FolderManagerConstants.ERR_EMPTY_FOLDER == e.value.args[0]


def test_edit_folder_within_app_success_updates_title(test_folder_manager:FolderManager):
    # arrange
    f = test_folder_manager.add_folder("Orig")  # id 1

    # act
    updated = test_folder_manager.edit_folder_within_app(f.id, "New Title")

    # assert
    assert updated is not None
    assert updated.title == "New Title"


def test_edit_folder_within_app_nonexistent_returns_none(test_folder_manager:FolderManager):
    # arrange - no folders

    # act
    result = test_folder_manager.edit_folder_within_app(999, "Nope")

    # assert
    assert result is None


def test_edit_folders_within_app_batch_updates_and_skips_missing(test_folder_manager:FolderManager):
    # arrange
    test_folder_manager.add_folder("A")  # id 1
    test_folder_manager.add_folder("B")  # id 2

    # act
    test_folder_manager.edit_folders_within_app({1: "AA", 2: "BB", 99: "X"})

    # assert
    assert test_folder_manager.get_folder(1).title == "AA"
    assert test_folder_manager.get_folder(2).title == "BB"
    assert test_folder_manager.get_folder(99) is None


def test_edit_folder_within_app_non_str_raises_error(test_folder_manager:FolderManager):
    # arrange
    f=test_folder_manager.add_folder("one")  # id 1

    # act / assert
    with pytest.raises(ValueError) as e:
        test_folder_manager.edit_folder_within_app(f.id, 123)
    assert FolderManagerConstants.ERR_ADD_FOLDER_NON_STR == e.value.args[0]


def test_edit_folder_within_app_empty_str_raises_error(test_folder_manager:FolderManager):
    # arrange
    f = test_folder_manager.add_folder("one")  # id 1

    # act / assert
    with pytest.raises(ValueError) as e:
        test_folder_manager.edit_folder_within_app(f.id, "   ")
    assert FolderManagerConstants.ERR_EMPTY_FOLDER == e.value.args[0]


def test_remove_folder_within_app_success(test_folder_manager:FolderManager):
    # arrange
    test_folder_manager.add_folder("one")  # id 1
    test_folder_manager.add_folder("two")  # id 2

    # act
    test_folder_manager.remove_folder_within_app(1)

    # assert
    remaining_ids = [f.id for f in test_folder_manager.folders]
    assert len(remaining_ids) == 1
    assert 1 not in remaining_ids


def test_remove_folder_within_app_nonexistent_id_no_change(test_folder_manager:FolderManager):
    # arrange
    test_folder_manager.add_folder("only")  # id 1

    # act
    test_folder_manager.remove_folder_within_app(99)  # no-op

    # assert
    assert len(test_folder_manager.folders) == 1
    assert test_folder_manager.folders[0].title == "only"


def test_remove_folders_within_app_success_and_skips_missing(test_folder_manager:FolderManager):
    # arrange
    test_folder_manager.add_folder("one")   # id 1
    test_folder_manager.add_folder("two")   # id 2
    test_folder_manager.add_folder("three") # id 3

    # act
    test_folder_manager.remove_folders_within_app([1, 3, 99])

    # assert
    remaining_titles = [i.title for i in test_folder_manager.folders]
    assert remaining_titles == ["two"]


def test_remove_folders_within_app_on_empty_manager_is_noop(test_folder_manager:FolderManager):
    # arrange - manager starts empty

    # act (should not raise)
    test_folder_manager.remove_folders_within_app([1, 2])

    # assert
    assert test_folder_manager.folders == []


def test_does_any_any_folder_exist_true_and_false(test_folder_manager:FolderManager):
    # arrange
    test_folder_manager.add_folder("exists")  # id 1

    # act / assert
    assert test_folder_manager.does_any_folder_exist_in_foldermanager() is True
    assert test_folder_manager.does_folder_exist(1) is True
    assert test_folder_manager.does_folder_exist(999) is False


def test_get_folders_works_and_if_folder_do_not_exist_it_skips(test_folder_manager:FolderManager):
    # arrange
    test_folder_manager.add_folder("x")  # id 1
    test_folder_manager.add_folder("y")  # id 2

    # act / assert
    assert isinstance(test_folder_manager.get_folders(), list)
    assert test_folder_manager.get_folder(99) is None

def test_get_folder_work(test_folder_manager:FolderManager):
    # arrange
    test_folder_manager.add_folder("x")  # id 1
    test_folder_manager.add_folder("y")  # id 2

    # act / assert
    assert test_folder_manager.get_folder(2).title == "y"

"""
def test_search_for_folders_using_title_prefix_case_insensitive_and_trimming(test_folder_manager:FolderManager):
    # arrange
    test_folder_manager.add_folder("Alpha One")
    test_folder_manager.add_folder("Alpine")
    test_folder_manager.add_folder("beta")

    # act
    results = test_folder_manager.search_for_folders_using_title("  al ")

    # assert
    titles = [r.title for r in results]
    assert "Alpha One" in titles and "Alpine" in titles
    assert len(titles) == 2


def test_search_for_folders_using_title_non_str_raises_error(test_folder_manager:FolderManager):
    # arrange
    test_folder_manager.add_folder("one")

    # act / assert
    with pytest.raises(ValueError) as e:
        test_folder_manager.search_for_folders_using_title(123)
    assert FolderManagerConstants.ERR_ADD_FOLDER_NON_STR == e.value.args[0]


def test_search_for_folders_using_title_empty_returns_no_results(test_folder_manager:FolderManager):
    # arrange
    test_folder_manager.add_folder("one")
    test_folder_manager.add_folder("two")

    # act
    results = test_folder_manager.search_for_folders_using_title("   ")

    # assert
    assert results == []
"""

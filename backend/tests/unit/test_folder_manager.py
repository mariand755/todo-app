import pytest

from library.folder_manager import FolderManager, FolderManagerConstants


@pytest.fixture
def test_folder_manager():
    return FolderManager()


# Adding a valid folder title should create the folder and return it.
@pytest.mark.BUT19
def test_add_folder_success(test_folder_manager: FolderManager):
    # arrange
    add_newfolder = "New Test Folder"
    # act
    new_folder = test_folder_manager.add_folder(add_newfolder)

    # assert
    assert 1 == len(test_folder_manager.folders)
    assert add_newfolder == new_folder.title


# Passing a non-string (like a list) as the title should raise a ValueError.
@pytest.mark.BUT20
def test_add_folder_non_str_title_raise_exception(test_folder_manager: FolderManager):
    # arrange
    add_non_str_folder: list[any] = []

    # act / assert
    with pytest.raises(ValueError) as e:
        test_folder_manager.add_folder(add_non_str_folder)
    assert FolderManagerConstants.ERR_ADD_FOLDER_NON_STR == e.value.args[0]


# An empty string title is not acceptable and should raise a ValueError.
@pytest.mark.BUT21
def test_add_folder_empty_title_raise_exception(test_folder_manager: FolderManager):
    # arrange
    add_empty_folder = ""

    # act / assert
    with pytest.raises(ValueError) as e:
        test_folder_manager.add_folder(add_empty_folder)
    assert FolderManagerConstants.ERR_EMPTY_FOLDER == e.value.args[0]


# Whitespace-only titles are treated the same as empty and should be rejected.
@pytest.mark.BUT22
def test_add_folder_whitespace_only_raises_exception(test_folder_manager: FolderManager):
    # arrange
    whitespace_title = "   "

    # act / assert
    with pytest.raises(ValueError) as e:
        test_folder_manager.add_folder(whitespace_title)
    assert FolderManagerConstants.ERR_EMPTY_FOLDER == e.value.args[0]


# Renaming an existing folder should update its title and return the folder.
@pytest.mark.BUT23
def test_edit_folder_within_app_success_updates_title(test_folder_manager: FolderManager):
    # arrange
    f = test_folder_manager.add_folder("Orig")  # id 1

    # act
    updated = test_folder_manager.edit_folder_within_app(f.id, "New Title")

    # assert
    assert updated is not None
    assert updated.title == "New Title"


# Editing a folder id that does not exist should return None without raising.
@pytest.mark.BUT24
def test_edit_folder_within_app_nonexistent_returns_none(test_folder_manager: FolderManager):
    # arrange - no folders

    # act
    result = test_folder_manager.edit_folder_within_app(999, "Nope")

    # assert
    assert result is None


# Batch edit should update all matching ids and silently skip ids that are missing.
@pytest.mark.BUT25
def test_edit_folders_within_app_batch_updates_and_skips_missing(
    test_folder_manager: FolderManager,
):
    # arrange
    test_folder_manager.add_folder("A")  # id 1
    test_folder_manager.add_folder("B")  # id 2

    # act
    test_folder_manager.edit_folders_within_app({1: "AA", 2: "BB", 99: "X"})

    # assert
    assert test_folder_manager.get_folder(1).title == "AA"
    assert test_folder_manager.get_folder(2).title == "BB"
    assert test_folder_manager.get_folder(99) is None


# Passing a non-string as the new title should raise a ValueError regardless of id.
@pytest.mark.BUT26
def test_edit_folder_within_app_non_str_raises_error(test_folder_manager: FolderManager):
    # arrange
    f = test_folder_manager.add_folder("one")  # id 1

    # act / assert
    with pytest.raises(ValueError) as e:
        test_folder_manager.edit_folder_within_app(f.id, 123)
    assert FolderManagerConstants.ERR_ADD_FOLDER_NON_STR == e.value.args[0]


# A blank or whitespace-only new title should be rejected with the empty-folder error.
@pytest.mark.BUT27
def test_edit_folder_within_app_empty_str_raises_error(test_folder_manager: FolderManager):
    # arrange
    f = test_folder_manager.add_folder("one")  # id 1

    # act / assert
    with pytest.raises(ValueError) as e:
        test_folder_manager.edit_folder_within_app(f.id, "   ")
    assert FolderManagerConstants.ERR_EMPTY_FOLDER == e.value.args[0]


# Removing a folder by id should remove only that folder, leaving the rest intact.
@pytest.mark.BUT28
def test_remove_folder_within_app_success(test_folder_manager: FolderManager):
    # arrange
    test_folder_manager.add_folder("one")  # id 1
    test_folder_manager.add_folder("two")  # id 2

    # act
    test_folder_manager.remove_folder_within_app(1)

    # assert
    remaining_ids = [f.id for f in test_folder_manager.folders]
    assert len(remaining_ids) == 1
    assert 1 not in remaining_ids


# Removing an id that does not exist should be a no-op with no side effects.
@pytest.mark.BUT29
def test_remove_folder_within_app_nonexistent_id_no_change(test_folder_manager: FolderManager):
    # arrange
    test_folder_manager.add_folder("only")  # id 1

    # act
    test_folder_manager.remove_folder_within_app(99)  # no-op

    # assert
    assert len(test_folder_manager.folders) == 1
    assert test_folder_manager.folders[0].title == "only"


# Bulk removal should delete the matching ids and silently skip unknown ones.
@pytest.mark.BUT30
def test_remove_folders_within_app_success_and_skips_missing(test_folder_manager: FolderManager):
    # arrange
    test_folder_manager.add_folder("one")  # id 1
    test_folder_manager.add_folder("two")  # id 2
    test_folder_manager.add_folder("three")  # id 3

    # act
    test_folder_manager.remove_folders_within_app([1, 3, 99])

    # assert
    remaining_titles = [i.title for i in test_folder_manager.folders]
    assert remaining_titles == ["two"]


# Bulk remove on a manager with no folders should complete without errors.
@pytest.mark.BUT31
def test_remove_folders_within_app_on_empty_manager_is_noop(test_folder_manager: FolderManager):
    # arrange - manager starts empty

    # act (should not raise)
    test_folder_manager.remove_folders_within_app([1, 2])

    # assert
    assert test_folder_manager.folders == []


# Existence checks should correctly reflect what the manager actually holds.
@pytest.mark.BUT32
def test_folder_existence_checks_return_correct_booleans(test_folder_manager: FolderManager):
    # arrange
    test_folder_manager.add_folder("exists")  # id 1

    # act / assert
    assert test_folder_manager.does_any_folder_exist_in_foldermanager() is True
    assert test_folder_manager.does_folder_exist(1) is True
    assert test_folder_manager.does_folder_exist(999) is False


# get_folders returns a list; get_folder returns None for ids that are missing.
@pytest.mark.BUT33
def test_get_folders_and_get_folder_behavior(test_folder_manager: FolderManager):
    # arrange
    test_folder_manager.add_folder("x")  # id 1
    test_folder_manager.add_folder("y")  # id 2

    # act / assert
    assert isinstance(test_folder_manager.get_folders(), list)
    assert test_folder_manager.get_folder(99) is None


# Fetching a folder by a valid id should return the correct folder object.
@pytest.mark.BUT34
def test_get_folder_returns_correct_folder(test_folder_manager: FolderManager):
    # arrange
    test_folder_manager.add_folder("x")  # id 1
    test_folder_manager.add_folder("y")  # id 2

    # act / assert
    assert test_folder_manager.get_folder(2).title == "y"

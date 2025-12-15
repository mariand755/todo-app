from library.folder import Folder 
import pytest

# Fixture
@pytest.fixture
def test_folder():
    dummy_id = 1
    dummy_title = "folder_test"

    t_f = Folder(dummy_id, dummy_title)
    return t_f



# happy path first
def test_add_new_items_to_folder_success(test_folder):
    # arrange
    test_items = ["test_item1", "test_item2", "test_item3"]

    # act
    test_folder.add_new_items_to_folder(test_items)

    # assert
    expected = len(test_items)
    actual = len(test_folder.items)
    assert expected == actual

# error handling
def test_add_new_items_to_folder_non_array_input_throws_exception(test_folder):
    # arrange
    test_items_not_array = {}

    # act / assert
    with pytest.raises(ValueError):
        test_folder.add_new_items_to_folder(test_items_not_array)
    

# edge case
def test_add_new_items_to_folder_empty_array_adds_no_items(test_folder):
    # arrange
    test_items_empty_array = []

    # act
    test_folder.add_new_items_to_folder(test_items_empty_array)

    # assert
    expected = 0
    actual = len(test_folder.items)
    assert expected == actual
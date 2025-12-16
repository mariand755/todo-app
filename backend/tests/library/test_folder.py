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

# happy path
def test_add_new_item_to_folder_success(test_folder):
    #arrange
    test_item = "test_item1"

    #act
    test_folder.add_new_item_to_folder(test_item)
    #assert
    excepted = 1
    actual = len(test_folder.items)
    assert excepted == actual

# error handling
def test_add_new_item_to_folder_non_str_inputs_raises_error(test_folder):
    #arrange
    non_str_input = ()

    #act /assert
    with pytest.raises(ValueError):
        test_folder.add_new_item_to_folder(non_str_input)
  
# edge case
def test_add_new_item_to_folder_empty_str_inputs_raises_error(test_folder):
    #arrange
    empty_str_input = ""

    #act /assert
    with pytest.raises(ValueError) as err:
        test_folder.add_new_item_to_folder(empty_str_input)
    assert "input is empty" == err.value.args[0]
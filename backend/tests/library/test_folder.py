from library.folder import Folder, FolderConstants 
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
    items_not_array = {}

    # act / assert
    with pytest.raises(ValueError) as err:
        test_folder.add_new_items_to_folder(items_not_array)
    assert FolderConstants.ERR_ITEMS_NOT_ARRAY ==  err.value.args[0]
    
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
    with pytest.raises(ValueError) as err:
        test_folder.add_new_item_to_folder(non_str_input)
    assert FolderConstants.ERR_NON_STR_INPUT == err.value.args[0]
  
# edge case
def test_add_new_item_to_folder_empty_str_inputs_raises_error(test_folder):
    #arrange
    empty_str_input = ""

    #act /assert
    with pytest.raises(ValueError) as err:
        test_folder.add_new_item_to_folder(empty_str_input)
    assert FolderConstants.ERR_EMPTY_STR_INPUT == err.value.args[0]



def test_remove_item_within_folder_success(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("a")  # id 1
    test_folder.add_new_item_to_folder("b")  # id 2
    test_folder.add_new_item_to_folder("c")  # id 3

    # act
    test_folder.remove_item_within_folder(2)

    # assert
    remaining_ids = [item.id for item in test_folder.items]
    assert len(remaining_ids) == 2
    assert 2 not in remaining_ids


def test_remove_item_within_folder_nonexistent_id_no_change(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("only")  # id 1

    # act
    test_folder.remove_item_within_folder(99)  # no-op

    # assert
    assert len(test_folder.items) == 1
    assert test_folder.items[0].title == "only"


def test_remove_items_within_folder_success(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("one")   # id 1
    test_folder.add_new_item_to_folder("two")   # id 2
    test_folder.add_new_item_to_folder("three") # id 3

    # act
    test_folder.remove_items_within_folder([1, 3])

    # assert
    remaining_titles = [i.title for i in test_folder.items]
    assert remaining_titles == ["two"]


def test_remove_items_within_folder_on_empty_folder_is_noop(test_folder):
    # arrange - folder starts empty

    # act (should not raise)
    test_folder.remove_items_within_folder([1, 2])

    # assert
    assert test_folder.items == []


def test_edit_item_within_folder_success(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("old")  # id 1

    # act
    updated = test_folder.edit_item_within_folder(1, "new")

    # assert
    assert updated is not None
    assert updated.title == "new"
    assert test_folder.get_item(1).title == "new"


def test_edit_item_within_folder_nonexistent_returns_none(test_folder):
    # arrange - empty folder

    # act
    result = test_folder.edit_item_within_folder(999, "nope")

    # assert
    assert result is None


def test_edit_items_within_folder_success_and_skips_missing(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("a")  # id 1
    test_folder.add_new_item_to_folder("b")  # id 2

    # act - also include a non-existing id (99) which should be skipped silently
    test_folder.edit_items_within_folder({1: "A", 2: "B", 99: "X"})

    # assert
    assert test_folder.get_item(1).title == "A"
    assert test_folder.get_item(2).title == "B"


def test_does_item_exist_true_and_false(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("exists")  # id 1

    # act / assert
    assert test_folder.does_item_exist(1) is True
    assert test_folder.does_item_exist(999) is False


def test_get_items_and_get_item_are_in_listformat(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("x")  # id 1
    test_folder.add_new_item_to_folder("y")  # id 2

    # act
    items = test_folder.get_items()

    # assert
    assert isinstance(items, list)

def test_get_items_and_get_item_num_in_folder(test_folder:Folder):
    # arrange
    test_folder.add_new_item_to_folder("x")  # id 1
    test_folder.add_new_item_to_folder("y")  # id 2

    # act
    items = test_folder.get_items()

    # assert
    assert len(items) == 2


def test__get_item_not_empty(test_folder:Folder):
    # arrange
    test_folder.add_new_item_to_folder("x")  # id 1
    test_folder.add_new_item_to_folder("y")  # id 2

    # act
    item = test_folder.get_item(id=2)

    # assert
    assert item is not None and item.title == "y"

def test_get_item_none_existing_item_fails_silently(test_folder:Folder):
    # arrange
    test_folder.add_new_item_to_folder("x")  # id 1
    test_folder.add_new_item_to_folder("y")  # id 2

    # act
    missing = test_folder.get_item(99)

    # assert
    assert missing is None

"""
def test_search_for_item_in_folder_and_none(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("first")  # id 1
    test_folder.add_new_item_to_folder("second") # id 2

    # act / assert
    assert test_folder.search_for_item_in_folder(2).title == "second"
    assert test_folder.search_for_item_in_folder(99) is None


def test_search_for_items_using_title_prefix_case_insensitive(test_folder):
    # arrange
    # Note: search uses prefix matching (startswith) and should be case-insensitive and trimmed
    test_folder.add_new_item_to_folder("Alpha One")
    test_folder.add_new_item_to_folder("Alpine")
    test_folder.add_new_item_to_folder("beta")

    # act
    results = test_folder.search_for_items_using_title("  al ")

    # assert - should find the two "Al" matches
    titles = [r.title for r in results]
    assert "Alpha One" in titles and "Alpine" in titles
    assert len(titles) == 2
"""
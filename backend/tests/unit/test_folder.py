import pytest

from library.folder import Folder, FolderConstants


@pytest.fixture
def test_folder():
    return Folder(1, "folder_test")


# Adding multiple items at once should store all of them in the folder.
@pytest.mark.BUT01
def test_add_new_items_to_folder_success(test_folder):
    # arrange
    test_items = ["test_item1", "test_item2", "test_item3"]

    # act
    test_folder.add_new_items_to_folder(test_items)

    # assert
    expected = len(test_items)
    actual = len(test_folder.items)
    assert expected == actual


# Passing something that is not a list should be rejected immediately.
@pytest.mark.BUT02
def test_add_new_items_to_folder_non_array_input_throws_exception(test_folder):
    # arrange
    items_not_array = {}

    # act / assert
    with pytest.raises(ValueError) as err:
        test_folder.add_new_items_to_folder(items_not_array)
    assert FolderConstants.ERR_ITEMS_NOT_ARRAY == err.value.args[0]


# An empty list is valid input; it just means nothing gets added to the folder.
@pytest.mark.BUT03
def test_add_new_items_to_folder_empty_array_adds_no_items(test_folder):
    # arrange
    test_items_empty_array = []

    # act
    test_folder.add_new_items_to_folder(test_items_empty_array)

    # assert
    expected = 0
    actual = len(test_folder.items)
    assert expected == actual


# Adding a single valid string item should increase the item count by one.
@pytest.mark.BUT04
def test_add_new_item_to_folder_success(test_folder):
    # arrange
    test_item = "test_item1"

    # act
    test_folder.add_new_item_to_folder(test_item)
    # assert
    excepted = 1
    actual = len(test_folder.items)
    assert excepted == actual


# Non-string input (like a tuple) should raise a ValueError with the right message.
@pytest.mark.BUT05
def test_add_new_item_to_folder_non_str_inputs_raises_error(test_folder):
    # arrange
    non_str_input = ()

    # act /assert
    with pytest.raises(ValueError) as err:
        test_folder.add_new_item_to_folder(non_str_input)
    assert FolderConstants.ERR_NON_STR_INPUT == err.value.args[0]


# An empty string title is not a valid item name and should be rejected.
@pytest.mark.BUT06
def test_add_new_item_to_folder_empty_str_inputs_raises_error(test_folder):
    # arrange
    empty_str_input = ""

    # act /assert
    with pytest.raises(ValueError) as err:
        test_folder.add_new_item_to_folder(empty_str_input)
    assert FolderConstants.ERR_EMPTY_STR_INPUT == err.value.args[0]


# Removing an item by id should leave all remaining items in place.
@pytest.mark.BUT07
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


# Removing a non-existent id should not raise and should leave the folder unchanged.
@pytest.mark.BUT08
def test_remove_item_within_folder_nonexistent_id_no_change(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("only")  # id 1

    # act
    test_folder.remove_item_within_folder(99)  # no-op

    # assert
    assert len(test_folder.items) == 1
    assert test_folder.items[0].title == "only"


# Bulk removal should drop only the specified ids and leave everything else.
@pytest.mark.BUT09
def test_remove_items_within_folder_success(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("one")  # id 1
    test_folder.add_new_item_to_folder("two")  # id 2
    test_folder.add_new_item_to_folder("three")  # id 3

    # act
    test_folder.remove_items_within_folder([1, 3])

    # assert
    remaining_titles = [i.title for i in test_folder.items]
    assert remaining_titles == ["two"]


# Bulk remove on an empty folder should complete without errors.
@pytest.mark.BUT10
def test_remove_items_within_folder_on_empty_folder_is_noop(test_folder):
    # arrange - folder starts empty

    # act (should not raise)
    test_folder.remove_items_within_folder([1, 2])

    # assert
    assert test_folder.items == []


# Editing an item should update its title and return the updated item object.
@pytest.mark.BUT11
def test_edit_item_within_folder_success(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("old")  # id 1

    # act
    updated = test_folder.edit_item_within_folder(1, "new")

    # assert
    assert updated is not None
    assert updated.title == "new"
    assert test_folder.get_item(1).title == "new"


# Editing an item id that does not exist should return None without raising.
@pytest.mark.BUT12
def test_edit_item_within_folder_nonexistent_returns_none(test_folder):
    # arrange - empty folder

    # act
    result = test_folder.edit_item_within_folder(999, "nope")

    # assert
    assert result is None


# Batch edit should update matching items and silently skip ids that are not found.
@pytest.mark.BUT13
def test_edit_items_within_folder_success_and_skips_missing(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("a")  # id 1
    test_folder.add_new_item_to_folder("b")  # id 2

    # act - also include a non-existing id (99) which should be skipped silently
    test_folder.edit_items_within_folder({1: "A", 2: "B", 99: "X"})

    # assert
    assert test_folder.get_item(1).title == "A"
    assert test_folder.get_item(2).title == "B"


# Existence checks should return the correct boolean for both known and unknown ids.
@pytest.mark.BUT14
def test_does_item_exist_true_and_false(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("exists")  # id 1

    # act / assert
    assert test_folder.does_item_exist(1) is True
    assert test_folder.does_item_exist(999) is False


# get_items should always return a list type, even when the folder is empty.
@pytest.mark.BUT15
def test_get_items_returns_a_list(test_folder):
    # arrange
    test_folder.add_new_item_to_folder("x")  # id 1
    test_folder.add_new_item_to_folder("y")  # id 2

    # act
    items = test_folder.get_items()

    # assert
    assert isinstance(items, list)


# The item count returned should match exactly how many items were added.
@pytest.mark.BUT16
def test_get_items_count_matches_what_was_added(test_folder: Folder):
    # arrange
    test_folder.add_new_item_to_folder("x")  # id 1
    test_folder.add_new_item_to_folder("y")  # id 2

    # act
    items = test_folder.get_items()

    # assert
    assert len(items) == 2


# Fetching by id should return the correct item with the expected title.
@pytest.mark.BUT17
def test_get_item_returns_correct_item(test_folder: Folder):
    # arrange
    test_folder.add_new_item_to_folder("x")  # id 1
    test_folder.add_new_item_to_folder("y")  # id 2

    # act
    item = test_folder.get_item(id=2)

    # assert
    assert item is not None and item.title == "y"


# Requesting an item id that does not exist should return None, not raise an exception.
@pytest.mark.BUT18
def test_get_item_nonexistent_returns_none(test_folder: Folder):
    # arrange
    test_folder.add_new_item_to_folder("x")  # id 1
    test_folder.add_new_item_to_folder("y")  # id 2

    # act
    missing = test_folder.get_item(99)

    # assert
    assert missing is None

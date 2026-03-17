from types import SimpleNamespace

import pytest

from app.api import apply_item_order_positions


def make_item(id, position=-1, title=None):
    return SimpleNamespace(id=id, position=position, title=title or f"item_{id}")


# When all item ids are in the order list, positions should map exactly from index 0.
@pytest.mark.BUT43
def test_apply_order_assigns_positions_matching_full_order():
    items = [make_item(i) for i in range(1, 5)]
    order = [4, 2, 3, 1]

    apply_item_order_positions(items, order)

    positions = {item.id: item.position for item in items}
    assert positions[4] == 0
    assert positions[2] == 1
    assert positions[3] == 2
    assert positions[1] == 3


# Items not included in the order list should be appended after the explicitly ordered ones.
@pytest.mark.BUT44
def test_apply_order_partial_list_appends_unlisted_items_at_the_end():
    items = [make_item(i) for i in range(1, 6)]
    order = [3, 1]

    apply_item_order_positions(items, order)

    positions = {item.id: item.position for item in items}
    assert positions[3] == 0
    assert positions[1] == 1
    # every unlisted item's position should be >= len(order)
    for i in [2, 4, 5]:
        assert positions[i] >= len(order)

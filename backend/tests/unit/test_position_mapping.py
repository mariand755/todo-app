from types import SimpleNamespace

from app.api import apply_item_order_positions


def make_item(id, position=-1, title=None):
    return SimpleNamespace(id=id, position=position, title=title or f"item_{id}")


def test_apply_order_full_list():
    items = [make_item(i) for i in range(1, 5)]
    order = [4, 2, 3, 1]

    apply_item_order_positions(items, order)

    # positions should match order indices
    positions = {item.id: item.position for item in items}
    assert positions[4] == 0
    assert positions[2] == 1
    assert positions[3] == 2
    assert positions[1] == 3


def test_apply_order_partial_list_appends_others():
    items = [make_item(i) for i in range(1, 6)]
    order = [3, 1]

    apply_item_order_positions(items, order)

    # listed items should get positions 0 and 1
    positions = {item.id: item.position for item in items}
    assert positions[3] == 0
    assert positions[1] == 1
    # every other item's position should be >= len(order)
    for i in [2, 4, 5]:
        assert positions[i] >= len(order)

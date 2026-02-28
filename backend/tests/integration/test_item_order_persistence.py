from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.helpers import seed_db_with_test_folder, seed_db_with_test_item


def test_reorder_persists_on_get(test_client: TestClient, testing_db_session: Session):
    # seed folder and items
    folder = seed_db_with_test_folder(testing_db_session)
    items = [seed_db_with_test_item(testing_db_session, folder, position=i) for i in range(4)]

    # reorder: move last to first
    order_payload = {"itemOrder_id": [items[3].id, items[0].id, items[1].id, items[2].id]}
    resp = test_client.put(f"/folders/{folder.id}/item_order", json=order_payload)
    assert resp.status_code == 200

    # fetch items and ensure positions are persisted and ordered
    get_resp = test_client.get(f"/folders/{folder.id}/items")
    assert get_resp.status_code == 200
    got = get_resp.json()
    assert len(got) == 4
    assert got[0]["id"] == items[3].id and got[0]["position"] == 0
    assert got[1]["id"] == items[0].id and got[1]["position"] == 1
    assert got[2]["id"] == items[1].id and got[2]["position"] == 2
    assert got[3]["id"] == items[2].id and got[3]["position"] == 3


def test_partial_order_list_appends_missing_items(test_client: TestClient, testing_db_session: Session):
    # seed folder and items
    folder = seed_db_with_test_folder(testing_db_session)
    items = [seed_db_with_test_item(testing_db_session, folder, position=i) for i in range(4)]

    # send payload with only two ids; others should be appended after
    order_payload = {"itemOrder_id": [items[2].id, items[0].id]}
    resp = test_client.put(f"/folders/{folder.id}/item_order", json=order_payload)
    assert resp.status_code == 200

    # fetch items and ensure positions for listed items are 0.. and others follow
    get_resp = test_client.get(f"/folders/{folder.id}/items")
    assert get_resp.status_code == 200
    got = get_resp.json()
    ids = [i["id"] for i in got]
    # first two should be the ones we sent, in that order
    assert ids[0] == items[2].id
    assert ids[1] == items[0].id
    # remaining ids should be the other two in some order, but positions should be >=2
    remaining_positions = {got[i]["id"]: got[i]["position"] for i in range(2, len(got))}
    for _rid, pos in remaining_positions.items():
        assert pos >= 2

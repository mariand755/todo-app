import uuid

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from library.models import Folder


def test_create_items_assigned_sequential_positions(test_client: TestClient, testing_db_session: Session):
    # create a folder directly in the DB
    folder = Folder(title=f"f_{uuid.uuid4()}")
    testing_db_session.add(folder)
    testing_db_session.flush()

    # create three items via the API and assert positions 0,1,2
    created = []
    for i in range(3):
        payload = {"title": f"item_{i}"}
        resp = test_client.post(f"/folders/{folder.id}/items", json=payload)
        assert resp.status_code == 200
        created.append(resp.json())

    assert created[0]["position"] == 0
    assert created[1]["position"] == 1
    assert created[2]["position"] == 2


def test_edit_created_item_preserves_position_and_order(test_client: TestClient, testing_db_session: Session):
    # create a folder
    folder = Folder(title=f"f_{uuid.uuid4()}")
    testing_db_session.add(folder)
    testing_db_session.flush()

    # create two items via API
    resp1 = test_client.post(f"/folders/{folder.id}/items", json={"title": "first"})
    resp2 = test_client.post(f"/folders/{folder.id}/items", json={"title": "second"})
    assert resp1.status_code == 200 and resp2.status_code == 200
    item1 = resp1.json()
    resp2.json()

    # edit the first item
    update_resp = test_client.put(f"/folders/{folder.id}/items/{item1['id']}", json={"title": "first-updated"})
    assert update_resp.status_code == 200
    updated = update_resp.json()
    # position should be preserved
    assert updated["position"] == item1["position"]

    # fetching folder items should return them ordered by position and updated title present
    list_resp = test_client.get(f"/folders/{folder.id}/items")
    assert list_resp.status_code == 200
    items = list_resp.json()
    positions = [it["position"] for it in items]
    assert positions == sorted(positions)

    found = next((it for it in items if it["id"] == item1["id"]), None)
    assert found is not None
    assert found["position"] == item1["position"]
    assert found["title"] == "first-updated"

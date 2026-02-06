import pytest
from fastapi.testclient import TestClient
from app.api import app 
from sqlalchemy.orm import Session
from library.models import get_db, Folder, TodoItem
import uuid


@pytest.fixture
def test_client(testing_db_session: Session):
    with TestClient(app) as client:
        app.dependency_overrides[get_db] = lambda: testing_db_session
        yield client

def seed_db_with_test_folder(testing_db_session: Session, random_title:str=f"test_{uuid.uuid4()}", is_folder_deleted:bool=False) -> Folder:
    folder = Folder(title=random_title, is_deleted=is_folder_deleted)
    testing_db_session.add(folder)
    testing_db_session.commit()
    return folder

def create_test_payload(num:int) -> list[dict]:
    return [{"title":f"test_{uuid.uuid4()}"} for i in range(num)]

def seed_db_with_test_item(testing_db_session: Session, folder:Folder, random_title:str=f"test_{uuid.uuid4()}", 
                           is_item_deleted:bool=False, completed:bool=False, 
                           position:int=-1) -> TodoItem:
    item = TodoItem(folder_id=folder.id, title=random_title, is_deleted=is_item_deleted, completed=completed, position=position)
    testing_db_session.add(item)
    testing_db_session.commit()
    return item

def test_get_default_empty_folders_success(test_client: TestClient):
    response = test_client.get("/folders")
    assert response.status_code == 200
    assert response.json() == []

def test_get_active_folders_success(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    #act
    response = test_client.get("/folders")
    #assert
    assert response.status_code == 200
    res_json = response.json()
    assert len(res_json) == 1
    assert res_json[0]["title"] == folder.title

def test_get_deleted_folders_not_in_response(test_client: TestClient, testing_db_session: Session):
    #arrange
    seed_db_with_test_folder(testing_db_session, is_folder_deleted=True)
    #act
    response = test_client.get("/folders")
    #assert
    assert response.status_code == 200
    assert response.json() == []

def test_create_folder_success(test_client: TestClient):
    #arrange
    test_payload = create_test_payload(1)
    #act
    response = test_client.post("/folders", json=test_payload[0])
    #assert
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["title"] == test_payload[0]["title"]

def test_create_folders_bad_input_success(test_client: TestClient):
    #arrange
    bad_payload = []
    #act
    response = test_client.post("/folders", json=bad_payload)
    #assert
    assert response.status_code == 400

def test_get_single_folder_id_exist_success(test_client: TestClient, testing_db_session: Session):
    #arrange
    seed_folder = seed_db_with_test_folder(testing_db_session)
    #act
    response = test_client.get(f"/folders/{seed_folder.id}")
    #assert
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["title"] == seed_folder.title

def test_get_folder_id_not_found(test_client: TestClient):
    #arrange
    none_existing_folder = 3
    #act
    response = test_client.get(f"/folders/{none_existing_folder}")
    #assert
    assert response.status_code == 404

def test_get_existing_folder_is_deleted(test_client: TestClient, testing_db_session: Session):
    #arrange
    seed_folder = seed_db_with_test_folder(testing_db_session, is_folder_deleted=True)
    #act
    response = test_client.get(f"/folders/{seed_folder.id}")
    #assert
    assert response.status_code == 404

def test_get_anydata_instead_of_int(test_client: TestClient):
    #arrange
    bad_data = "this"
    #act
    response = test_client.get(f"folders/{bad_data}")
    #assert
    assert response.status_code == 400


def test_update_folder_title(test_client: TestClient, testing_db_session: Session):
    #arrange
    seed_folder = seed_db_with_test_folder(testing_db_session)
    new_folder_title = create_test_payload(1)
    #act
    updated_response = test_client.put(f"folders/{seed_folder.id}", json=new_folder_title[0])
    #assert
    assert updated_response.status_code == 200
    res_json = updated_response.json()
    assert res_json["title"] == new_folder_title[0]["title"] 

def test_update_folder_with_same_title(test_client: TestClient, testing_db_session: Session):
    #arrange
    seed_folder = seed_db_with_test_folder(testing_db_session)
    #act
    #place in a variable  = extract form the db the title of the folder via title
    #use the variable to update the seed_folder title via the api call
    seed_res_payload = {"title": seed_folder.title}
    updated_folder_title = test_client.put(f"folders/{seed_folder.id}", json=seed_res_payload)
    #assert
    assert updated_folder_title.status_code == 200
    res_json = updated_folder_title.json()
    assert res_json["title"] == seed_folder.title


def test_updated_folder_is_deleted(test_client: TestClient, testing_db_session: Session):
    #arrange
    #seed the db with data, delete the data = set is_deleted to True
    #check payload obj with the seed_data obj incase tilte
    #check the response status code is not found 404
    seed_folder = seed_db_with_test_folder(testing_db_session, is_folder_deleted=True)
    seed_res_payload = {"title": seed_folder.title}
    #act
    deleted_folder = test_client.put(f"folders/{seed_folder.id}", json=seed_res_payload)
    #assert
    assert deleted_folder.status_code == 404
    res_json = deleted_folder.json()
    assert res_json == {"detail": "Folder not found"}

#use payload for a diff folder
#update the folder of the seeded data (using put api call)
#check the json response of the the updated folder is not found 
def test_non_existing_updated_folder(test_client: TestClient):
    #arrange
    res_payload = {"title": "None Existing Folder"}
    #act
    update_nonexisting_folder = test_client.put("folders/1", json=res_payload)
    #assert
    assert update_nonexisting_folder.status_code == 404
    res_json = update_nonexisting_folder.json()
    assert res_json == {"detail": "Folder not found"}

# manipulating the api url
# dont need to seed data
# do need a mock url (on the id)
# verify the status code 
def test_put_api_endpoint_without_int_id(test_client: TestClient):
    #arrange
    manipulated_endpoint = {"title": "None Existing Folder"}
    #act
    endpoint_without_int_id = test_client.put("folders/ndpoint", json=manipulated_endpoint)
    #assert
    assert endpoint_without_int_id.status_code == 400

def test_delete_existing_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    #seed db to have an existing folder 
    seed_folder = seed_db_with_test_folder(testing_db_session)  
    #act
    #call the delete api 
    deleted_folder = test_client.delete(f"folders/{seed_folder.id}")
    #assert
    #check status code 204
    assert deleted_folder.status_code == 204

def test_delete_already_deleted_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    #seed data will have it set to is_deleted true
    #db session
    seed_folder = seed_db_with_test_folder(testing_db_session, is_folder_deleted=True)
    #act
    #call the delet api 
    already_deleted_folder = test_client.delete(f"folders/{seed_folder.id}")
    #assert
    #check status code 404
    #check error message
    assert already_deleted_folder.status_code == 404
    res_json = already_deleted_folder.json()
    assert res_json == {"detail": "Folder not found"}
     
def test_delete_nonexisting_folder(test_client: TestClient):
    #arrange
    #folder do not exist so no need for seed data
    #create a variable for a random folder id
    non_existing_folder = 1
    #act
    #delete the random folder id
    delete_non_existing_folder = test_client.delete(f"folders/{non_existing_folder}")
    #assert
    #check status code = 404
    #check error message
    assert delete_non_existing_folder.status_code == 404
    res_json = delete_non_existing_folder.json()
    assert res_json == {"detail": "Folder not found"}

# send an invalid delete endpoint
def test_invalid_delete_endpoint(test_client: TestClient):
    #arrange
    #create a variable for a manipulate the invalid endpoint
    invalid_endpoint = "invalid"
    #act
    #call the invalid api 
    delete_invalid_endpoint = test_client.delete(f"folders/{invalid_endpoint}")
    #arrange
    #check status code = 400
    assert delete_invalid_endpoint.status_code == 400

#create item within folder
def test_get_item_within_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    #seed the db with item
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder)
    #act
    #call the get item api with the seed data
    item_within_folder = test_client.get(f"folders/{folder.id}/items")
    #assert
    #check the status code of the call = 200
    #check the res json tilte = the seed data tilte
    assert item_within_folder.status_code == 200
    res_json = item_within_folder.json()
    assert res_json[0]["title"] == item.title

#create multiple items (3)
def test_get_multiple_items_within_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    #seed folder data
    folder = seed_db_with_test_folder(testing_db_session)
    #seed multiple items data 
    items = []
    for i in range(3):
       item = seed_db_with_test_item(testing_db_session, folder) 
       items.append(item)
    #act
    #call the get item api with the seed data
    items_within_folder = test_client.get(f"folders/{folder.id}/items")
    #assert
    #check the status code of the call = 200
    assert items_within_folder.status_code == 200 
    #check the res json tiltes = the items seed data titles
    res_json = items_within_folder.json()
    for i in range(3):
        item = items[i]
        for res_item in res_json:
            if res_item["id"] == item.id:
                assert res_item["title"] == item.title 

# verify num of items within folder
# seed db with data - folder/items
# create a for loop to seed multiple items data
# call the api to created the muliple items
# verify the response json status code
# verify the len of items to get #
def test_get_num_of_items_in_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    #seed folder data
    folder = seed_db_with_test_folder(testing_db_session)
    #seed multiple items data 
    for i in range(5):
       item = seed_db_with_test_item(testing_db_session, folder) 
    #act
    #call the get item api with the seed data
    items_within_folder = test_client.get(f"folders/{folder.id}/items")
    #assert
    #check the status code of the call = 200
    assert items_within_folder.status_code == 200
    #verify the number of items within folder
    res_json = items_within_folder.json()
    assert len(res_json) == 5


#verify empty items api call return 200
# seed db with folder data 
# do not seed with items data
# call the items api
# verify response status code 200
def test_get_empty_folder_returns_successfully(test_client: TestClient, testing_db_session: Session):
    #arrange
    #seed folder data
    folder = seed_db_with_test_folder(testing_db_session)
    #act
    #call the get item api with the seed data
    folder_without_items = test_client.get(f"folders/{folder.id}/items")
    #assert
    #check the status code of the call = 200
    assert folder_without_items.status_code == 200 
    res_json = folder_without_items.json()
    assert len(res_json) == 0

#verify in folder returns 404
# call a non existing folder with items api call
# check response returns 404
def test_get_non_existing_folder_with_items_api(test_client: TestClient):
    #arrange
    non_existing_folder = 3
    #act
    non_existing_folder_with_items_api = test_client.get(f"folders/{non_existing_folder}/items")
    #assert
    assert non_existing_folder_with_items_api.status_code == 404
    res_json = non_existing_folder_with_items_api.json()
    assert res_json == {"detail": "Folder not found"}

#verify existing folder with items is deleted returns 404
# seed db with folder
# seed db with items
# call the is_deleted on the seeded folder
# call the items api on the deleted seed folder
# verify the response returns 404
def test_get_existing_folder_with_items_isdeleted(test_client: TestClient, testing_db_session: Session):
    # arrange
    seed_folder = seed_db_with_test_folder(testing_db_session, is_folder_deleted=True)
    # act
    existing_folder_with_items_isdeleted = test_client.get(f"folders/{seed_folder.id}/items") 
    # assert 
    assert existing_folder_with_items_isdeleted.status_code == 404
    res_json = existing_folder_with_items_isdeleted.json()
    assert res_json == {"detail": "Folder not found"}

#verify invalid api call returns 400
# create invalid folder id type
# verify the response returns 400
def test_get_invalid_api_call(test_client: TestClient):
    # arrange
    invalid_folder_id = "pops"
    # act
    invalid_api_call = test_client.get(f"folders/{invalid_folder_id}/items")
    # assert
    assert invalid_api_call.status_code == 400

# POST /folders/{folder_id}/items - Create item within folder

#verify create item within folder returns 200
# seed db with folder data 
# create item payload
# call the create item api
# verify response status code 200
# verify response contains item details
def test_create_item_success(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item_payload = {"title": "test_item"}
    #act
    create_item_response = test_client.post(f"folders/{folder.id}/items", json=item_payload)
    #assert
    assert create_item_response.status_code == 200
    res_json = create_item_response.json()
    assert res_json["title"] == item_payload["title"]
    assert res_json["folder_id"] == folder.id

#verify create multiple items within folder returns 200
# seed db with folder data
# create multiple item payloads
# call the create item api multiple times
# verify response status code 200 for each
# verify each response contains correct item details
def test_create_multiple_items_success(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item_payloads = create_test_payload(3)
    #act
    created_items = []
    for payload in item_payloads:
        response = test_client.post(f"folders/{folder.id}/items", json=payload)
        created_items.append(response)
    #assert
    for i, response in enumerate(created_items):
        assert response.status_code == 200
        res_json = response.json()
        assert res_json["title"] == item_payloads[i]["title"]
        assert res_json["folder_id"] == folder.id

#verify create item within non-existing folder returns 404
# create item payload
# call the create item api with non-existing folder id
# verify response status code 404
def test_create_item_in_nonexisting_folder(test_client: TestClient):
    #arrange
    non_existing_folder = 999
    item_payload = {"title": "test_item"}
    #act
    create_item_response = test_client.post(f"folders/{non_existing_folder}/items", json=item_payload)
    #assert
    assert create_item_response.status_code == 404
    res_json = create_item_response.json()
    assert res_json == {"detail": "Folder not found"}

#verify create item within deleted folder returns 404
# seed db with folder (is_deleted=True)
# create item payload
# call the create item api with deleted folder id
# verify response status code 404
def test_create_item_in_deleted_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session, is_folder_deleted=True)
    item_payload = {"title": "test_item"}
    #act
    create_item_response = test_client.post(f"folders/{folder.id}/items", json=item_payload)
    #assert
    assert create_item_response.status_code == 404
    res_json = create_item_response.json()
    assert res_json == {"detail": "Folder not found"}

#verify create item with bad input returns 400
# seed db with folder data
# create empty/invalid item payload
# call the create item api with bad payload
# verify response status code 400
def test_create_item_bad_input(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    bad_payload = {}
    #act
    create_item_response = test_client.post(f"folders/{folder.id}/items", json=bad_payload)
    #assert
    assert create_item_response.status_code == 400

#verify create item with invalid folder id type returns 400
# create item payload
# call the create item api with invalid folder id type
# verify response status code 400
def test_create_item_invalid_folder_id_type(test_client: TestClient):
    #arrange
    invalid_folder_id = "invalid"
    item_payload = {"title": "test_item"}
    #act
    create_item_response = test_client.post(f"folders/{invalid_folder_id}/items", json=item_payload)
    #assert
    assert create_item_response.status_code == 400

#verify created item has correct default values
# seed db with folder data
# create item payload
# call the create item api
# verify response contains correct default values (completed=False, position=-1)
def test_create_item_default_values(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item_payload = {"title": "test_item"}
    #act
    create_item_response = test_client.post(f"folders/{folder.id}/items", json=item_payload)
    #assert
    assert create_item_response.status_code == 200
    res_json = create_item_response.json()
    assert res_json["completed"] == False
    assert res_json["position"] == -1

# GET /folders/{folder_id}/items/{item_id} - Get specific item within folder

#verify get existing item returns 200
# seed db with folder and item
# call the get item api with folder_id and item_id
# verify response status code 200
# verify response contains correct item details
def test_get_item_success(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder)
    #act
    get_item_response = test_client.get(f"folders/{folder.id}/items/{item.id}")
    #assert
    assert get_item_response.status_code == 200
    res_json = get_item_response.json()
    assert res_json["id"] == item.id
    assert res_json["title"] == item.title
    assert res_json["folder_id"] == folder.id

#verify get item with correct response model
# seed db with folder and item
# call the get item api
# verify response contains all required fields
def test_get_item_response_model(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder)
    #act
    get_item_response = test_client.get(f"folders/{folder.id}/items/{item.id}")
    #assert
    assert get_item_response.status_code == 200
    res_json = get_item_response.json()
    assert "id" in res_json
    assert "title" in res_json
    assert "folder_id" in res_json
    assert "completed" in res_json
    assert "position" in res_json

#verify get non-existing item returns 404
# seed db with folder but no item
# call the get item api with non-existing item_id
# verify response status code 404
def test_get_nonexisting_item(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    non_existing_item_id = 999
    #act
    get_item_response = test_client.get(f"folders/{folder.id}/items/{non_existing_item_id}")
    #assert
    assert get_item_response.status_code == 404
    res_json = get_item_response.json()
    assert res_json == {"detail": "Item not found"}

#verify get item from non-existing folder returns 404
# do not seed folder
# call the get item api with non-existing folder_id
# verify response status code 404
def test_get_item_from_nonexisting_folder(test_client: TestClient):
    #arrange
    non_existing_folder_id = 999
    non_existing_item_id = 1
    #act
    get_item_response = test_client.get(f"folders/{non_existing_folder_id}/items/{non_existing_item_id}")
    #assert
    assert get_item_response.status_code == 404
    res_json = get_item_response.json()
    assert res_json == {"detail": "Folder not found"}

#verify get item from deleted folder returns 404
# seed db with deleted folder
# seed db with item
# call the get item api with deleted folder_id
# verify response status code 404
def test_get_item_from_deleted_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session, is_folder_deleted=True)
    item = seed_db_with_test_item(testing_db_session, folder)
    #act
    get_item_response = test_client.get(f"folders/{folder.id}/items/{item.id}")
    #assert
    assert get_item_response.status_code == 404
    res_json = get_item_response.json()
    assert res_json == {"detail": "Folder not found"}

#verify get item with invalid folder_id type returns 400
# create invalid folder_id type
# call the get item api with invalid folder_id
# verify response status code 400
def test_get_item_invalid_folder_id_type(test_client: TestClient):
    #arrange
    invalid_folder_id = "invalid"
    item_id = 1
    #act
    get_item_response = test_client.get(f"folders/{invalid_folder_id}/items/{item_id}")
    #assert
    assert get_item_response.status_code == 400

#verify get item with invalid item_id type returns 400
# seed db with folder
# create invalid item_id type
# call the get item api with invalid item_id
# verify response status code 400
def test_get_item_invalid_item_id_type(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    invalid_item_id = "invalid"
    #act
    get_item_response = test_client.get(f"folders/{folder.id}/items/{invalid_item_id}")
    #assert
    assert get_item_response.status_code == 400

#verify get item from wrong folder returns 404
# seed db with two folders and items in each
# call the get item api with folder_id and item_id from different folders
# verify response status code 404
def test_get_item_from_wrong_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder1 = seed_db_with_test_folder(testing_db_session)
    folder2 = seed_db_with_test_folder(testing_db_session)
    item_in_folder1 = seed_db_with_test_item(testing_db_session, folder1)
    #act
    get_item_response = test_client.get(f"folders/{folder2.id}/items/{item_in_folder1.id}")
    #assert
    assert get_item_response.status_code == 404
    res_json = get_item_response.json()
    assert res_json == {"detail": "Item not found"}

# PUT /folders/{folder_id}/items/{item_id} - Update item within folder

#verify update existing item returns 200
# seed db with folder and item
# create update payload with new title
# call the update item api
# verify response status code 200
# verify response contains updated item details
def test_update_item_success(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder)
    update_payload = {"title": "updated_title"}
    #act
    update_item_response = test_client.put(f"folders/{folder.id}/items/{item.id}", json=update_payload)
    #assert
    assert update_item_response.status_code == 200
    res_json = update_item_response.json()
    assert res_json["id"] == item.id
    assert res_json["title"] == update_payload["title"]
    assert res_json["folder_id"] == folder.id

#verify update item with same title returns 200
# seed db with folder and item
# create update payload with same title
# call the update item api
# verify response status code 200
# verify response title matches
def test_update_item_same_title(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder)
    update_payload = {"title": item.title}
    #act
    update_item_response = test_client.put(f"folders/{folder.id}/items/{item.id}", json=update_payload)
    #assert
    assert update_item_response.status_code == 200
    res_json = update_item_response.json()
    assert res_json["title"] == item.title

#verify update non-existing item returns 404
# seed db with folder but no item
# create update payload
# call the update item api with non-existing item_id
# verify response status code 404
def test_update_nonexisting_item(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    non_existing_item_id = 999
    update_payload = {"title": "updated_title"}
    #act
    update_item_response = test_client.put(f"folders/{folder.id}/items/{non_existing_item_id}", json=update_payload)
    #assert
    assert update_item_response.status_code == 404
    res_json = update_item_response.json()
    assert res_json == {"detail": "Item not found"}

#verify update item in non-existing folder returns 404
# do not seed folder
# create update payload
# call the update item api with non-existing folder_id
# verify response status code 404
def test_update_item_in_nonexisting_folder(test_client: TestClient):
    #arrange
    non_existing_folder_id = 999
    item_id = 1
    update_payload = {"title": "updated_title"}
    #act
    update_item_response = test_client.put(f"folders/{non_existing_folder_id}/items/{item_id}", json=update_payload)
    #assert
    assert update_item_response.status_code == 404
    res_json = update_item_response.json()
    assert res_json == {"detail": "Folder not found"}

#verify update item in deleted folder returns 404
# seed db with deleted folder
# seed db with item
# create update payload
# call the update item api
# verify response status code 404
def test_update_item_in_deleted_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session, is_folder_deleted=True)
    item = seed_db_with_test_item(testing_db_session, folder)
    update_payload = {"title": "updated_title"}
    #act
    update_item_response = test_client.put(f"folders/{folder.id}/items/{item.id}", json=update_payload)
    #assert
    assert update_item_response.status_code == 404
    res_json = update_item_response.json()
    assert res_json == {"detail": "Folder not found"}

#verify update deleted item returns 404
# seed db with folder and deleted item
# create update payload
# call the update item api
# verify response status code 404
def test_update_deleted_item(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder, is_item_deleted=True)
    update_payload = {"title": "updated_title"}
    #act
    update_item_response = test_client.put(f"folders/{folder.id}/items/{item.id}", json=update_payload)
    #assert
    assert update_item_response.status_code == 404
    res_json = update_item_response.json()
    assert res_json == {"detail": "Item not found"}

#verify update item with bad input returns 400
# seed db with folder and item
# create empty/invalid update payload
# call the update item api with bad payload
# verify response status code 400
def test_update_item_bad_input(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder)
    bad_payload = {}
    #act
    update_item_response = test_client.put(f"folders/{folder.id}/items/{item.id}", json=bad_payload)
    #assert
    assert update_item_response.status_code == 400

#verify update item with invalid folder_id type returns 400
# create update payload
# call the update item api with invalid folder_id type
# verify response status code 400
def test_update_item_invalid_folder_id_type(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder)
    invalid_folder_id = "invalid"
    update_payload = {"title": "updated_title"}
    #act
    update_item_response = test_client.put(f"folders/{invalid_folder_id}/items/{item.id}", json=update_payload)
    #assert
    assert update_item_response.status_code == 400

#verify update item with invalid item_id type returns 400
# seed db with folder
# create update payload
# call the update item api with invalid item_id type
# verify response status code 400
def test_update_item_invalid_item_id_type(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    invalid_item_id = "invalid"
    update_payload = {"title": "updated_title"}
    #act
    update_item_response = test_client.put(f"folders/{folder.id}/items/{invalid_item_id}", json=update_payload)
    #assert
    assert update_item_response.status_code == 400

#verify update item from wrong folder returns 404
# seed db with two folders and items in each
# create update payload
# call the update item api with folder_id and item_id from different folders
# verify response status code 404
def test_update_item_from_wrong_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder1 = seed_db_with_test_folder(testing_db_session)
    folder2 = seed_db_with_test_folder(testing_db_session)
    item_in_folder1 = seed_db_with_test_item(testing_db_session, folder1)
    update_payload = {"title": "updated_title"}
    #act
    update_item_response = test_client.put(f"folders/{folder2.id}/items/{item_in_folder1.id}", json=update_payload)
    #assert
    assert update_item_response.status_code == 404
    res_json = update_item_response.json()
    assert res_json == {"detail": "Item not found"}

#verify update item preserves other fields
# seed db with folder and item with specific values
# create update payload with only title
# call the update item api
# verify completed and position fields are preserved
def test_update_item_preserves_other_fields(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder, completed=False, position=5)
    update_payload = {"title": "updated_title"}
    #act
    update_item_response = test_client.put(f"folders/{folder.id}/items/{item.id}", json=update_payload)
    #assert
    assert update_item_response.status_code == 200 
    res_json = update_item_response.json()
    assert res_json["title"] == update_payload["title"]
    assert res_json["completed"] == False
    assert res_json["position"] == 5

#verify update cannot be made on a item marked complete
# seed db with folder and item marked complete
# create updated payload 
# call the update item api
# verify response status code 403 and detail content 
def test_update_completed_item_unsuccessful(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder, completed=True)
    update_payload = {"title":"updated_title"}
    #act
    update_item_reponse = test_client.put(f"folders/{folder.id}/items/{item.id}", json=update_payload)
    #assert
    assert update_item_reponse.status_code == 403
    res_json = update_item_reponse.json()
    assert res_json == {"detail": "Item completed and cannot be updated"}



# DELETE /folders/{folder_id}/items/{item_id} - Delete item within folder

#verify delete existing item returns 204
# seed db with folder and item
# call the delete item api
# verify response status code 204
def test_delete_item_success(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder)
    #act
    delete_response = test_client.delete(f"folders/{folder.id}/items/{item.id}")
    #assert
    assert delete_response.status_code == 204

#verify delete non-existing item returns 404
# seed db with folder but no item
# call the delete item api with non-existing item_id
# verify response status code 404
def test_delete_nonexisting_item(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    non_existing_item_id = 999
    #act
    delete_response = test_client.delete(f"folders/{folder.id}/items/{non_existing_item_id}")
    #assert
    assert delete_response.status_code == 404
    res_json = delete_response.json()
    assert res_json == {"detail": "Item not found"}

#verify delete item from non-existing folder returns 404
# do not seed folder
# call the delete item api with non-existing folder_id
# verify response status code 404
def test_delete_item_from_nonexisting_folder(test_client: TestClient):
    #arrange
    non_existing_folder_id = 999
    item_id = 1
    #act
    delete_response = test_client.delete(f"folders/{non_existing_folder_id}/items/{item_id}")
    #assert
    assert delete_response.status_code == 404
    res_json = delete_response.json()
    assert res_json == {"detail": "Folder not found"}

#verify delete item from deleted folder returns 404
# seed db with deleted folder and item
# call the delete item api
# verify response status code 404
def test_delete_item_from_deleted_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session, is_folder_deleted=True)
    item = seed_db_with_test_item(testing_db_session, folder)
    #act
    delete_response = test_client.delete(f"folders/{folder.id}/items/{item.id}")
    #assert
    assert delete_response.status_code == 404
    res_json = delete_response.json()
    assert res_json == {"detail": "Folder not found"}

#verify delete already deleted item returns 404
# seed db with folder and deleted item
# call the delete item api
# verify response status code 404
def test_delete_already_deleted_item(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder, is_item_deleted=True)
    #act
    delete_response = test_client.delete(f"folders/{folder.id}/items/{item.id}")
    #assert
    assert delete_response.status_code == 404
    res_json = delete_response.json()
    assert res_json == {"detail": "Item not found"}

#verify delete item with invalid folder_id type returns 400
def test_delete_item_invalid_folder_id_type(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder)
    invalid_folder_id = "invalid"
    #act
    delete_response = test_client.delete(f"folders/{invalid_folder_id}/items/{item.id}")
    #assert
    assert delete_response.status_code == 400

#verify delete item with invalid item_id type returns 400
def test_delete_item_invalid_item_id_type(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    invalid_item_id = "invalid"
    #act
    delete_response = test_client.delete(f"folders/{folder.id}/items/{invalid_item_id}")
    #assert
    assert delete_response.status_code == 400

#verify delete item from wrong folder returns 404
# seed db with two folders and item in one
# call the delete api on the other folder with that item id
# verify response status code 404
def test_delete_item_from_wrong_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder1 = seed_db_with_test_folder(testing_db_session)
    folder2 = seed_db_with_test_folder(testing_db_session)
    item_in_folder1 = seed_db_with_test_item(testing_db_session, folder1)
    #act
    delete_response = test_client.delete(f"folders/{folder2.id}/items/{item_in_folder1.id}")
    #assert
    assert delete_response.status_code == 404
    res_json = delete_response.json()
    assert res_json == {"detail": "Item not found"}

# PUT /folders/{folder_id}/items/{item_id}/toggle - Toggle item completed status

#verify toggle item from incomplete to complete returns 200
# seed db with folder and item (completed=False)
# call the toggle item api
# verify response status code 200
# verify completed field changed to True
def test_toggle_item_incomplete_to_complete(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder, completed=False)
    #act
    toggle_response = test_client.put(f"folders/{folder.id}/items/{item.id}/toggle")
    #assert
    assert toggle_response.status_code == 200
    res_json = toggle_response.json()
    assert res_json["id"] == item.id
    assert res_json["completed"] == True

#verify toggle item from complete to incomplete returns 200
# seed db with folder and item (completed=True)
# call the toggle item api
# verify response status code 200
# verify completed field changed to False
def test_toggle_item_complete_to_incomplete(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder, completed=True)
    #act
    toggle_response = test_client.put(f"folders/{folder.id}/items/{item.id}/toggle")
    #assert
    assert toggle_response.status_code == 200
    res_json = toggle_response.json()
    assert res_json["id"] == item.id
    assert res_json["completed"] == False

#verify toggle item preserves other fields
# seed db with folder and item with specific values
# call the toggle item api
# verify title, folder_id, position fields are preserved
def test_toggle_item_preserves_other_fields(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder, completed=False, position=3)
    original_title = item.title
    #act
    toggle_response = test_client.put(f"folders/{folder.id}/items/{item.id}/toggle")
    #assert
    assert toggle_response.status_code == 200
    res_json = toggle_response.json()
    assert res_json["title"] == original_title
    assert res_json["folder_id"] == folder.id
    assert res_json["position"] == 3
    assert res_json["completed"] == True

#verify toggle non-existing item returns 404
# seed db with folder but no item
# call the toggle item api with non-existing item_id
# verify response status code 404
def test_toggle_nonexisting_item(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    non_existing_item_id = 999
    #act
    toggle_response = test_client.put(f"folders/{folder.id}/items/{non_existing_item_id}/toggle")
    #assert
    assert toggle_response.status_code == 404
    res_json = toggle_response.json()
    assert res_json == {"detail": "Item not found"}

#verify toggle item in non-existing folder returns 404
# do not seed folder
# call the toggle item api with non-existing folder_id
# verify response status code 404
def test_toggle_item_in_nonexisting_folder(test_client: TestClient):
    #arrange
    non_existing_folder_id = 999
    item_id = 1
    #act
    toggle_response = test_client.put(f"folders/{non_existing_folder_id}/items/{item_id}/toggle")
    #assert
    assert toggle_response.status_code == 404
    res_json = toggle_response.json()
    assert res_json == {"detail": "Folder not found"}

#verify toggle item in deleted folder returns 404 
# toggle endpoint does check if folder is deleted
# seed db with deleted folder and item
# call the toggle item api
# verify response status code 404 & detail = folder not found
def test_toggle_item_in_deleted_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session, is_folder_deleted=True)
    item = seed_db_with_test_item(testing_db_session, folder, completed=False)
    #act
    toggle_response = test_client.put(f"folders/{folder.id}/items/{item.id}/toggle")
    #assert
    assert toggle_response.status_code == 404
    res_json = toggle_response.json()
    assert res_json == {"detail": "Folder not found"}

#verify toggle deleted item returns 404
# toggle endpoint does check if item is deleted
# seed db with folder and deleted item
# call the toggle item api
# verify response status code 404 & detail = item not found
def test_toggle_deleted_item(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder, is_item_deleted=True, completed=False)
    #act
    toggle_response = test_client.put(f"folders/{folder.id}/items/{item.id}/toggle")
    #assert
    assert toggle_response.status_code == 404
    res_json = toggle_response.json()
    assert res_json == {"detail": "Item not found"}

#verify toggle item with invalid folder_id type returns 400
# create invalid folder_id type
# call the toggle item api with invalid folder_id
# verify response status code 400
def test_toggle_item_invalid_folder_id_type(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item = seed_db_with_test_item(testing_db_session, folder)
    invalid_folder_id = "invalid"
    #act
    toggle_response = test_client.put(f"folders/{invalid_folder_id}/items/{item.id}/toggle")
    #assert
    assert toggle_response.status_code == 400

#verify toggle item with invalid item_id type returns 400
# seed db with folder
# create invalid item_id type
# call the toggle item api with invalid item_id
# verify response status code 400
def test_toggle_item_invalid_item_id_type(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    invalid_item_id = "invalid"
    #act
    toggle_response = test_client.put(f"folders/{folder.id}/items/{invalid_item_id}/toggle")
    #assert
    assert toggle_response.status_code == 400

#verify toggle item from wrong folder returns 404
# seed db with two folders and item in one
# call the toggle api on the other folder with that item id
# verify response status code 404
def test_toggle_item_from_wrong_folder(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder1 = seed_db_with_test_folder(testing_db_session)
    folder2 = seed_db_with_test_folder(testing_db_session)
    item_in_folder1 = seed_db_with_test_item(testing_db_session, folder1)
    #act
    toggle_response = test_client.put(f"folders/{folder2.id}/items/{item_in_folder1.id}/toggle")
    #assert
    assert toggle_response.status_code == 404
    res_json = toggle_response.json()
    assert res_json == {"detail": "Item not found"}

# PUT /folders/{folder_id}/item_order - Reorder items within folder

#verify update item order returns 200
# seed db with folder and multiple items
# create payload with reordered item ids
# call the item order api
# verify response status code 200
# verify items are returned in new order
def test_update_item_order_success(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item1 = seed_db_with_test_item(testing_db_session, folder, position=0)
    item2 = seed_db_with_test_item(testing_db_session, folder, position=1)
    item3 = seed_db_with_test_item(testing_db_session, folder, position=2)
    # reorder to 3, 1, 2
    order_payload = {"itemOrder_id": [item3.id, item1.id, item2.id]}
    #act
    updated_order_response = test_client.put(f"folders/{folder.id}/item_order", json=order_payload)
    #assert
    assert updated_order_response.status_code == 200
    res_json = updated_order_response.json()
    assert len(res_json["items"]) == 3
    assert res_json["items"][0]["id"] == item3.id
    assert res_json["items"][0]["position"] == 0
    assert res_json["items"][1]["id"] == item1.id
    assert res_json["items"][1]["position"] == 1
    assert res_json["items"][2]["id"] == item2.id
    assert res_json["items"][2]["position"] == 2

#verify update item order with two items
# seed db with folder and two items
# create payload with reordered item ids
# call the item order api
# verify items are in correct order
def test_update_item_order_two_items(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item1 = seed_db_with_test_item(testing_db_session, folder, position=0)
    item2 = seed_db_with_test_item(testing_db_session, folder, position=1)
    # reorder to 2, 1
    order_payload = {"itemOrder_id": [item2.id, item1.id]}
    #act
    updated_order_response = test_client.put(f"folders/{folder.id}/item_order", json=order_payload)
    #assert
    assert updated_order_response.status_code == 200
    res_json = updated_order_response.json()
    assert res_json["items"][0]["id"] == item2.id
    assert res_json["items"][0]["position"] == 0
    assert res_json["items"][1]["id"] == item1.id
    assert res_json["items"][1]["position"] == 1

#verify update item order with same order
# seed db with folder and items
# create payload with same order as current
# call the item order api
# verify response status code 200
def test_update_item_order_same_order(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item1 = seed_db_with_test_item(testing_db_session, folder, position=0)
    item2 = seed_db_with_test_item(testing_db_session, folder, position=1)
    item3 = seed_db_with_test_item(testing_db_session, folder, position=2)
    # same order as current
    order_payload = {"itemOrder_id": [item1.id, item2.id, item3.id]}
    #act
    updated_order_response = test_client.put(f"folders/{folder.id}/item_order", json=order_payload)
    #assert
    assert updated_order_response.status_code == 200
    res_json = updated_order_response.json()
    assert res_json["items"][0]["id"] == item1.id
    assert res_json["items"][1]["id"] == item2.id
    assert res_json["items"][2]["id"] == item3.id

#verify update item order in non-existing folder returns 404
# do not seed folder
# create payload with item ids
# call the item order api with non-existing folder_id
# verify response status code 404
def test_update_item_order_nonexisting_folder(test_client: TestClient):
    #arrange
    non_existing_folder_id = 999
    order_payload = {"itemOrder_id": [1, 2, 3]}
    #act
    updated_order_response = test_client.put(f"folders/{non_existing_folder_id}/item_order", json=order_payload)
    #assert
    assert updated_order_response.status_code == 404
    res_json = updated_order_response.json()
    assert res_json == {"detail": "Folder not found"}

#verify update item order with invalid folder_id type returns 400
# create invalid folder_id type
# create payload with item ids
# call the item order api with invalid folder_id
# verify response status code 400
def test_update_item_order_invalid_folder_id_type(test_client: TestClient):
    #arrange
    invalid_folder_id = "invalid"
    order_payload = {"itemOrder_id": [1, 2, 3]}
    #act
    updated_order_response = test_client.put(f"folders/{invalid_folder_id}/item_order", json=order_payload)
    #assert
    assert updated_order_response.status_code == 400

#verify update item order with bad payload returns 400
# seed db with folder
# create empty/invalid payload
# call the item order api with bad payload
# verify response status code 400
def test_update_item_order_bad_payload(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    bad_payload = {}
    #act
    updated_order_response = test_client.put(f"folders/{folder.id}/item_order", json=bad_payload)
    #assert
    assert updated_order_response.status_code == 400

#verify update item order with empty list returns 400
# seed db with folder and items
# create payload with empty item list
# call the item order api
# verify response status code 400
def test_update_item_order_empty_list(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    seed_db_with_test_item(testing_db_session, folder)
    order_payload = {"itemOrder_id": []}
    #act
    updated_order_response = test_client.put(f"folders/{folder.id}/item_order", json=order_payload)
    #assert
    assert updated_order_response.status_code == 400


#verify update item order preserves item data
# seed db with folder and items with various properties
# create payload with reordered ids
# call the item order api
# verify item titles and other properties are preserved
def test_update_item_order_preserves_item_data(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = seed_db_with_test_folder(testing_db_session)
    item1 = seed_db_with_test_item(testing_db_session, folder, position=0, completed=True)
    item2 = seed_db_with_test_item(testing_db_session, folder, position=1, completed=False)
    item1_title = item1.title
    item2_title = item2.title
    # reorder to 2, 1
    order_payload = {"itemOrder_id": [item2.id, item1.id]}
    #act
    updated_order_response = test_client.put(f"folders/{folder.id}/item_order", json=order_payload)
    #assert
    assert updated_order_response.status_code == 200
    res_json = updated_order_response.json()
    assert res_json["items"][0]["title"] == item2_title
    assert res_json["items"][0]["completed"] == False
    assert res_json["items"][1]["title"] == item1_title
    assert res_json["items"][1]["completed"] == True




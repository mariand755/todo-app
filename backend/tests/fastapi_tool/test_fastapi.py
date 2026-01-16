import pytest
from fastapi.testclient import TestClient
from fastapi_tool.fastapi import app 
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

def test_single_folder_id_exist_success(test_client: TestClient, testing_db_session: Session):
    #arrange
    seed_folder = seed_db_with_test_folder(testing_db_session)
    #act
    response = test_client.get(f"/folders/{seed_folder.id}")
    #assert
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["title"] == seed_folder.title

def test_folder_id_not_found(test_client: TestClient):
    #arrange
    none_existing_folder = 3
    #act
    response = test_client.get(f"/folders/{none_existing_folder}")
    #assert
    assert response.status_code == 404

def test_existing_folder_is_deleted(test_client: TestClient, testing_db_session: Session):
    #arrange
    seed_folder = seed_db_with_test_folder(testing_db_session, is_folder_deleted=True)
    #act
    response = test_client.get(f"/folders/{seed_folder.id}")
    #assert
    assert response.status_code == 404

def test_anydata_instead_of_int(test_client: TestClient):
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
def test_create_item_within_folder(test_client: TestClient, testing_db_session: Session):
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
# verify #items in folder 
# verify empty items api call return 200
#verify no item in folder returns 404
#verify existing item is deleted returns 404
#verify invalid api call returns 400

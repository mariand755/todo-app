import pytest
from fastapi.testclient import TestClient
from fastapi_tool.fastapi import app 
from sqlalchemy.orm import Session
from library.models import get_db, Folder
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

# check an update folder is deleted
# update non existing folder tilte
# update with int instead of a str

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


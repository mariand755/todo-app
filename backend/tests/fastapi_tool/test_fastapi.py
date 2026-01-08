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

def create_test_folder(testing_db_session: Session, random_title:str=f"test_{uuid.uuid4()}", is_folder_deleted:bool=False) -> Folder:
    folder = Folder(title=random_title, is_deleted=is_folder_deleted)
    testing_db_session.add(folder)
    testing_db_session.commit()
    return folder

    
def test_get_default_empty_folders_success(test_client: TestClient):
    response = test_client.get("/folders")
    assert response.status_code == 200
    assert response.json() == []

def test_get_active_folders_success(test_client: TestClient, testing_db_session: Session):
    #arrange
    folder = create_test_folder(testing_db_session)
    #act
    response = test_client.get("/folders")
    #assert
    assert response.status_code == 200
    res_json = response.json()
    assert len(res_json) == 1
    assert res_json[0]["title"] == folder.title

def test_get_deleted_folders_not_in_response(test_client: TestClient, testing_db_session: Session):
    #arrange
    create_test_folder(testing_db_session, is_folder_deleted=True)
    #act
    response = test_client.get("/folders")
    #assert
    assert response.status_code == 200
    assert response.json() == []


#def test_create_folder_success(test_client: TestClient):
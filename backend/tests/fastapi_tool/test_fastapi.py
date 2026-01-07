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

class TestGetFoldersEndPoint:
    
    def test_get_default_empty_folders_success(test_client: TestClient):
        response = test_client.get("/folders")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_active_folders_success(test_client: TestClient, testing_db_session: Session):
        #arrange
        random_title = f"test_{uuid.uuid4()}"
        folder = Folder(title=random_title)

        #act

        #assert


#def test_create_folder_success(test_client: TestClient):
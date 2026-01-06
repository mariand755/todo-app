import pytest
from fastapi.testclient import TestClient
from fastapi_tool.fastapi import app 
from sqlalchemy.orm import Session


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client

def test_get_folders_success(testing_db_session: Session, test_client: TestClient):
    response = test_client.get("/folders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


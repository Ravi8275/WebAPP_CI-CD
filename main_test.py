from fastapi import status
from fastapi.testclient import TestClient
from main import application

client = TestClient(application)

def test_client():
    response = client.get('/healthz')
    assert response.status_code == status.HTTP_200_OK

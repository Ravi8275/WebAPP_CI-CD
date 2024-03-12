from fastapi.testclient import TestClient
from main import application
from main import status
import pytest

client = TestClient(application)

def test_health_check():
    response = client.get('/healthz')
    assert response.status_code == status.HTTP_200_OK

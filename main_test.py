from unittest.mock import patch
from fastapi.testclient import TestClient
from main import application

client = TestClient(application)

@patch('main.start_postgresql')
def test_health_check(mock_start_postgresql):
    mock_start_postgresql.return_value = None
    response = client.get('/healthz')
    assert response.status_code == 200

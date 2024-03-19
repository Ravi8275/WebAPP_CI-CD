from unittest.mock import patch
from fastapi.testclient import TestClient
from main import application

client = TestClient(application)

@patch('database.start_postgresql')
def test_health_check(mock_start_postgresql):
    mock_start_postgresql.return_value = None
    import main
    response = client.get('/healthz')
    assert response.status_code == 200

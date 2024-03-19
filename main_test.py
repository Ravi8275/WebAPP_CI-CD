from unittest.mock import patch
from fastapi.testclient import TestClient
from main import application

client = TestClient(application)

@patch('subprocess.run')
def test_health_check(mock_subprocess_run):
    mock_subprocess_run.return_value = None
    import database
    response = client.get('/healthz')
    assert response.status_code == 200

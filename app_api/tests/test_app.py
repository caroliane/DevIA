import pytest
from fastapi.testclient import TestClient
from app_api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to app_api!"}

@pytest.mark.asyncio
async def test_fetch_data(monkeypatch):
    """monkeypatch est utilisé pour remplacer l'appel réel à httpx par une réponse simulée.
    Cela permet de tester l'interaction entre les deux APIs sans démarrer le conteneur de data_api."""
    # Simule la réponse de l'API data_api
    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json_data = json_data

        def json(self):
            return self._json_data  # Sérialisation JSON synchrone

    async def mock_get_data(*args, **kwargs):
        return MockResponse(200, {"data": "Mocked data from data_api"})

    # Patcher l'appel HTTPX
    monkeypatch.setattr("httpx.AsyncClient.get", mock_get_data)

    # Tester la route /fetch-data
    response = client.get("/fetch-data")
    assert response.status_code == 200
    assert response.json() == {"data_from_data_api": {"data": "Mocked data from data_api"}}

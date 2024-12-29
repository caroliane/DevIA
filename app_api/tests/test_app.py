import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import patch
from app_api.main import app
from app_api.mongo_utils import get_db_connection
import os
os.environ["TESTING"] = "1"

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

def test_youtube_url_valid():
    """Teste une URL YouTube valide"""
    payload = {
        "url": "https://www.youtube.com/watch?v=AGtF3HdXmOY",
        "upload_timestamp": "2024-12-28T13:31:09.798Z",
    }
    response = client.post("/youtube-url", json=payload)
    assert response.status_code == 200
    response_json = response.json()

    # Vérifier les autres champs
    assert response_json["url"] == payload["url"]
    assert response_json["message"] == "L'URL YouTube est valide et a été acceptée."

    # Comparer le timestamp en format ISO
    returned_timestamp = datetime.fromisoformat(response_json["upload_timestamp"].replace("Z", "+00:00"))
    expected_timestamp = datetime.fromisoformat(payload["upload_timestamp"].replace("Z", "+00:00"))
    assert returned_timestamp == expected_timestamp

# def test_youtube_url_invalid():
#     """Teste une URL YouTube invalide"""
#     payload = {
#         "url": "https://www.youtube.com/watch?v=AGtF3HdXmOYxxx/",
#         "upload_timestamp": "2024-12-28T13:31:09.798Z",
#     }
#     response = client.post("/youtube-url", json=payload)
#     assert response.status_code == 400
#     assert response.json()["detail"] == "L'URL doit être une URL YouTube valide."

# Mock MongoDB connection
@pytest.fixture(autouse=True)
def mock_db():
    """Mock la connexion à MongoDB pour les tests."""
    with patch("app_api.mongo_utils.get_db_connection") as mock_get_db_connection:
        from mongomock import MongoClient
        mock_get_db_connection.return_value = MongoClient().db
        yield

def test_read_root():
    """Teste la route racine."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to app_api!"}

@pytest.mark.asyncio
async def test_fetch_data(monkeypatch):
    """Teste l'interaction avec /fetch-data."""
    # Simule la réponse de l'API data_api
    class MockResponse:
        def __init__(self, status_code, json_data):
            self.status_code = status_code
            self._json_data = json_data

        def json(self):
            return self._json_data

    async def mock_get_data(*args, **kwargs):
        return MockResponse(200, {"data": "Mocked data from data_api"})

    # Patcher l'appel HTTPX
    monkeypatch.setattr("httpx.AsyncClient.get", mock_get_data)

    # Tester la route /fetch-data
    response = client.get("/fetch-data")
    assert response.status_code == 200
    assert response.json() == {"data_from_data_api": {"data": "Mocked data from data_api"}}

def test_youtube_url_valid():
    """Teste l'insertion d'une URL YouTube valide."""
    payload = {
        "url": "https://www.youtube.com/watch?v=AGtF3HdXmOY",
        "upload_timestamp": "2024-12-29T15:34:40.865Z",
    }
    response = client.post("/youtube-url", json=payload)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["url"] == payload["url"]
    assert response_json["message"] == "L'URL YouTube est valide et a été enregistrée."

    # Vérification du timestamp
    returned_timestamp = datetime.fromisoformat(response_json["upload_timestamp"].replace("Z", "+00:00"))
    expected_timestamp = datetime.fromisoformat(payload["upload_timestamp"].replace("Z", "+00:00"))
    assert returned_timestamp == expected_timestamp

# def test_youtube_url_duplicate():
#     """Teste l'insertion d'une URL YouTube déjà existante."""
#     payload = {
#         "url": "https://www.youtube.com/watch?v=AGtF3HdXmOY",
#         "upload_timestamp": "2024-12-29T15:34:40.865Z",
#     }
#     response = client.post("/youtube-url", json=payload)
#     assert response.status_code == 200

#     # Deuxième tentative avec la même URL
#     response = client.post("/youtube-url", json=payload)
#     assert response.status_code == 400
#     assert response.json()["detail"] == "L'URL YouTube est déjà enregistrée."

# def test_youtube_url_invalid():
#     """Teste l'insertion d'une URL invalide."""
#     payload = {
#         "url": "https://www.invalid-url.com",
#         "upload_timestamp": "2024-12-29T15:34:40.865Z",
#     }
#     response = client.post("/youtube-url", json=payload)
#     assert response.status_code == 400
#     assert "L'URL doit être une URL YouTube valide." in response.json()["detail"]
from fastapi.testclient import TestClient
from data_api.main import app

client = TestClient(app)

def test_get_data():
    response = client.get("/data")
    assert response.status_code == 200
    assert response.json() == {"data": "This is data from data_api"}

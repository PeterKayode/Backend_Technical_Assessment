from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/api/v1/users/register", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login():
    response = client.post("/api/v1/users/login", data={"username": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert "access_token" in response.json()
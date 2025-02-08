from unittest.mock import patch, MagicMock
import pytest
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

# Mock the entire smol_blogwriter module
with patch.dict('sys.modules', {'app.tasks.smol_blogwriter': MagicMock()}):
    from app.main import app  # Import after mocking

def test_root_endpoint():
    from fastapi.testclient import TestClient  # Assuming FastAPI
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200

# Test User Registration
def test_register_user():
    response = client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"

# Test User Login
def test_login_user():
    response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test Create Blog Post (Authenticated)
def test_create_blog_post():
    # Login to get token
    login_response = client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "password123"
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create Blog
    response = client.post("/api/v1/blog/", json={
        "title": "Test Blog",
        "content": "This is a test blog post."
    }, headers=headers)

    assert response.status_code == 201
    assert response.json()["title"] == "Test Blog"

# Test Fetch Blogs
def test_get_blogs():
    response = client.get("/api/v1/blog/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test Background Task Trigger
def test_trigger_background_task():
    response = client.post("/api/v1/blog/generate", json={
        "prompt": "Write about AI in 2024."
    })
    assert response.status_code == 202
    assert "task_id" in response.json()

# Test AI Agent Task
def test_ai_agent_task():
    response = client.post("/api/v1/blog/ai-agent", json={
        "prompt": "Benefits of automation."
    })
    assert response.status_code == 200
    assert "content" in response.json()

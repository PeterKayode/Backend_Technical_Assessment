import pytest
from fastapi.testclient import TestClient
from app.main import app  # Ensure this is your FastAPI app

client = TestClient(app)

# Hard-coded token for endpoints requiring authentication
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0aW5nMDAxQGV4YW1wbGUuY29tIiwiZXhwIjoxNzM4OTU3MTMwfQ.p8oAWrN2-QDQLoogUvbuXI1rkcV-EGQFJEu5P2GfSDc"
headers = {"Authorization": f"Bearer {token}"}

def test_create_user():
    response = client.post("/api/v1/register", json={"email": "test012@example.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["email"] == "test012@example.com"

def test_login():
    response = client.post("/api/v1/login", json={"email": "test012@example.com", "password": "password"})

    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.fixture
def create_blog():
    global token
    global headers

    # Blog data for creation
    blog_data = {
        "title": "Test Blog Title",
        "content": "This is a test blog content"
    }
    
    # Create the blog post using the authentication header
    response = client.post("/api/v1/blogs", json=blog_data, headers=headers)
    
    # Assert that creation was successful (status code 201)
    assert response.status_code == 201
    
    # Retrieve the created blog's ID from the nested "blog" key.
    response_json = response.json()
    # Print for debugging (optional):
    print("Create blog response:", response_json)
    created_blog_id = response_json["blog"]["id"]
    
    # Return the ID for reuse in other tests
    return created_blog_id

def test_create_blog():
    global token
    global headers

    blog_data = {
        "title": "Test Blog Title",
        "content": "This is a test blog content"
    }
    response = client.post("/api/v1/blogs", json=blog_data, headers=headers)
    # Now assert that the creation was successful.
    assert response.status_code == 201
    response_json = response.json()
    # The response now returns a nested structure, so check for the "blog" key.
    assert "blog" in response_json
    assert "id" in response_json["blog"]
    # Verify the returned title.
    assert response_json["blog"]["title"] == blog_data["title"]

def test_read_blog(create_blog):
    blog_id = create_blog  # Get the created blog ID from the fixture
    response = client.get(f"/api/v1/blogs/{blog_id}")
    assert response.status_code == 200
    response_json = response.json()
    # The read endpoint is assumed to return a blog post dictionary with key "id"
    assert response_json["id"] == blog_id

def test_update_blog(create_blog):
    blog_id = create_blog  # Get the created blog ID from the fixture
    updated_blog_data = {
        "title": "Updated Blog Title",
        "content": "This is updated blog content"
    }

    # Update the blog post
    response = client.put(f"/api/v1/blogs/{blog_id}", json=updated_blog_data)
    # Change the expected status code from 200 to 202.
    assert response.status_code == 202
    response_json = response.json()
    # Check that the update message is correct.
    assert response_json["message"] == "Blog update is being processed."
    # Check that the title has been updated exactly.
    assert response_json["blog"]["title"] == updated_blog_data["title"]
    # Verify that the updated blog content is non-empty.
    assert response_json["blog"]["content"], "The updated blog content should not be empty."


def test_delete_blog(create_blog):
    blog_id = create_blog  # Get the created blog ID from the fixture
    # Include the token header for authentication on delete.
    response = client.delete(f"/api/v1/blogs/{blog_id}", headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["message"] == "Blog post deleted successfully"

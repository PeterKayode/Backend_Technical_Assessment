# AI-Powered Blog Post Creation API

## Overview
This API allows users to **create**, **read**, **update**, and **delete** blog posts, with automated content generation powered by an AI module (`smol_blogwriter.py`). Content generation tasks run in the background, ensuring smooth performance and quick API responses.

---

## **Table of Contents**

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Database Structure](#database-structure)
- [Setup and Installation](#setup-and-installation)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Database Migrations](#database-migrations)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [AI Content Generation (smol_blogwriter.py)](#ai-content-generation)
- [Background Task Workflow](#background-taskworkflow)
- [Error Handling](#error-handling)
- [Testing](#testing)
- [For Frontend Developers](#for-frontend-developers)
- [Future Enhancements](#future-enhancements)

---

## **Features**

- **User Authentication:**  
  - User registration (`POST /api/v1/register`)
  - User login (`POST /api/v1/login`) with JWT authentication

- **Blog Post Management:**  
  - Create blog posts with AI-generated content (via background tasks) (`POST /api/v1/blogs`)
  - Retrieve a single blog post (`GET /api/v1/blogs/{id}`)
  - Retrieve all blog posts (`GET /api/v1/blogs`)
  - Update blog posts (optionally regenerating content asynchronously) (`PUT /api/v1/blogs/{id}`)
  - Delete blog posts (`DELETE /api/v1/blogs/{id}`)

- **AI Integration:**  
  - Uses an AI agent (GPT-4o-mini) to generate blog content.
  - Background task processing for long-running AI operations.
  - Status tracking for blog post generation (e.g., "pending", "in_progress", "completed", "failed").

---

## **Technologies Used**

- **FastAPI:** For building the API.
- **SQLAlchemy:** ORM for database interactions.
- **Alembic:** For database migrations.
- **Uvicorn:** ASGI server to run the FastAPI app.
- **Pytest:** For testing the application.
- **Python-JOSE:** For JWT authentication.
- **Asyncio:** To support asynchronous tasks.
- **OpenAI API:** For AI-generated content.

---

## **Project Structure**

```
Backend_Technical_Assessment/
├── .env
├── .gitignore
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py
│   │   │   │   ├── blog.py
│   │   │   ├── __init__.py
│   │   ├── __init__.py
│   ├── background_tasks/
│   │   ├── blog_task.py
│   │   ├── __init__.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── __init__.py
│   ├── crud/
│   │   ├── blog.py
│   │   ├── user.py
│   │   ├── __init__.py
│   ├── db/
│   │   ├── base.py
│   │   ├── base_class.py
│   │   ├── session.py
│   │   ├── __init__.py
│   ├── models/
│   │   ├── blog.py
│   │   ├── user.py
│   │   ├── __init__.py
│   ├── schemas/
│   │   ├── blog.py
│   │   ├── user.py
│   │   ├── __init__.py
│   ├── tasks/
│   │   ├── ai_agent.py
│   │   ├── __init__.py
│   │   ├── smol_blogwriter.py
│   ├── main.py
│   ├── __init__.py
├── requirements.txt
├── tests/
│   ├── test_api.py
│   ├── __init__.py
├── README.md
```

---

## **Database Structure**

### BlogPost Model

```python
    __tablename__ = "blog_posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))  # Foreign key to User

    # Relationship to User
    owner = relationship("User", back_populates="blogs")
```

- **`id`**: The primary key for the blog post.
- **`title`**: The title of the blog post.
- **`content`**: The main text content of the blog post.
- **`owner_id`**: A foreign key that links the blog post to the user who owns it.
- **Relationship**:  
  - Each blog post is associated with one user (the owner).  
  - The `owner` attribute provides access to the corresponding `User` object.  
  - The `back_populates="blogs"` indicates that in the `User` model, the related collection is accessed via the `blogs` attribute.

### User Model

```python
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship to BlogPost
    blogs = relationship("BlogPost", back_populates="owner")
```

- **`id`**: The primary key for the user.
- **`email`**: The user's unique email address.
- **`hashed_password`**: The user's password stored in a hashed format.
- **`is_active`**: A boolean flag to indicate if the user is active.
- **Relationship**:  
  - A user can have multiple blog posts.  
  - The `blogs` attribute holds a list of all blog posts associated with the user, corresponding to the `owner` relationship defined in the `BlogPost` model.

### Relationship Summary

- **One-to-Many Relationship (User to BlogPost):**
  - A single user (owner) can have many blog posts.
  - In the **User** model, the `blogs` attribute is a collection of all the blog posts that the user has created.
  - In the **BlogPost** model, the `owner_id` field is used as a foreign key to reference the associated user, and the `owner` relationship allows easy access to that user.

---

## **Setup and Installation**

### Prerequisites

- Python 3.12 or higher
- A relational database (SQLite)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Environment Variables

Create a `.env` file in the project root with the following variables (adjust as needed):

```dotenv
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your_OPENAI_API_KEY_here
```

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PeterKayode/Backend_Technical_Assessment
   cd Backend_Technical_Assessment
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Alembic (if not already initialized):**

   ```
   alembic init alembic
   ```

5. **Generate a migration script:**

   ```
   alembic revision --autogenerate -m "Initial migration"
   ```

6. **Apply migrations:**

   ```
   alembic upgrade head
   ```

7. **Run the API:**
   ```bash
   uvicorn app.main:app --reload
   ```


The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## **API Documentation**

FastAPI automatically generates interactive API documentation:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## **AI Content Generation (smol_blogwriter.py)**
- **Location:** `app/tasks/smol_blogwriter.py`
- **Function:** `write_blog_post(title, content)`
- **Returns:**
  ```json
  {
    "title": "Optimized Blog Title",
    "content": "This is the AI-generated blog content."
  }
  ```
- **Integration:** The background task `generate_blog_content` in `blog_task.py` handles invoking this AI module.

---

## **Background Task Workflow**
1. **User submits a blog post.**
2. **`generate_blog_content`** starts running in the background.
3. **AI generates content** using `write_blog_post()`.
4. **Blog status** updates from `pending` → `in_progress` → `completed`.
5. **Error handling** ensures status updates to `failed` if any issue occurs.

---

## **Error Handling**
- **404 Not Found:** When blog post ID doesn’t exist.

---

## **Testing**

The project includes a suite of tests using Pytest. To run the tests:

```
pytest
```

Tests cover user registration, login, and CRUD operations on blog posts, including background task processing for AI-generated content.

---

## ***For Frontend Developers***

### API Endpoints Overview

- **User Registration:**  
  `POST /api/v1/register`  
  **Request Body:**  
  ```json
  {
    "email": "user@example.com",
    "password": "password"
  }
  ```
  
- **User Login:**  
  `POST /api/v1/login`  
  **Request Body/Form Data:**  
  ```json
  {
    "email": "user@example.com",
    "password": "password"
  }
  ```
  **Response:**  
  ```json
  {
    "access_token": "jwt_token_here",
    "token_type": "bearer"
  }
  ```

- **Create Blog Post:**  
  `POST /api/v1/blogs`  
  **Request Body:**  
  ```json
  {
    "title": "Blog Title",
    "content": "Initial blog content (optional)"
  }
  ```
  **Response:**  
  ```json
  {
    "message": "Blog creation is being processed.",
    "blog": {
      "id": 1,
      "title": "Blog Title",
      "content": "",
      "owner_id": 1,
      "status": "pending"
    }
  }
  ```
  _Note:_ The final blog content will be updated asynchronously.

- **Read Single Blog Post:**  
  `GET /api/v1/blogs/{id}`

- **Read All Blog Posts:**  
  `GET /api/v1/blogs`  
  **Response:**  
  ```json
  {
    "blogs": [
      { "id": 1, "title": "Blog Title", "content": "...", "status": "completed" },
      ...
    ]
  }
  ```

- **Update Blog Post:**  
  `PUT /api/v1/blogs/{id}`  
  _Note:_ The update may trigger background AI processing and returns a status of `202 Accepted`.

- **Delete Blog Post:**  
  `DELETE /api/v1/blogs/{id}`

### Authentication

- All endpoints that modify data (create, update, delete) require a valid JWT token in the `Authorization` header.  
  Example header:
  ```
  Authorization: Bearer your_jwt_token_here
  ```

### Background Tasks and Status Tracking

- **Background Tasks:**  
  The API uses background tasks to handle long-running AI interactions. When a blog post is created or updated, it’s initially marked with a status like `"pending"` or `"in_progress"`, and then updated to `"completed"` (or `"failed"`) once the AI generation is finished.
  
- **Status Field:**  
  The blog post model includes a `status` field to indicate the progress of AI-generated content. Frontend developers can poll the blog endpoint to check the status of a post.

---

## **Future Enhancements**

- **Improved Error Handling:** Enhance error messages and logging.
- **Pagination for Blog Posts:** Add pagination support for the GET /blogs endpoint.
- **Caching:** Implement caching for improved performance.
- **Extended Testing:** Increase test coverage and integrate continuous integration (CI).

---

## **Contact**

For questions or further information, please contact [peterkayode618@gmail.com](mailto:peterkayode618@gmail.com.com).
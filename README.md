# AI-Powered Blog Post Creation API

## Setup

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run the application: `uvicorn app.main:app --reload`.
4. Access the API documentation at `http://localhost:8000/docs`.

## API Endpoints

- **User Registration**: `POST /api/v1/users/register`
- **User Login**: `POST /api/v1/users/login`
- **Create Blog Post**: `POST /api/v1/blogs`
- **Get Blog Post**: `GET /api/v1/blogs/{id}`
- **Update Blog Post**: `PUT /api/v1/blogs/{id}`
- **Delete Blog Post**: `DELETE /api/v1/blogs/{id}`


## Project Structure

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
│   ├── main.py
│   ├── __init__.py
├── requirements.txt
├── tests/
│   ├── conftest.py
│   ├── test_api.py
│   ├── test_crud.py
│   ├── __init__.py
├── README.md
```

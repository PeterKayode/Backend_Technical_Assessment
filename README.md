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

## Testing

Run the tests using:

```bash
pytest
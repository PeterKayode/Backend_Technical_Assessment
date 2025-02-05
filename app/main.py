from fastapi import FastAPI
from app.api.v1.endpoints import auth, blog
from app.core.config import settings

app = FastAPI(title="AI-Powered Blog Post Creation API")

app.include_router(auth.router, prefix="/api/v1")
app.include_router(blog.router, prefix="/api/v1")
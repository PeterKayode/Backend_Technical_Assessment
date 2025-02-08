from fastapi import FastAPI
from app.api.v1.endpoints import auth, blog
from app.core.config import settings
import os

app = FastAPI()

# Check API Key on Startup
@app.on_event("startup")
async def check_api_key():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ API Key loaded: {api_key[:6]}****")
    else:
        print("❌ API Key NOT loaded!")

@app.get("/")
def index():
    return {"message": "AI-Powered Blog Post Creation API"}

app.include_router(auth.router, prefix="/api/v1")
app.include_router(blog.router, prefix="/api/v1")

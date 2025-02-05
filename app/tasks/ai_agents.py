import httpx
from fastapi import HTTPException

async def generate_blog_post(title: str) -> str:
    url = "https://github.com/samwit/smolagents_examples/blob/main/smol_blogwriter.py"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to generate blog post")
        return response.text
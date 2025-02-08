from fastapi import HTTPException
from app.tasks.smol_blogwriter import write_blog_post
import traceback


async def generate_blog_post(title: str, topic: str, input_content: str) -> dict:
    try:
        # Await the synchronous write_blog_post call (since it's wrapped in an async function, you can call it with await)
        blog_post_result = await write_blog_post(topic, input_content)
        return {"title": title, "content": blog_post_result["content"]}
    except Exception as e:
        error_message = f"Failed to generate blog post: {str(e)}"
        traceback_details = traceback.format_exc()
        print(f"{error_message}\nTraceback:\n{traceback_details}")
        raise HTTPException(status_code=500, detail=error_message)
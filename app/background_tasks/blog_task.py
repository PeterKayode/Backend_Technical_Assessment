import asyncio
from sqlalchemy.orm import Session
from app.models.blog import BlogPost
from app.tasks.ai_agent import generate_blog_post as async_generate_blog_post

def generate_blog_content(db: Session, blog_id: int, input_content: str):
    """
    Background task: Generate blog content using the AI agent and update the blog post.
    This function is synchronous (to be used by FastAPI BackgroundTasks), so it runs the asynchronous
    AI generation function using asyncio.run.
    """
    try:
        # Retrieve the blog post from the database.
        blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
        if not blog:
            return
        
        # Update the status to "in_progress"
        blog.status = "in_progress"
        db.commit()
        
        # Run the async AI generation function in the event loop.
        result = asyncio.run(async_generate_blog_post(blog.title, input_content))
        
        # Update the blog with the generated content.
        blog.title = result.get("title", blog.title)
        blog.content = result.get("content", "")
        blog.status = "completed"
        db.commit()
    except Exception as e:
        # If an error occurs, mark the blog as failed.
        if blog:
            blog.status = "failed"
            db.commit()
        print("Error in background task generate_blog_content:", e)

from app.models.blog import BlogPost
from app.tasks.smol_blogwriter import write_blog_post  # Synchronous version
from sqlalchemy.orm import Session
import json

def generate_blog_content(db: Session, blog_id: int, new_title: str, input_content: str):
    """
    Background task: Generate new blog content using AI and update the blog post record.
    - db: Database session.
    - blog_id: The ID of the blog to update.
    - new_title: The new title provided by the user.
    - input_content: The update instructions/content.
    """
    blog = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if not blog:
        return

    try:
        # Mark blog as in progress
        blog.status = "in_progress"
        db.commit()

        # Generate the blog post using write_blog_post
        # Pass the new title as well, so the AI uses the updated title context.
        result = write_blog_post(new_title, input_content)

        # Check if generation was successful and update the blog post record
        if result:
            blog.title = result.get("title", new_title)
            blog.content = result.get("content", "")
            if isinstance(blog.content, dict):
                blog.content = json.dumps(blog.content)
            blog.status = "completed"
        else:
            blog.status = "failed"

        db.commit()
    except Exception as e:
        blog.status = "failed"
        db.commit()
        print("Error in background task generate_blog_content:", e)

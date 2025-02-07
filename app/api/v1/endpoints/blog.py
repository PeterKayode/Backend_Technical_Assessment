from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.blog import create_blog_post, get_blog_post, delete_blog_post
from app.schemas.blog import BlogPostCreate, BlogPostUpdate
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.tasks.ai_agent import generate_blog_post  # Import the AI agent
import traceback
from app.models.blog import BlogPost


router = APIRouter()


# For the AI agent
@router.post("/blogs")
async def create_blog(blog: BlogPostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new blog post using the AI agent.
    """
    try:
        # Generate the blog post content using the AI agent
        blog_data = await generate_blog_post(blog.title, blog.content)
        
        # Create the blog post in the database
        db_blog = create_blog_post(db, BlogPostCreate(**blog_data), current_user.id)
        
        return db_blog
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/blogs/{id}")
def read_blog(id: int, db: Session = Depends(get_db)):
    db_blog = get_blog_post(db, id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return db_blog

@router.put("/blogs/{id}")
async def update_blog(id: int, blog_data: BlogPostUpdate, db: Session = Depends(get_db)):
    try:
        blog = db.query(BlogPost).filter(BlogPost.id == id).first()
        
        if not blog:
            raise HTTPException(status_code=404, detail="Blog post not found.")
        

        # blog.title = blog_data.title
        # blog.content = blog_data.content

        # Generate the blog post content using the AI agent
        blog_data = await generate_blog_post(blog.title, blog.content)

        blog.title = blog_data["title"]
        blog.content = blog_data["content"]
        
        db.commit()
        db.refresh(blog)

        return {"message": "Blog post updated successfully.", "blog": blog}

    except Exception as e:
        import traceback
        print(f"Error updating blog: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to update blog post: {str(e)}")


@router.delete("/blogs/{id}")
def delete_blog(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_blog = delete_blog_post(db, id, current_user.id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"message": "Blog post deleted successfully"}
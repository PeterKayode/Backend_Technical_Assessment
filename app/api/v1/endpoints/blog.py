from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.blog import create_blog_post, get_blog_post, update_blog_post, delete_blog_post
from app.schemas.blog import BlogPostCreate, BlogPostUpdate
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.tasks.ai_agent import generate_blog_post  # Import the AI agent


router = APIRouter()

#Without AI agent
# @router.post("/blogs")
# def create_blog(blog: BlogPostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     return create_blog_post(db, blog, current_user.id)

# For the AI agent

@router.post("/blogs")
async def create_blog(blog: BlogPostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create a new blog post using the AI agent.
    """
    try:
        # Generate the blog post content using the AI agent
        blog_data = await generate_blog_post(blog.title)
        
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

# @router.put("/blogs/{id}")
# def update_blog(id: int, blog: BlogPostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
#     db_blog = update_blog_post(db, id, blog, current_user.id)
#     if db_blog is None:
#         raise HTTPException(status_code=404, detail="Blog post not found")
#     return db_blog

@router.put("/blogs/{id}")
async def update_blog(
    id: int,
    blog: BlogPostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update an existing blog post and regenerate content using the AI agent.
    """
    try:
        # Debugging: Ensure current_user is correctly passed
        print(f"Current user: {current_user.email}")

        # Regenerate content using the AI agent (assuming blog.title is the new title)
        updated_content = await generate_blog_post(blog.title)

        if not isinstance(updated_content, str):
            raise HTTPException(status_code=500, detail="Generated content is not a valid string")

        # Log the content before updating
        print(f"Generated content for update: {updated_content[:100]}...")  # Log first 100 characters

        # Update the blog post in the database with the new title and regenerated content
        updated_blog = update_blog_post(db, id, blog, current_user.id, updated_content)

        if updated_blog is None:
            raise HTTPException(status_code=404, detail="Blog post not found")

        # Return the updated blog post
        return {"message": "Blog post updated successfully", "updated_blog": updated_blog}

    except Exception as e:
        # Handle exceptions and raise HTTPException with the message
        raise HTTPException(status_code=500, detail=f"Failed to update blog post: {str(e)}")



@router.delete("/blogs/{id}")
def delete_blog(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_blog = delete_blog_post(db, id, current_user.id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"message": "Blog post deleted successfully"}
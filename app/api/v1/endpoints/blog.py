from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.crud.blog import create_blog_post, get_blog_post, delete_blog_post
from app.schemas.blog import BlogPostCreate, BlogPostUpdate
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.blog import BlogPost
from app.background_tasks.blog_task import generate_blog_content  # Background task function

router = APIRouter()

#--------------------------------------------------------------- Create Blog -----------------------------------------------------------------------------------------

@router.post("/blogs", status_code=201)
async def create_blog(
    blog: BlogPostCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        pending_data = {
            "title": blog.title,
            "content": "...",  # Placeholder
            "status": "pending"
        }
        db_blog = create_blog_post(db, BlogPostCreate(**pending_data), current_user.id)
        db.refresh(db_blog)  # Refresh to ensure session sync

        background_tasks.add_task(generate_blog_content, db, db_blog.id, blog.title, blog.content)

        return {
            "status": "processing",
            "message": "Blog creation is being processed.",
            "blog": db_blog
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating blog: {str(e)}")


#--------------------------------------------------------------- Read All Blogs -----------------------------------------------------------------------------------------

@router.get("/blogs")
def read_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(BlogPost).all()
    if not blogs:
        raise HTTPException(status_code=404, detail="No blog posts found")
    return {"status": "success", "blogs": blogs}


#--------------------------------------------------------------- Read a Single Blog -----------------------------------------------------------------------------------------

@router.get("/blogs/{id}")
def read_blog(id: int, db: Session = Depends(get_db)):
    db_blog = get_blog_post(db, id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"status": "success", "blog": db_blog}


#--------------------------------------------------------------- Update a Blog -----------------------------------------------------------------------------------------

@router.put("/blogs/{id}", status_code=202)
async def update_blog(
    id: int,
    blog_data: BlogPostUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        blog = db.query(BlogPost).filter(BlogPost.id == id).first()
        if not blog:
            raise HTTPException(status_code=404, detail="Blog post not found.")

        blog.title = blog_data.title
        blog.content = "..."  # Placeholder
        blog.status = "pending"
        db.commit()
        db.refresh(blog)

        background_tasks.add_task(generate_blog_content, db, blog.id, blog_data.title, blog_data.content)

        return {"status": "processing", "message": "Blog update is being processed.", "blog": blog}
    except Exception as e:
        import traceback
        print(f"Error updating blog: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to update blog post: {str(e)}")


#--------------------------------------------------------------- Delete Blog -----------------------------------------------------------------------------------------

@router.delete("/blogs/{id}")
def delete_blog(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_blog = delete_blog_post(db, id, current_user.id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"status": "success", "message": "Blog post deleted successfully"}

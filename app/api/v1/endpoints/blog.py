from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.blog import create_blog_post, get_blog_post, update_blog_post, delete_blog_post
from app.schemas.blog import BlogPostCreate, BlogPostUpdate
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/blogs")
def create_blog(blog: BlogPostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_blog_post(db, blog, current_user.id)

@router.get("/blogs/{id}")
def read_blog(id: int, db: Session = Depends(get_db)):
    db_blog = get_blog_post(db, id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return db_blog

@router.put("/blogs/{id}")
def update_blog(id: int, blog: BlogPostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_blog = update_blog_post(db, id, blog, current_user.id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return db_blog

@router.delete("/blogs/{id}")
def delete_blog(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_blog = delete_blog_post(db, id, current_user.id)
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return {"message": "Blog post deleted successfully"}
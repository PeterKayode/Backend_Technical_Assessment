from sqlalchemy.orm import Session
from app.models.blog import BlogPost
from app.schemas.blog import BlogPostCreate, BlogPostUpdate
from fastapi import HTTPException

def create_blog_post(db: Session, blog: BlogPostCreate, owner_id: int):
    db_blog = BlogPost(**blog.dict(), owner_id=owner_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blog_post(db: Session, id: int):
    return db.query(BlogPost).filter(BlogPost.id == id).first()

# def update_blog_post(db: Session, id: int, blog: BlogPostUpdate, owner_id: int):
#     db_blog = db.query(BlogPost).filter(BlogPost.id == id, BlogPost.owner_id == owner_id).first()
#     if db_blog:
#         db_blog.title = blog.title
#         db_blog.content = blog.content
#         db.commit()
#         db.refresh(db_blog)
#     return db_blog

def update_blog_post(db: Session, id: int, blog: BlogPostUpdate, owner_id: int, updated_content: str):
    # Find the blog post by id and make sure the current user is the owner
    db_blog = db.query(BlogPost).filter(BlogPost.id == id, BlogPost.owner_id == owner_id).first()

    if not db_blog:
        print(f"Blog post with ID {id} not found.")  # Debug: Log missing blog post
        return None  # Ensure we return None if not found

    # Update the blog
    db_blog.title = blog.title
    db_blog.content = updated_content
    db.commit()
    db.refresh(db_blog)
    
    print(f"Updated blog post: {db_blog.title} - {db_blog.content}")  # Debug: Log updated content
    return db_blog

def delete_blog_post(db: Session, id: int, owner_id: int):
    db_blog = db.query(BlogPost).filter(BlogPost.id == id, BlogPost.owner_id == owner_id).first()
    if db_blog:
        db.delete(db_blog)
        db.commit()
    return db_blog
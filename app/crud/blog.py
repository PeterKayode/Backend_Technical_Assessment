from sqlalchemy.orm import Session
from app.models.blog import BlogPost
from app.schemas.blog import BlogPostCreate, BlogPostUpdate
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError


def create_blog_post(db: Session, blog: BlogPostCreate, owner_id: int):
    db_blog = BlogPost(**blog.dict(), owner_id=owner_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blog_post(db: Session, id: int):
    return db.query(BlogPost).filter(BlogPost.id == id).first()

def update_blog_post(db: Session, id: int, blog: BlogPostUpdate, owner_id: int, updated_content: str):
    try:
        db_blog = db.query(BlogPost).filter(BlogPost.id == id, BlogPost.owner_id == owner_id).first()

        if not db_blog:
            print(f"Blog post with ID {id} not found.")
            return None
        
        # Validate updated content
        if not isinstance(updated_content, str) or not updated_content.strip():
            print("Invalid content generated.")  # Debug print
            raise ValueError("Generated content is invalid.")

        db_blog.title = blog.title
        db_blog.content = updated_content

        db.commit()
        db.refresh(db_blog)

        print(f"Updated blog post: {db_blog.title} - {db_blog.content}")
        return db_blog

    except SQLAlchemyError as e:
        print(f"Database error occurred: {str(e)}")  # Log database-specific errors
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    except Exception as e:
        print(f"General error occurred: {str(e)}")  # Log unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


def delete_blog_post(db: Session, id: int, owner_id: int):
    db_blog = db.query(BlogPost).filter(BlogPost.id == id, BlogPost.owner_id == owner_id).first()
    if db_blog:
        db.delete(db_blog)
        db.commit()
    return db_blog
from pydantic import BaseModel

class BlogPostCreate(BaseModel):
    title: str
    content: str

class BlogPostUpdate(BaseModel):
    title: str
    content: str

class BlogPostInDB(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

    class Config:
        from_attributes = True
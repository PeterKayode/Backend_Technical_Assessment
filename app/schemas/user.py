from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserInDB(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True
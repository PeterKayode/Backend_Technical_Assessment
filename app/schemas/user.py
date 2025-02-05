from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True
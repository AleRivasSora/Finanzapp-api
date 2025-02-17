from sqlmodel import SQLModel
from pydantic import EmailStr
from datetime import datetime

class UserBase(SQLModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode: True

class UserLogin(SQLModel):
    email: EmailStr
    password: str
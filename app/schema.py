from datetime import datetime

from typing import Optional

from pydantic import BaseModel,EmailStr
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class ResponseUser(BaseModel):
    id: int
    email : EmailStr
    created_at : datetime
    
    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password : str

class PostCreate(PostBase):
    pass
class Responsepost(PostBase):
    id:int
    created_at : datetime
    owner_id : int
    owner : ResponseUser

    class Config:
        orm_mode = True

class Responsepost2(BaseModel):
    Post:Responsepost
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type  : str


class TokenData(BaseModel):
    id : Optional[str] = None

class Vote(BaseModel):
    post_id:int
    dir: int
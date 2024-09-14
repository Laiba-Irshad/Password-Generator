from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str
    created_at: Optional[datetime] = None

class UserLogin(BaseModel):
    username: str
    password: str

class userResetPassword(BaseModel):
    username:str
    current_password:str
    new_password:str

class userDeleteRequest(BaseModel):
    username:str
    password:str
    
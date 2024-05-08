from pydantic import BaseModel,EmailStr
from datetime import datetime


class User(BaseModel):
    username: str
    email: EmailStr | None = None
    password: str 
    created_at: datetime | None = None
    # hashed_password: str 
    # user_type:  str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None



class Resources(BaseModel):
    id: int
    user_id: str
    title: str
    created_at: datetime

class Resource_details(BaseModel):
    id: int
    resource_id: int
    resource_link: str
    created_at: datetime

class UserDict(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    password: str

class TokenData(BaseModel):
    username: str | None = None

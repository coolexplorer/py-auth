from typing import List, Optional

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserIn(UserBase):
    password: str
    email: str

class User(UserBase):
    hashed_password: str
    email: str

    class Config:
        orm_mode = True
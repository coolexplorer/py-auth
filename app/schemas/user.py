from typing import List, Optional

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str

class UserIn(UserBase):
    password: str

class User(UserBase):
    hashed_password: str

    class Config:
        orm_mode = True
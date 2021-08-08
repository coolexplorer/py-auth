from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserIn(UserBase):
    password: str

class User(UserBase):
    hashed_password: str
    create_date: datetime
    last_login: datetime

    class Config:
        orm_mode = True
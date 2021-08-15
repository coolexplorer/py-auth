from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

class UserBase(BaseModel):
    email: str

class UserIn(UserBase):
    password: str

    class Config:
        schema_extra = {
            "example" : {
                "email": "example@email.com",
                "password": "weakpassword",
            }
        }

class User(UserBase):
    hashed_password: str
    session_id: str
    create_date: datetime
    last_login: datetime

    class Config:
        orm_mode = True
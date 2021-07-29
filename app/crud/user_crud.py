from sqlalchemy import schema
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

import app.models.user as userModels
import app.schemas.user as userSchema
from app.utils.logger import logger

async def get_users(db: Session):
    return db.query(userModels.User).all()

async def get_user(db: Session, username: str):
    return db.query(userModels.User).filter(userModels.User.username == username).first()

async def get_user_by_id(db: Session, id: int):
    return db.query(userModels.User).filter(userModels.User.id == id).first()

async def create_user(db: Session, user: userSchema.UserIn):
    db_user = userModels.User(username=user.username, hashed_password=bcrypt.hash(user.password), email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def authenticate_user(db:Session, username: str, password: str):
    user = await get_user(db, username)

    if not user:
        return False
    
    if not verify_password(password = password, hashed_pasword=user.hashed_password):
        return False
    
    return user

def verify_password(password: str, hashed_pasword: str):
    return bcrypt.verify(password, hashed_pasword)

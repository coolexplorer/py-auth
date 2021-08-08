from sqlalchemy import schema
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from datetime import datetime

import models.user as userModels
import schemas.user as userSchema
from utils.logger import logger

async def get_users(db: Session):
    return db.query(userModels.User).all()

async def get_user(db: Session, email: str):
    return db.query(userModels.User).filter(userModels.User.email == email).first()

async def get_user_by_id(db: Session, id: int):
    return db.query(userModels.User).filter(userModels.User.id == id).first()

async def create_user(db: Session, user: userSchema.UserIn):
    db_user = userModels.User(
        email=user.email, 
        hashed_password=bcrypt.hash(user.password), 
        create_date=datetime.utcnow(),
        last_login=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def update_user(db: Session, user: userModels.User):
    user.last_login = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user

async def authenticate_user(db:Session, email: str, password: str):
    user = await get_user(db, email)

    if not user:
        return False
    
    if not verify_password(password = password, hashed_pasword=user.hashed_password):
        return False
    
    return user

def verify_password(password: str, hashed_pasword: str):
    return bcrypt.verify(password, hashed_pasword)

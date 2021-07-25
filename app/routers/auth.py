import logging
import jwt

from fastapi import APIRouter, Depends
from fastapi_versioning import version
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import crud.user_crud as userCrud
import schemas.user as userSchema
from dependencies.database import get_db
from utils.sqlalchemy import object_as_dict

JWT_SECRET = 'mysecret'
logger = logging.getLogger(__name__)
router = APIRouter(tags=['auth'])

# FastAPI security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

@router.post('/login', response_model=userSchema.User)
@version(1)
async def login(userIn: userSchema.UserIn, db: Session = Depends(get_db)):
    user = await userCrud.get_user(db, userIn.username)

    if not user:
        user = await userCrud.create_user(db, userIn)

    return user

@router.post('/token')
@version(1)
async def generate_token(userIn: userSchema.UserIn, db: Session = Depends(get_db)):
    user = await userCrud.authenticate_user(db, userIn.username, userIn.password)

    if not user:
        return { 'error': 'invalid credentials' }

    token = jwt.encode(object_as_dict(user), JWT_SECRET)

    return { 'access_token': token, 'token_type': 'bearer' }
    
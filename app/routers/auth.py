import logging
import jwt

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_versioning import version
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import schema
from sqlalchemy.orm import Session

import app.crud.user_crud as user_crud
import app.schemas.user as userSchema
import app.schemas.token as tokenSchema
from app.dependencies.database import get_db
from app.utils.sqlalchemy import object_as_dict

JWT_SECRET = 'mysecret'
logger = logging.getLogger(__name__)
router = APIRouter(tags=['auth'])

# FastAPI security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token/test')


@router.post('/login', response_model=userSchema.User)
@version(1)
async def login(userIn: userSchema.UserIn, db: Session = Depends(get_db)):
    user = await user_crud.get_user(db, userIn.username)

    if not user:
        user = await user_crud.create_user(db, userIn)

    return user


async def get_generate_token(userIn, db: Session):
    user = await user_crud.authenticate_user(db, userIn.username, userIn.password)

    if not user:
        return { 'error': 'invalid credentials' }

    token = jwt.encode(object_as_dict(user), JWT_SECRET)

    return tokenSchema.Token(access_token=token, token_type='bearer')


@router.post('/token')
@version(1)
async def generate_token(userIn: userSchema.UserIn, db: Session = Depends(get_db)):
    return await get_generate_token(userIn, db)


@router.post('/token/test')
@version(1)
async def generate_test_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await get_generate_token(form_data, db)


@router.get('/user', response_model=userSchema.User)
@version(1)
async def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await user_crud.get_user_by_id(db, id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    
    return user

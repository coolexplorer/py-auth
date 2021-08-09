import logging
import jwt
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_versioning import version
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import schema
from sqlalchemy.orm import Session

import crud.user_crud as user_crud
import schemas.user as userSchema
import schemas.token as tokenSchema
import schemas.base_response as baseResponseSchema
from config import config
from dependencies.database import get_db
from utils.sqlalchemy import object_as_dict
from utils.json import DateTimeEncoder

JWT_SECRET = 'yourownsecret'
logger = logging.getLogger(__name__)
router = APIRouter(tags=['auth'])

# FastAPI security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token/test')


def generate_token(user: userSchema.User, token_expired_time: int) -> str:
    try:
        if not user:
            raise jwt.InvalidTokenError

        payload = object_as_dict(user)
        expired_time = datetime.utcnow() + timedelta(seconds=token_expired_time)
        payload['exp'] = expired_time
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256", json_encoder=DateTimeEncoder)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is expired'
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials'
        )

    return token


async def get_generated_token(userIn, db: Session, token_expired_time: int):
    user = await user_crud.authenticate_user(db, userIn.email, userIn.password)
    return tokenSchema.Token(access_token=generate_token(user, token_expired_time), token_type='bearer')


@router.post('/login', response_model=tokenSchema.Token)
@version(1)
async def login(userIn: userSchema.UserIn, db: Session = Depends(get_db), settings: config.Settings = Depends(config.get_settings)):
    user = await user_crud.get_user(db, userIn.email)

    if not user:
        user = await user_crud.create_user(db, userIn)
    else:
        user = await user_crud.update_user(db, user)

    return await create_token(userIn, db, settings)


@router.post('/token', response_model=tokenSchema.Token)
@version(1)
async def create_token(userIn: userSchema.UserIn, db: Session = Depends(get_db), settings: config.Settings = Depends(config.get_settings)):
    return await get_generated_token(userIn, db, settings.token_expired_time)


@router.post('/token/test')
@version(1)
async def create_test_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await get_generated_token(form_data, db)


@router.get('/user', response_model=userSchema.User)
@version(1)
async def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await user_crud.get_user_by_id(db, id=payload.get('id'))
    except Exception as err:
        logger.debug(f"jwt decode problem : {err}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    
    return user


@router.get('/token/validate')
@version(1)
async def validate_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await user_crud.get_user_by_id(db, id=payload.get('id'))

        if not user:
            raise 
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is invalid.'
        )

    return baseResponseSchema.BaseResponse(result=True)
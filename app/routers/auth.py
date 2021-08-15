import logging
import jwt
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_versioning import version
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud.user_crud as user_crud
import schemas.user as user_schema
import schemas.token as token_schema
import schemas.base_response as base_response_schema
from config import config
from dependencies.database import get_db
from utils.sqlalchemy import object_as_dict
import utils.jwt as jwt_util


logger = logging.getLogger(__name__)
router = APIRouter(tags=['auth'])

# FastAPI security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token/test')


def generate_token(user: user_schema.User, token_expired_time: int) -> str:
    try:
        if not user:
            raise jwt.InvalidTokenError

        payload = object_as_dict(user)
        expired_time = datetime.utcnow() + timedelta(seconds=token_expired_time)
        payload['exp'] = expired_time
        token = jwt_util.encode(payload=payload)
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
    return token_schema.Token(access_token=generate_token(user, token_expired_time))


@router.post('/login', response_model=token_schema.Token)
@version(1)
async def login(userIn: user_schema.UserIn, db: Session = Depends(get_db), settings: config.Settings = Depends(config.get_settings)):
    user = await user_crud.get_user(db, userIn.email)

    if not user:
        user = await user_crud.create_user(db, userIn)
    else:
        user = await user_crud.update_user(db, user)

    return await create_token(userIn, db, settings)


@router.post('/token', response_model=token_schema.Token)
@version(1)
async def create_token(userIn: user_schema.UserIn, db: Session = Depends(get_db), settings: config.Settings = Depends(config.get_settings)):
    return await get_generated_token(userIn, db, settings.token_expired_time)


@router.post('/token/test')
@version(1)
async def create_test_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db), settings: config.Settings = Depends(config.get_settings)):
    return await get_generated_token(form_data, db, settings.jwt_secret)


@router.get('/user', response_model=user_schema.User)
@version(1)
async def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt_util.decode(token)
        user = await user_crud.get_user_by_id(db, id=payload.get('id'))
    except Exception as err:
        logger.debug(f"Invalid Token : {err}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    
    return user


@router.get('/token/validate')
@version(1)
async def validate_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt_util.decode(token)
        user = await user_crud.get_user_by_id(db, id=payload.get('id'))

        if not user:
            raise 
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is invalid.'
        )

    return base_response_schema.BaseResponse(result=True)
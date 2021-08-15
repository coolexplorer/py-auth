import jwt

from config import config
from utils.json import DateTimeEncoder


settings: config.Settings = config.get_settings()


def encode(payload: str) -> str:
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm, json_encoder=DateTimeEncoder)


def decode(token: str) -> dict:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])

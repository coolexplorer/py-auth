import logging
import os
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Postgresql = "postgresql://user:password@postgresserver/db"
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")


@lru_cache
def get_settings() -> BaseSettings:
    logger.info('Loading configurations from environment')
    return Settings()
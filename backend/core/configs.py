from typing import List

from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:miron@localhost:5432/pokebattle'
    DBBaseModel = declarative_base()

    JWT_SECRET: str = 'AZFqg2lgEO0lBKmZRJHpDN7OFeu_kE1NKbZMozb1b60'
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30

    class Config:
        case_sensitive = True


settings: Settings = Settings()
from pytz import timezone

from typing import Optional, List
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from jose import jwt

from models.player_model import PlayerModel
from core.configs import settings
from core.security import verify_password

from pydantic import EmailStr


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/players/login'
)


async def authenticate(email: EmailStr, password: str, db: AsyncSession) -> Optional[PlayerModel]:
    async with db as session:
        query = select(PlayerModel).filter(PlayerModel.email == email)
        result = await session.execute(query)
        player: PlayerModel = result.scalars().unique().one_or_none()

        if not player:
            return None

        if not verify_password(password, player.password):
            return None

        return player


def _create_token(type_token: str, life_time: timedelta, sub: str) -> str:
    payload = {}

    sp = timezone('America/Sao_Paulo')
    expire = datetime.now(tz=sp) + life_time

    payload["type"] = type_token
    payload["exp"] = expire
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def create_access_token(sub: str) -> str:
    return _create_token(
        type_token='access_token',
        life_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )

from typing import List, Optional, Any

from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from models.player_model import PlayerModel
from schemas.player_schema import PlayerSchemaBase, PlayerSchemaCreate, PlayerSchemaUp
from core.deps import get_session, get_current_user
from core.security import generate_password_hash
from core.auth import authenticate, create_access_token


router = APIRouter()


@router.get('/logged', response_model=PlayerSchemaBase)
def get_logged(logged_player: PlayerModel = Depends(get_current_user)):
    return logged_player


@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=PlayerSchemaBase)
async def post_player(player: PlayerSchemaCreate, db: AsyncSession = Depends(get_session)):
    new_player: PlayerModel = PlayerModel(name=player.name, email=player.email,
                                          password=generate_password_hash(player.password), is_admin=player.is_admin)

    async with db as session:
        try:
            session.add(new_player)
            await session.commit()

            return new_player
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='Já existe um jogador cadastrado.')


@router.get('/', response_model=List[PlayerSchemaBase])
async def get_players(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PlayerModel)
        result = await session.execute(query)
        players: List[PlayerSchemaBase] = result.scalars().unique().all()

        return players


@router.put('/{player_id}', response_model=PlayerSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_player(player_id: int, player: PlayerSchemaUp, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PlayerModel).filter(PlayerModel.id == player_id)
        result = await session.execute(query)
        player_up: PlayerSchemaBase = result.scalars().unique().one_or_none()

        if player_up:
            if player.name:
                player_up.name = player.name
            if player.email:
                player_up.email = player.email
            if player.password:
                player_up.password = generate_password_hash(player.password)

            await session.commit()

            return player
        else:
            raise HTTPException(detail='Jogador não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{player_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(player_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PlayerModel).filter(PlayerModel.id == player_id)
        result = await session.execute(query)
        player_del: PlayerSchemaBase = result.scalars().unique().one_or_none()

        if player_del:
            await session.delete(player_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Jogador não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    player = await authenticate(email=form_data.username, password=form_data.password, db=db)

    if not player:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Dados de acesso incorretos.')

    return JSONResponse(content={"access_token": create_access_token(sub=player.id), "token_type": "bearer"},
                        status_code=status.HTTP_200_OK)
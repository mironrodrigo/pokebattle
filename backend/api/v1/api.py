from fastapi import APIRouter

from api.v1.endpoints import player, pokemon


api_router = APIRouter()

api_router.include_router(pokemon.router, prefix='/pokemons', tags=['pokemons'])
api_router.include_router(player.router, prefix='/players', tags=['players'])
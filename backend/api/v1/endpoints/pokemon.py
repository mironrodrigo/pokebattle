from typing import List

from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.pokemon_model import PokemonModel
from models.player_model import PlayerModel
from schemas.pokemon_schema import PokemonSchema
from core.deps import get_session, get_current_user


router = APIRouter()


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PokemonSchema)
async def post_pokemon(
    pokemon: PokemonSchema,
    db: AsyncSession = Depends(get_session),
    logged_player: PlayerModel = Depends(get_current_user)
):
    new_pokemon: PokemonModel = PokemonModel(
        name=pokemon.name,
        type=pokemon.type,
        class_=pokemon.class_,
        rarity=pokemon.rarity,
        level=pokemon.level,
        health_points=pokemon.health_points,
        physical_attack=pokemon.physical_attack,
        elemental_attack=pokemon.elemental_attack,
        physical_defense=pokemon.physical_defense,
        elemental_defense=pokemon.elemental_defense,
        speed=pokemon.speed,
        critical=pokemon.critical,
        evasion=pokemon.evasion,
        image_url=pokemon.image_url
    )

    db.add(new_pokemon)
    await db.commit()

    return new_pokemon


@router.get('/', response_model=List[PokemonSchema])
async def get_pokemons(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PokemonModel)
        result = await session.execute(query)
        pokemons: List[PokemonModel] = result.scalars().unique().all()

        return pokemons


@router.get('/{pokemon_id}', response_model=PokemonSchema, status_code=status.HTTP_200_OK)
async def get_pokemon_by_id(pokemon_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(PokemonModel).filter(PokemonModel.id == pokemon_id)
        result = await session.execute(query)
        pokemon: PokemonModel = result.scalars().unique().one_or_none()

        if pokemon:
            return pokemon
        else:
            raise HTTPException(detail='Pokemon não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


@router.put('/{pokemon_id}', response_model=PokemonSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_pokemon(
    pokemon_id: int,
    pokemon: PokemonSchema,
    db: AsyncSession = Depends(get_session),
    logged_player: PlayerModel = Depends(get_current_user)
):
    async with db as session:
        query = select(PokemonModel).filter(PokemonModel.id == pokemon_id)
        result = await session.execute(query)
        pokemon_up: PokemonModel = result.scalars().unique().one_or_none()

        if pokemon_up:
            if pokemon.name:
                pokemon_up.name = pokemon.name
            if pokemon.type:
                pokemon_up.type = pokemon.type
            if pokemon.class_:
                pokemon_up.class_ = pokemon.class_
            if pokemon.rarity:
                pokemon_up.rarity = pokemon.rarity
            if pokemon.level:
                pokemon_up.level = pokemon.level
            if pokemon.health_points:
                pokemon_up.health_points = pokemon.health_points
            if pokemon.physical_attack:
                pokemon_up.physical_attack = pokemon.physical_attack
            if pokemon.elemental_attack:
                pokemon_up.elemental_attack = pokemon.elemental_attack
            if pokemon.physical_defense:
                pokemon_up.physical_defense = pokemon.physical_defense
            if pokemon.elemental_defense:
                pokemon_up.elemental_defense = pokemon.elemental_defense
            if pokemon.speed:
                pokemon_up.speed = pokemon.speed
            if pokemon.critical:
                pokemon_up.critical = pokemon.critical
            if pokemon.evasion:
                pokemon_up.evasion = pokemon.evasion
            if pokemon.image_url:
                pokemon_up.image_url = pokemon.image_url

            await session.commit()

            return pokemon_up
        else:
            raise HTTPException(detail='Pokemon não encontrado.', status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{pokemon_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_pokemon(
    pokemon_id: int,
    db: AsyncSession = Depends(get_session),
    logged_player: PlayerModel = Depends(get_current_user)
):
    async with db as session:
        query = select(PokemonModel).filter(PokemonModel.id == pokemon_id)
        result = await session.execute(query)
        pokemon_del: PokemonModel = result.scalars().unique().one_or_none()

        if pokemon_del:
            await session.delete(pokemon_del)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(detail='Pokemon não encontrado.', status_code=status.HTTP_404_NOT_FOUND)
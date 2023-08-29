from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.configs import settings


class PokemonModel(settings.DBBaseModel):
    """
    Pokémon e.g.:
    id = 1
    name = bulbasaur
    type = grass
    class_ = suport
    level = 1
    health_points = 89
    physical_attack = 25
    elemental_attack = 52
    physical_defense = 48
    elemental_defense = 55
    speed = 44
    critical = 5
    evasion = 5
    image_url = https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/1.png
    """

    __tablename__ = 'pokemons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), index=True, nullable=False)
    type = Column(String(256), index=True, nullable=False)
    class_ = Column(String(256), index=True, nullable=False)
    rarity = Column(String(256), index=True, nullable=False)
    level = Column(Integer, nullable=False)
    health_points = Column(Integer, nullable=False)
    physical_attack = Column(Integer, nullable=False)
    elemental_attack = Column(Integer, nullable=False)
    physical_defense = Column(Integer, nullable=False)
    elemental_defense = Column(Integer, nullable=False)
    speed = Column(Integer, nullable=False)
    critical = Column(Integer, nullable=False)
    evasion = Column(Integer, nullable=False)
    image_url = Column(String, nullable=False)
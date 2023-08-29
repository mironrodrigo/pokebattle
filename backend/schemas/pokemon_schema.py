from typing import Optional

from pydantic import BaseModel as SCBaseModel, HttpUrl


class PokemonSchema(SCBaseModel):
    id: Optional[int] = None
    name: str
    type: str
    class_: str
    rarity: str
    level: int
    health_points: int
    physical_attack: int
    elemental_attack: int
    physical_defense: int
    elemental_defense: int
    speed: int
    critical: int
    evasion: int
    image_url: HttpUrl

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

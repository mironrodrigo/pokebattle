from typing import Optional, List

from pydantic import BaseModel as SCBaseModel, EmailStr


class PlayerSchemaBase(SCBaseModel):
    id: Optional[int] = None
    name: str
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PlayerSchemaCreate(PlayerSchemaBase):
    password: str


class PlayerSchemaUp(PlayerSchemaBase):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    is_admin = bool

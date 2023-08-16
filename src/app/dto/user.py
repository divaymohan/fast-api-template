from typing import List, Union
from pydantic import BaseModel
from src.app.dto.item import Item


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class ConfigDict:
        orm_mode = True

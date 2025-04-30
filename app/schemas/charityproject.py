# app/schemas/charityproject.py

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(
        None, min_length=1, max_length=100, title='Название проекта')
    description: Optional[str] = Field(None, min_length=1, title='Описание')
    full_amount: Optional[int] = Field(None, ge=1, title='Сумма')

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(
        ..., min_length=1, max_length=100, title='Название проекта')
    description: str = Field(..., min_length=1, title='Описание')
    full_amount: int = Field(..., ge=1, title='Сумма')


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    pass

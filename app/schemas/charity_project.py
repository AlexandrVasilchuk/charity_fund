from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator
from pydantic.schema import datetime

MINIMAL_LENGHT = 1
MAXIMAL_LENGTH = 100
MINIMAL_INT_VAlUE = 0
DEFAULT_INT_VALUE = 0

PROJECT_NAME_NOT_NULL = 'Имя проекта не может быть пустым'
PROJECT_DESCRIPTION_NOT_NULL = 'Описание не может быть пустым'


class CharityProjectBase(BaseModel):
    name: str = Field(min_length=MINIMAL_LENGHT, max_length=MAXIMAL_LENGTH)
    description: str = Field(min_length=MINIMAL_LENGHT)
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    @validator('name')
    def name_not_null(cls, value: str) -> str:
        if value is None:
            raise ValueError(PROJECT_NAME_NOT_NULL)
        return value

    @validator('description')
    def description_not_null(cls, value: str) -> str:
        if value is None:
            raise ValueError(PROJECT_DESCRIPTION_NOT_NULL)
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=MINIMAL_LENGHT, max_length=MAXIMAL_LENGTH
    )
    description: Optional[str] = Field(None, min_length=MINIMAL_LENGHT)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid

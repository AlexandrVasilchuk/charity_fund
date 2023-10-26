from typing import Optional

from pydantic import BaseModel, PositiveInt
from pydantic.schema import datetime


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationDBShort(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationDBShort):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]


class DonationUpdate(BaseModel):
    """Схема заглушка для корректной аннотации CRUD класса."""

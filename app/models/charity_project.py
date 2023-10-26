from sqlalchemy import Column, String, Text

from app.models.base import AbstractBase

NAME_MAX_LENGTH = 100


class CharityProject(AbstractBase):
    name = Column(String(NAME_MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}(Полная сумма: {self.full_amount}, Закрыт: {self.fully_invested})'

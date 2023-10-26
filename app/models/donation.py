from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import AbstractBase


class Donation(AbstractBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return f'{self.__class__.__name__}(Полная сумма: {self.full_amount}, Закрыт: {self.fully_invested})'

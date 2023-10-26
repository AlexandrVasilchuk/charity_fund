import datetime

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class ProjectDonationBase(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount <= full_amount'),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=int)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        attributes = (
            self.full_amount,
            self.invested_amount,
            self.fully_invested,
            self.create_date,
            self.close_date,
        )
        return f'{self.__class__.__name__}{attributes}'

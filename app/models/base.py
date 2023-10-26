import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


def update_close_date(context):
    if context and context.current_parameters.get('fully_invested') is True:
        return datetime.datetime.now()
    return None


class AbstractBase(Base):
    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=int)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.datetime.now)
    close_date = Column(
        DateTime, default=update_close_date, onupdate=update_close_date
    )

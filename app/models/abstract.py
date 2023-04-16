from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, CheckConstraint

from app.core.db import Base

REPRESENTATION_BASE_CLASS = (
    'full_amount: {full_amount}, '
    'invested_amount: {invested_amount}, '
    'fully_invested: {fully_invested}, '
    'create_date: {create_date}, '
    'close_date: {close_date}'
)


class AbstractBaseClass(Base):
    __abstract__ = True
    __table_args__ = (
        CheckConstraint('full_amount > 0'),
        CheckConstraint('invested_amount <= full_amount'),
    )

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    def __repr__(self):
        return REPRESENTATION_BASE_CLASS.format(
            full_amount=self.full_amount,
            invested_amount=self.invested_amount,
            fully_invested=self.fully_invested,
            created_date=self.create_date,
            close_data=self.close_date
        )

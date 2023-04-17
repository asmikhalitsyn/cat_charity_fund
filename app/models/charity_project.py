from sqlalchemy import Column, String, Text

from .abstract import InvestmentDate

REPRESENTATION_CHARITY_PROJECT = (
    'name: {name:.16}, '
    'description: {description:.16}, '
    'base: {base}'
)


class CharityProject(InvestmentDate):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return REPRESENTATION_CHARITY_PROJECT.format(
            name=self.name,
            description=self.description,
            base=super().__repr__(),
        )

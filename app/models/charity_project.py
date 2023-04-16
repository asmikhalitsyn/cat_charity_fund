from sqlalchemy import Column, String, Text

from .abstract import AbstractBaseClass

REPRESENTATION_CHARITY_PROJECT = (
    'name: {name}, '
    'description: {description}, '
    'base: {base}'
)


class CharityProject(AbstractBaseClass):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return REPRESENTATION_CHARITY_PROJECT.format(
            name=self.name,
            description=self.description[:16],
            base=super().__repr__(),
        )

from sqlalchemy import Column, ForeignKey, Integer, Text

from .abstract import AbstractBaseClass


REPRESENTATION_DONATION = (
    'user_id: {name}, '
    'comment: {comment}, '
    'base: {base}'
)


class Donation(AbstractBaseClass):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return REPRESENTATION_DONATION.format(
            user_id=self.user_id,
            comment=self.comment[:16],
            base=super().__repr__()
        )

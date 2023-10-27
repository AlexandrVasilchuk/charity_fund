import re

from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import ProjectDonationBase


class Donation(ProjectDonationBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        attributes = re.sub(
            r'\)$', f', {self.user_id}, {self.comment})', super().__repr__()
        )
        return attributes

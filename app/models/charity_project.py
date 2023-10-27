import re

from sqlalchemy import Column, String, Text

from app.models.base import ProjectDonationBase

NAME_MAX_LENGTH = 100


class CharityProject(ProjectDonationBase):
    name = Column(String(NAME_MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        attributes = re.sub(
            r'\)$', f', {self.name}, {self.description})', super().__repr__()
        )
        return attributes

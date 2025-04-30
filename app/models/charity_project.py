# app/models/charityproject.py
from sqlalchemy import Column, Integer, String, Text

from app.core.db import Base
from app.models.base_project_donation import BaseProjectDonationMixin


class CharityProject(Base, BaseProjectDonationMixin):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)

    def __repr__(self):
        return (f'Проект: {self.name}')

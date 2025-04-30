# app/models/donation.py
from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.base_project_donation import BaseProjectDonationMixin


class Donation(Base, BaseProjectDonationMixin):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
    full_amount = Column(Integer, nullable=False)

    def __repr__(self):
        return (f'Пожертвование на сумму {self.full_amount}')

# app/models/base_project_donation.py
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer


class BaseProjectDonationMixin:
    """Миксин для добавления одинаковых полей в модели."""

    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)

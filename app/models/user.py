# app/models/user.py
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Класс пользователя берется 'по умолчанию'."""

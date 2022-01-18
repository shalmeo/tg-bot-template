from sqlalchemy import Column, BigInteger, Boolean

from .base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'Users'
    
    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    allow = Column(Boolean)
from sqlalchemy import BigInteger, Boolean, Column, Integer, String

from tgbot.services.database.base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'User'
    
    id = Column(BigInteger, primary_key=True)
    full_name = Column(String(255), nullable=False)
    status = Column(Boolean, default=False, nullable=False)


class Trash(TimedBaseModel):
    __tablename__ = 'Trash'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
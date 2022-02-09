from sqlalchemy import Column, BigInteger, Boolean, Integer, String, ARRAY

from .base import TimedBaseModel


class User(TimedBaseModel):
    __tablename__ = 'Users'
    
    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    full_name = Column(String(255), nullable=False)
 
    def __str__(self):
        return f'user_id - {self.user_id}\nfull_name - {self.full_name}'
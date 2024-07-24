from app.db import Base
from sqlalchemy import Column, Integer, String

# user class inherits from the Base class; the properties in the user class will be used by the parent Base class to create the table

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)


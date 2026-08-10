from sqlalchemy import Column, Integer, String
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, index=True , nullable=False)
    email = Column(String, index=True , )
    hash_password = Column(String, index=True , nullable=False)
from sqlalchemy import Column, Integer, String
from src.utils.db import Base

class Task(Base):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_completed = Column(String, index=True)
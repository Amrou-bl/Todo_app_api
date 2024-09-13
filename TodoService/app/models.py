from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text



class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, default=text('now()'))
    user_id = Column(Integer)
    
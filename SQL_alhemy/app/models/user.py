from fastapi import APIRouter, Depends
from app.backend.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Session
from app.backend.db_depends import get_db
from typing import Annotated


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    firstname = Column(String)
    lastname = Column(String)
    age = Column(Integer)
    slug = Column(String, unique=True, index=True)

    tasks = relationship('Task', back_populates='user')




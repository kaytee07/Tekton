#!/usr/bin/python3
"""
creat user class that inherit from BaseModel
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import relationship
from os import getenv

TK_TYPE_STORAGE = getenv('TK_TYPE_STORAGE')


class User(BaseModel, Base):
    """
    user class that describes the user
    """
    __tablename__ = 'users'

    if TK_TYPE_STORAGE == 'db':
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        username = Column(String(60), nullable=False)
        user_type = Column(String(60))
        email = Column(String(60), nullable=False)
        password = Column(String(140), nullable=False)
        phone_no = Column(Integer)
        salt = Column(LargeBinary)
    else:
        first_name = None
        last_name = None
        username = None
        email = None
        salt = None
        password = None

    def __init__(self, *args, **kwargs):
        """
        inherit BaseModel methods and attributes
        """
        super().__init__(*args, **kwargs)

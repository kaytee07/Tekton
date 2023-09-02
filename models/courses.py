#!/usr/bin/python3
"""
creat user class that inherit from BaseModel
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import relationship
from os import getenv

SD_TYPE_STORAGE = getenv('SD_TYPE_STORAGE')


class Course(BaseModel, Base):
    """
    user class that describes the user
    """
    __tablename__ = 'courses'

    if SD_TYPE_STORAGE == 'db':
        name = Column(String(128), nullable=False)
        no_of_students = Column(Integer, nullable=False)
        students = relationship('Student', backref="course")
    else:
        course_name = None
        no_of_students = None

    def __init__(self, *args, **kwargs):
        """
        inherit BaseModel methods and attributes
        """
        super().__init__(*args, **kwargs)

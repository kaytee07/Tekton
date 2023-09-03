#!/usr/bin/python3
"""
creat user class that inherit from BaseModel
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.types import LargeBinary
from sqlalchemy.orm import relationship
from os import getenv

TK_TYPE_STORAGE = getenv('TK_TYPE_STORAGE')


class Student(BaseModel, Base):
    """
    user class that describes the user
    """
    __tablename__ = 'students'

    if TK_TYPE_STORAGE == 'db':
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        course_id = Column(String(128), ForeignKey('courses.id'))
        cohort_id = Column(String(128), ForeignKey('cohorts.id'))
        Phone_no = Column(Integer, nullable=False)
        age = Column(Integer, nullable=False)
        email = Column(String(60), nullable=False)
    else:
        first_name = None
        last_name = None
        course_id = None
        cohort_id = None
        Phone_no = None
        age = None
        email = None

    def __init__(self, *args, **kwargs):
        """
        inherit BaseModel methods and attributes
        """
        super().__init__(*args, **kwargs)

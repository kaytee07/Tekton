#!/usr/bin/python3
"""
creat user class that inherit from BaseModel
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.types import LargeBinary
from datetime import datetime

from sqlalchemy.orm import relationship
from os import getenv

SD_TYPE_STORAGE = getenv('SD_TYPE_STORAGE')


class Cohort(BaseModel, Base):
    """
    user class that describes the user
    """
    __tablename__ = 'cohorts'

    if SD_TYPE_STORAGE == 'db':
        cohort_no = Column(Integer, nullable=False, autoincrement=True)
        start_date = Column(DateTime, nullable=False)
        end_date = Column(DateTime, nullable=False)
        students = relationship('Student', backref='cohort')
    else:
        cohort_no = None
        start_date = None
        end_date = None
        students = None

    def __init__(self, *args, **kwargs):
        """
        inherit BaseModel methods and attributes
        """
        super().__init__(*args, **kwargs)

    def start_date():
        start_date = datetime.utcnow()

    def end_date():
        end_date = datetime.utcnow()

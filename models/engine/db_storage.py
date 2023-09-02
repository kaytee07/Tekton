#!/usr/bin/python3
"""
store attributes in database
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.users import User
from models.courses import Course
from models.cohorts import Cohort
from models.students import Student


classes = {'User': User, 'Course': Course, 'Cohort': Cohort, 'Student': Student}

classes


class DBStorage:
    """
    store object attribute in database
    """
    __engine = None
    __session = None

    def __init__(self):
        TK_MYSQL_USER = getenv('TK_MYSQL_USER')
        TK_MYSQL_PWD = getenv('TK_MYSQL_PWD')
        TK_MYSQL_HOST = getenv('TK_MYSQL_HOST')
        TK_MYSQL_DB = getenv('TK_MYSQL_DB')
        TK_ENV = getenv('TK_ENV')

        dburl = "mysql+mysqldb://{}:{}@{}/{}".format(TK_MYSQL_USER,
                                                     TK_MYSQL_PWD,
                                                     TK_MYSQL_HOST,
                                                     TK_MYSQL_DB)

        self.__engine = create_engine(dburl, pool_pre_ping=True)

        if TK_ENV == 'test':
            Base.metadata.drop_all()

    def all(self, cls=None):
        """
        get all object based on their class name and if cls = None
        query all object types in Database
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj=None):
        """
        add object to the session
        """
        self.__session.add(obj)

    def save(self):
        """
        commit all changes to the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        delete object from the current database session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        create tables in database and create database session
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        self.__session = Session()

    def get(self, cls, id=None, username=None, container_id=None):
        """
        get user based on user id passed or  username
        """
        if cls:
            if id:
                obj = self.__session.query(cls).filter_by(id=id).first()
                return obj
            elif username:
                obj = self.__session.query(cls).filter_by(username=username).first()
                return obj
            elif container_id:
                obj = self.__session.query(cls).filter_by(container_id=container_id).first()
                return obj
        else:
            None

    def count(self, cls=None):
        """
        count entries in tables based on the class object passed
        """
        if cls:
            count = self.__session.query(cls).count()
            return count
        else:
            count = 0
            for class_name, class_obj in classes.items():
                count += self.__session.query(class_obj).count()
            return count

    def close(self):
        """
        close session
        """
        self.__session.close()

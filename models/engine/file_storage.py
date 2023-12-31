#!/bin/usr/python3
"""
instance attributes will now be persistent
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.cohort import Cohort
from models.course import Course
from models.student import Student


classes = {'BaseModel': BaseModel, 'User': User, 'Cohort': Cohort, 'Course': Course, 'Student': Student}


class FileStorage:
    """
    store class attributes in file
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        returns the dictionary __objects
        """
        if cls:
            new_obj = {}
            new_cls = str(cls).split('.')[2].split("'")[0]
            for key, value in self.__objects.items():
                if new_cls == value.to_dict()['__class__']:
                    new_obj[key] = value
            return new_obj
        else:
            return self.__objects

    def new(self, obj):
        """
        set in the the __objects with the class objects
        """
        key = f"{obj.to_dict()['__class__']}.{obj.to_dict()['id']}"
        self.__objects[key] = obj

    def save(self):
        """
        serialize __objects to the JSON file
        (path:__file_path)
        """
        data = {}
        for key, value in self.__objects.items():
            data[key] = value.to_dict()
        with open(self.__file_path, 'w') as file:
            json.dump(data, file)

    def reload(self):
        """
        deserialize json file to objects if only json file path
        exist
        """
        try:
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
            for key, value in data.items():
                obj = classes[value['__class__']](**data[key])
                self.__objects[key] = obj
        except json.JSONDecodeError:
            pass

    def delete(self, obj=None):
        if obj:
            key = f"{obj.to_dict()['__class__']}.{obj.to_dict()['id']}"
            del self.__objects[key]

    def get(self, cls, id):
        """ Retrieve one object from storage """
        if cls:
            name = str(cls).split('.')[2].split("'")[0]
            key = f"{name}.{id}"
            return self.__objects[key]
        else:
            return None

    def count(self, cls=None):
        number = 0
        if cls:
            for key, value in self.__objects.items():
                name = str(cls).split('.')[2].split("'")[0]
                if value.to_dict()['__class__'] == name:
                    number += 1
        else:
            for key, value in self.__objects.items():
                number += 1
        return number

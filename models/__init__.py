#!/usr/bin/python3
"""
create instance of file storage and deserialze json file
"""
from os import getenv

TK_TYPE_STORAGE = getenv('TK_TYPE_STORAGE')
if TK_TYPE_STORAGE == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()

#!/usr/bin/python3
"""
all user apis including login and logout page
"""

from flask import abort, render_template, request, jsonify
from api.v1.views import app_views
from models.users import User
import os
import hashlib
import binascii


def hash_password(password, salt=None):
    rounds = 100000
    hash_algo = hashlib.sha256()

    if salt is None:
        salt = os.urandom(16)
        hk = hashlib.pbkdf2_hmac(hash_algo.name, password.encode('utf-8'), salt, rounds)
        hashed_password = binascii.hexlify(hk).decode('utf-8')
        return {"passwd": hashed_password, "salt": salt}
    else:
        salt_bytes = binascii.unhexlify(salt)
        hk = hashlib.pbkdf2_hmac(hash_algo.name, password.encode('utf-8'), salt_bytes, rounds)
        hashed_password = binascii.hexlify(hk).decode('utf-8')
        return hashed_password


@app_views.route('/createuser', strict_slashes="False", methods=['GET', 'POST'])
def createuser():
    """
    create user who can check registered kids
    """
    data = request.get_json()

    if not data:
        abort(404, description="absolutely no data")

    if 'password' not in data:
        abort(404, description="No password")

    if 'email' not in data:
        abort(404, description="No email")

    if 'phone_no' not in data:
        abort(404, description="No phone_no")

    hashed_data = hash_password(data['password'])
    data['password'] = hashed_data['passwd']
    data['salt'] = hashed_data['salt']
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict())


@app_views.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    """
    login as user online
    """
    pass

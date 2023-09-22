#!/usr/bin/python3
"""
all user apis including login and logout page
"""

from flask import abort, render_template, request, jsonify, session, redirect, url_for, flash
from api.v1.views import app_views
from models import storage
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

def all_users():
    all_users = storage.all('User')
    cohort_list = []
    for value in all_users.values():
        cohort_list.append(value.to_dict())
    return cohort_list


@app_views.route('/createuser', strict_slashes=False, methods=['GET', 'POST'])
def createuser():
    """
    create user who can check registered kids
    """
    if request.method == 'POST':
        data = request.get_json()

        if not data:
            abort(404, description="absolutely no data")

        if 'password' not in data:
            abort(404, description="No password")

        if 'email' not in data:
            abort(404, description="No email")

        if 'phone_no' not in data:
            abort(404, description="No phone_no")

        hashed_pass = hash_password(data['password'])
        data['password'] = hashed_pass['passwd']
        data['salt'] = hashed_pass['salt']
        new_user = User(**data)
        new_user.save()
        return redirect(url_for('appviews.login'))
    else:
        return render_template('signin.html')


@app_views.route('/login', strict_slashes=False, methods=['GET', 'POST'])
def login():
    """
    login as user online
    """
    if request.method == 'POST':
        data = request.form

        if not data:
            abort(404, description="absolutely no data")

        user = storage.get(User, username=data['user'])

        if user:
            user_dict = user.to_dict()
            if hash_password(data['pass'], user_dict['salt']) == user_dict['password']:
                session['user_id'] = user_dict['id']
                session['username'] = user_dict['username']
                return redirect(url_for('appviews.home'))
            else:
                flash('incorrect username and password')
                return render_template('login.html')
        else:
            flash('user cannot be found')
            return render_template('login.html')
    else:
        return render_template('login.html')

@app_views.route('/updateuser/<id>', strict_slashes=False, methods=['POST'])
def updateuser(id):
    """
    update user
    """
    get_user = storage.get(User, id=id)
    if get_user:
        data = request.get_json()
        if 'first_name' in data:
            get_user.first_name = data['first_name']
        if 'last_name' in data:
            get_user.last_name = data['last_name']
        if 'username' in data:
            get_user.username = data['username']
        if 'user_type' in data:
            get_user.user_type = data['user_type']
        if 'email' in data:
            get_user.email = data['email']

        get_user.save()
        return jsonify(get_user.to_dict())
    else:
        abort(404)


@app_views.route('/deleteuser/<id>', strict_slashes=False, methods=['POST'])
def deleteuser(id):
    """
    delete user
    """
    get_user = storage.get(User, id=id)
    if get_user:
        get_user.delete()
        storage.save()
        flash("deleted successfully")
        return jsonify(all_users()), 200
    else:
        abort(404)


@app_views.route('/home', strict_slashes=False, methods=['GET'])
def home():
    """
    home of user'
    """
    if 'user_id' in session:
        id = session.get('user_id')
        username = session.get('username')
        return render_template('home.html', id=id, username=username)
    else:
        flash('You need to log in to access this page.', 'danger')
        return redirect(url_for('appviews.login'))


@app_views.route('/logout', strict_slashes=False, methods=['POST'])
def logout():
    """
    user logout
    """
    session.clear()
    return redirect(url_for('appviews.login'))

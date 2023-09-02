#!/usr/bin/python3
"""
register blueprint to flask
"""
from flask import Blueprint

app_views = Blueprint("appviews", __name__)

from api.v1.views.users import *

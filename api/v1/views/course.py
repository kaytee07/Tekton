#!/usr/bin/python3
"""
all user apis including login and logout page
"""

from flask import abort, render_template, request, jsonify, session
from api.v1.views import app_views
from models import storage
from models.courses import Course


@app_views.route('/createcourse', strict_slashes=False, methods=['GET', 'POST'])
def createcourse():
    """
    create user who can check registered kids
    """
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(404, description="absolutely no data")

        if 'name' not in data:
            abort(404, description="No name passed")

        if 'no_of_students' not in data:
            abort(404, description="No no_of student")

        print(data)
        new_course = Course(**data)
        new_course.save()
        return jsonify(new_course.to_dict())
    else:
        return jsonify({"return": "success"})


@app_views.route('/allcourses', strict_slashes=False , methods=['GET'])
def get_all_courses():
    """
    get all courses
    """
    all_courses = storage.all('Course')
    course_list = []
    for value in all_courses.values():
        course_list.append(value.to_dict())
    return jsonify(course_list), 200

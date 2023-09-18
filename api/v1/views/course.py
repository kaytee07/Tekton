#!/usr/bin/python3
"""
all user apis including login and logout page
"""

from flask import abort, render_template, request, jsonify, session, redirect, url_for, flash
from api.v1.views import app_views
from models import storage
from models.courses import Course


@app_views.route('/createcourse', strict_slashes=False, methods=['GET', 'POST'])
def createcourse():
    """
    create user who can check registered kids
    """
    if request.method == 'POST':
        if 'user_id' in session:
            new_data = request.form
            print(new_data)
            if not new_data:
                abort(404, description="absolutely no data")

            if 'name' not in new_data:
                print('prob')
                abort(404, description="No name passed")

            if 'no_of_students' not in new_data:
                abort(404, description="No no_of student")

            data = new_data.to_dict()
            new_course = Course(**data)
            new_course.save()
            flash('course sucessfully created')
            return render_template('course.html', results="success")
    else:
        if 'user_id' in session:
            return render_template('course.html')
        else:
            flash('login to get access')
            redirect(url_for('appviews.login'))


@app_views.route('/allcourses', strict_slashes=False, methods=['GET'])
def get_all_courses():
    """
    get all courses
    """
    all_courses = storage.all('Course')
    course_list = []
    for value in all_courses.values():
        course_list.append(value.to_dict())
    return jsonify(course_list), 200

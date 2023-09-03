#!/usr/bin/python3
"""
all user apis including login and logout page
"""

from flask import abort, render_template, request, jsonify, session
from api.v1.views import app_views
from models import storage
from models.cohorts import Cohort
from models.courses import Course
from models.students import Student


@app_views.route('/createstudent', strict_slashes=False, methods=['GET', 'POST'])
def createstudent():
    """
    create a new cohort
    """
    if request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(404, description="absolutely no data")

        if 'first_name' not in data:
            abort(404, description="no first_name")

        if 'last_name' not in data:
            abort(404, description="no last_name")

        if 'age' not in data:
            abort(404, description="no age")

        if 'Phone_no' not in data:
            abort(404, description="No no_of student")

        course = storage.get(Course, coursename=data['course_name'])
        cohort = storage.get(Cohort, cohort_no=data['cohort_no'])
        if course and cohort:
            course_dict = storage.get(Course, coursename=data['course_name']).to_dict()
            cohort_dict = storage.get(Cohort, cohort_no=data['cohort_no']).to_dict()
            data['course_id'] = course_dict['id']
            data['cohort_id'] = cohort_dict['id']
            new_student = Student(**data)
            new_student.save()
            course.no_of_students = course_dict['no_of_students'] + 1
            cohort.no_of_students = cohort_dict['no_of_students'] + 1
            course.save()
            cohort.save()
            return jsonify(new_student.to_dict())
    else:
        return jsonify({"return": "success"})


@app_views.route('/allstudents', strict_slashes=False , methods=['POST'])
def get_all_student():
    """
    get all student
    """
    all_students = storage.all('Student')
    student_list = []
    for value in all_students.values():
        student_list.append(value.to_dict())
    return jsonify(student_list), 200

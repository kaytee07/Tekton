#!/usr/bin/python3
"""
all user apis including login and logout page
"""

from flask import abort, render_template, request, jsonify, session, flash, redirect, url_for
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
        new_data = request.form
        if not new_data:
            abort(404, description="absolutely no data")

        if 'first_name' not in new_data:
            abort(404, description="no first_name")

        if 'last_name' not in new_data:
            abort(404, description="no last_name")

        if 'age' not in new_data:
            abort(404, description="no age")

        if 'phone_no' not in new_data:
            abort(404, description="No phone_no")
        data = new_data.to_dict()
        cohort_num = 1
        course = storage.get(Course, coursename=data['course_name'])
        cohort = storage.get(Cohort, cohort_no=cohort_num)
        if course and cohort:
            course_dict = course.to_dict()
            cohort_dict = cohort.to_dict()
            data['course_id'] = course_dict['id']
            data['cohort_id'] = cohort_dict['id']
            new_student = Student(**data)
            new_student.save()
            if course.no_of_students == 20:
                flash('peak student reached, wait for next cohort or choose different course')
                return render_template('register.html')
            course.no_of_students = course_dict['no_of_students'] + 1
            cohort.no_of_students = cohort_dict['no_of_students'] + 1
            course.save()
            cohort.save()
            flash('registered successfully')
            return render_template('register.html')
    else:
        return render_template('register.html')


@app_views.route('/students/<cohort_no>/<course_name>', strict_slashes=False , methods=['POST'])
def get_all_student(cohort_no, course_name):
    """
    get all student
    """
    course = storage.get(Course, coursename=course_name)
    if course:
        course_dict = storage.get(Course, coursename=course_name).to_dict()
        cohort_dict = storage.get(Cohort, cohort_no=int(cohort_no)).to_dict()
        course_id = course_dict['id']
        cohort_id = cohort_dict['id']
        all_students = storage.all('Student')
        student_course_cohort = []
        for value in all_students.values():
            if value.to_dict()['course_id'] == course_id and value.to_dict()['cohort_id'] == cohort_id:
                student_course_cohort.append(value.to_dict())
        return jsonify(student_course_cohort)
    else:
        return redirect(url_for('appviews.home'))

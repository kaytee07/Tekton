#!/usr/bin/python3
"""
all user apis including login and logout page
"""

from flask import abort, render_template, request, jsonify, session, flash, url_for, current_app, make_response
from flask import redirect
from api.v1.views import app_views
from models import storage
from flask_mail import Message
from models.cohorts import Cohort
from models.courses import Course
from models.students import Student
from os import getenv
import requests
import json
import uuid
import time
from urllib.parse import urlencode


email_address = getenv('TK_EMAIL_ADDRESS')
PAYSTACK_KEY = getenv('TK_PAYSTACK_KEY')


def generate_unique_reference():
    unique_id = str(uuid.uuid4()).replace('-', '')[:12]

    timestamp = int(time.time())

    unique_reference = f'{timestamp}{unique_id}'

    return unique_reference


def pay_fees(amount, email, unique_reference, data):
    """
    PAYMENT VIA PAYSTACK API
    """
    paystack_url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {PAYSTACK_KEY}",
        "Content-Type": "application/json"
    }
    print(unique_reference)

    callback_url = url_for('appviews.payment_callback', _external=True)
    callback_url_with_params = f"{callback_url}?{urlencode(data)}"

    payment_data = {
        'amount': amount,
        'email': email,
        'currency': 'GHS',
        'reference': unique_reference,
        'callback_url': callback_url_with_params
    }

    response = requests.post(paystack_url, json=payment_data, headers=headers)
    response_json = response.json()
    return response_json['data']['authorization_url']


def email(email, message):
    mail = current_app.extensions['mail']

    msg = Message('Subject: Registration Successful',
                  sender=email_address,
                  recipients=[email])
    msg.body = message
    mail.send(msg)
    print("Email sent Successfully")


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
            return redirect(pay_fees(400, data['email'], generate_unique_reference(), data))
        else:
            return (jsonify({'response': 'no_cohort'}))
    else:
        return render_template('register.html')


@app_views.route('/students/<cohort_no>/<course_name>', strict_slashes=False, methods=['POST'])
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
        storage.close()
        return jsonify(student_course_cohort)
    else:
        return redirect(url_for('appviews.home'))


@app_views.route('/payment_callback', methods=['GET'])
def payment_callback():
    """
    Retrieve the payment callback data
    """
    data = request.args.to_dict()
    print(data)

    if data['trxref'] and data['reference']:
        cohort_num = 1
        course = storage.get(Course, coursename=data['course_name'])
        cohort = storage.get(Cohort, cohort_no=cohort_num)
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
        message = f"{data['first_name']} {data['last_name']}, You have successfully registered for the {data['course_name']} Course at Tekton institute"
        email(data['email'], message)
        flash('registered successfully')
        return render_template('register.html')
        additional_data = request.args.to_dict()
    else:
        flash(f"Payment failed. Error message: payment failed")
        return render_template('register.html')

#!/usr/bin/python3
"""
all user apis including login and logout page
"""

from flask import abort, render_template, request, jsonify, session, redirect, url_for, flash
from api.v1.views import app_views
from models import storage
from models.cohorts import Cohort


@app_views.route('/createcohort', strict_slashes=False, methods=['GET', 'POST'])
def createcohort():
    """
    create a new cohort
    """
    if request.method == 'POST':
        if 'user_id' in session:
            new_data = request.form
            if not new_data:
                abort(404, description="absolutely no data")

            data = new_data.to_dict()
            data['no_of_students'] = 0
            new_cohort = Cohort(**data)
            new_cohort.save()
            flash('cohort successfully created')
            return render_template('cohort.html', result="success")
    else:
        if 'user_id' in session:
            return render_template('cohort.html')
        else:
            flash('login to get access')
            redirect(url_for('appviews.login'))


@app_views.route('/allcohorts', strict_slashes=False, methods=['POST'])
def get_all_cohort():
    """
    get all courses
    """
    all_cohorts = storage.all('Cohort')
    cohort_list = []
    for value in all_cohorts.values():
        cohort_list.append(value.to_dict())
    return jsonify(cohort_list), 200

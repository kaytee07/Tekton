#!/usr/bin/python3
"""
all user apis including login and logout page
"""

from flask import abort, render_template, request, jsonify, session, redirect, url_for
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
            new_data = request.get_json()
            if not new_data:
                abort(404, description="absolutely no data")
            if 'no_of_students' not in new_data:
                abort(404, description="No no_of student")

            data = new_data.to_dict()
            new_cohort = Cohort(**data)
            new_cohort.save()
            return jsonify(new_cohort.to_dict())
    else:
        if 'user_id' in session:
            return render_template('cohort.html')
        else:
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

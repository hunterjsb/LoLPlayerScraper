from flask import Blueprint, render_template, request

views_blueprint = Blueprint('views_blueprint', __name__)

active_regions = []


@views_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if "LCS" in request.form:
        print('######### LCS #########')
    return render_template('wordle.html', active_regions=active_regions)


@views_blueprint.route('/about/')
def about():
    return render_template('about.html')


@views_blueprint.route('/api/')
def api():
    return render_template('api.html')

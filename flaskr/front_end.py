from flask import Blueprint, render_template

home_blueprint = Blueprint('home_blueprint', __name__)
about_blueprint = Blueprint('about_blueprint', __name__)


@home_blueprint.route('/')
def index():
    return render_template('index.html', debug_str='foobar')


@about_blueprint.route('/about/')
def about():
    return render_template('about.html')

from flask import Blueprint, render_template

views_blueprint = Blueprint('views_blueprint', __name__)


@views_blueprint.route('/')
def index():
    return render_template('index.html', debug_str='foobar')


@views_blueprint.route('/about/')
def about():
    return render_template('about.html')


@views_blueprint.route('/api/')
def api():
    return render_template('api.html')

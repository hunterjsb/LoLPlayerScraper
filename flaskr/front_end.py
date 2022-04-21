from flask import Blueprint, render_template

front_end_blueprint = Blueprint('front_end_blueprint', __name__)


@front_end_blueprint.route('/')
def index():

    # put epic front end stuff here idk
    return render_template('index.html')

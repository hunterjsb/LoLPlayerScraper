from flask import Blueprint

from flaskr.mdb import ApiDbUtil

api_blueprint = Blueprint('api_blueprint', __name__)
db = ApiDbUtil()


@api_blueprint.route('/api/get_player/<name>')
def get_player(name):
    return db.get_player(name)


@api_blueprint.route('/api/get_team/<name>')
def get_team(name):
    return db.get_team(name)

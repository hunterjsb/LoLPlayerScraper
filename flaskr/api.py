from flask import Blueprint

from flaskr.mdb import DBUtil

api_blueprint = Blueprint('api_blueprint', __name__)
db = DBUtil()


@api_blueprint.route('/api/get_player/<name>')
def get_player(name):
    return db.get_player(name)

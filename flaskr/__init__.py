from flask import Flask

from flaskr.api import api_blueprint
from flaskr.front_end import views_blueprint

app = Flask(__name__)
app.register_blueprint(api_blueprint)
app.register_blueprint(views_blueprint)

# don't define any routes here, create a new blueprint if needed

"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


# from flask import Flask, jsonify, request

# app = Flask(__name__)

# todos = [
#     { "label": "My first task", "done": False },
#     { "label": "My second task", "done": False }
# ]

# @app.route('/todos', methods=['GET'])
# def hello_world():
#     json_text = jsonify(todos)
#     return json_text

# @app.route('/todos', methods=['POST'])
# def add_new_todo():
#     request_body = request.data
#     todos.append(request.get_json(force=True))
#     print("Incoming request with the following body", request_body)
#     return jsonify(todos)

# @app.route('/todos/<int:position>', methods=['DELETE'])
# def delete_todo(position):
#     todos.pop(position)
#     print("This is the position to delete: ",position)
#     return jsonify(todos)

# # These two lines should always be at the end of your app.py file.
# if __name__ == '__main__':
#   app.run(host='0.0.0.0', port=3245, debug=True)
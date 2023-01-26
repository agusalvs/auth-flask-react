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
from models import db, User, People, Starships, Planets, Favorites
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


#ACÁ EMPIEZAN LAS RUTAS

# people = [
#     {"id": 1, "name": "Luke Skywalker", "birth_year": "19 BBY", "homeworld": "https://www.swapi.tech/api/planets/1/", "starships": "https://www.swapi.tech/api/starships/12/"},
#     {"id": 3, "name": "R2-D2", "birth_year": "33BBY", "homeworld": "https://www.swapi.tech/api/planets/8"}
# ]

# planets = [
#     {"id": 8, "name": "Naboo", "population": "4500000000", "gravity": "1 standard", "climate": "temperate"},
#     {"id": 5, "name": "Dagobah", "population": "unknown", "gravity": "N/A", "climate": "murky"}
# ]

# user = [
#     {"id": 1, "email": "uncorreo@gmail.com"},
#     {"id": 2, "email": "otrocorreo@gmail.com"}
# ]

# favorites = [
#     {"user_id": "2", "people_id": "3", "starships_id": "null", "planets_id": "null"},
#     {"user_id": "2", "people_id": "null", "starships_id": "null", "planets_id": "8"}
# ]

@app.route('/people', methods=['GET'])
def get_people():
    allpeople = People.query.all()
    results = list(map(lambda item: item.serialize(),allpeople))

    return jsonify(results), 200

# @app.route('/user/<int:user_id>', methods=['GET'])
# def get_info_user(user_id):
    
#     user = User.query.filter_by(id=user_id).first()
#     return jsonify(user.serialize()), 200
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):

    people = People.query.filter_by(id=people_id).first()
    return jsonify(people.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planets():

    allplanets = Planets.query.all()
    results = list(map(lambda item: item.serialize(),allplanets))

    return jsonify(results), 200


@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_planets_id(planets_id):

    planet = Planets.query.filter_by(id=planets_id).first()
    return jsonify(planet.serialize()), 200

@app.route('/user', methods=['GET'])
def get_user():

    allusers = User.query.all()
    results = list(map(lambda item: item.serialize(),allusers))

    return jsonify(results), 200

@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():

    planet = Planets.query.filter_by(id=planets_id).first()
    return jsonify(planet.serialize()), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def addfav():

    allfavorites = User.query.all()
    favorites.add(planet_id)
    results = list(map(lambda item: item.serialize(),allfavorites))
    print("Incoming request with the following body", allfavorites)

    return jsonify(results), 200

# @app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
# def add_new_fav_planet():

#     request_body = request.data
#     todos.append(request.get_json(force=True))
#     print("Incoming request with the following body", request_body)
#     return jsonify(todos)

# @app.route('/todos', methods=['POST'])
# def add_new_todo():
#     request_body = request.data
#     todos.append(request.get_json(force=True))
#     print("Incoming request with the following body", request_body)
#     return jsonify(todos)




#ACÁ TERMINAN LAS RUTAS


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
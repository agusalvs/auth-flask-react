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

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):

    favs = Favorites.query.filter_by(user_id=user_id).all()
    results = list(map(lambda item: item.serialize(),favs))

    return jsonify(results), 200


# [POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id

@app.route('/user/<int:user_id>/favorites/planets', methods=['POST'])
def add_planet_favorites(user_id):

    #me traigo el body
    request_body = request.json
    #veo lo que me trae
    print(request_body)
    #traigo lo que necesito y lo muestro en consola
    print(request_body['planets_id'])
    
    # #Class(propiedades a las que le agrego valores)
    #instanciar el obejto a partir de la clase
    new_fav_planet = Favorites(user_id = user_id, people_id = None, starships_id = None, planets_id = request_body['planets_id']) #lo que tengo dentro del print de la línea 118 lo llevo a mi variable

    favs = Favorites.query.filter_by(user_id=user_id, planets_id=request_body['planets_id']).first()
    print(favs)

    # si el usuario 1 tiene el planeta 1 le respondo que eso ya existe
    if favs is None:
        new_fav_planet = Favorites(user_id = user_id, people_id = None, starships_id = None, planets_id = request_body['planets_id']) #lo que tengo dentro del print de la línea 118 lo llevo a mi variable
        db.session.add(new_fav_planet)
        db.session.commit()

        return jsonify({new_fav_planet}), 200    

    return jsonify({'msg': 'el favorito ya existe'}), 400

# TERMINA EL POST DE PLANET

# EMPIEZA EL POST DE PEOPLE
@app.route('/user/<int:user_id>/favorites/people', methods=['POST'])
def add_people_favorites(user_id):

    #me traigo el body
    request_body = request.json
    #veo lo que me trae
    print(request_body)
    #traigo lo que necesito y lo verifico mostrándolo en consola
    print(request_body['people_id'])
    
    # #Class(propiedades a las que le agrego valores)
    #instanciar el obejto a partir de la clase
    new_fav_people = Favorites(user_id = user_id, people_id = request_body['people_id'], starships_id = None, planets_id = None) #lo que tengo dentro del print de la línea 118 lo llevo a mi variable

    favs = Favorites.query.filter_by(user_id=user_id, people_id=request_body['people_id']).first()
    print(favs)

    # si el usuario 1 tiene el planeta 1 le respondo que eso ya existe
    if favs is None:
        new_fav_people = Favorites(user_id = user_id, people_id = request_body['people_id'], starships_id = None, planets_id = None) #lo que tengo dentro del print de la línea 118 lo llevo a mi variable
        db.session.add(new_fav_people)
        db.session.commit()

        return jsonify({new_fav_people}), 200    

    return jsonify({'msg': 'el favorito ya existe'}), 400

# TERMINA EL POST DE PEOPLE


# #EMPIEZA EL DELETE DE PLANET

@app.route('/user/<int:user_id>/favorites/planets', methods=['DELETE'])
def delete_planet_favorites(user_id):

    #me traigo el body
    request_body = request.json
    #veo lo que me trae
    print(request_body)
    #traigo lo que necesito y lo verifico mostrándolo en consola
    print(request_body['planets_id'])
    
    # #Class(propiedades a las que le agrego valores)
    #instanciar el obejto a partir de la clase
    # delete_fav_planet = Favorites(user_id = user_id, people_id = None, starships_id = None, planets_id = request_body['planets_id']) #lo que tengo dentro del print de la línea 118 lo llevo a mi variable

    favs = Favorites.query.filter_by(user_id=user_id, planets_id=request_body['planets_id']).first()
    print(favs)

    # si el usuario 1 tiene el planeta 1 le respondo que eso ya existe
    if favs is not None:
        # delete_fav_planet = Favorites(user_id = user_id, people_id = None, starships_id = None, planets_id = request_body['planets_id']) #lo que tengo dentro del print de la línea 118 lo llevo a mi variable
        db.session.delete(favs)
        db.session.commit()

        # results = list(map(lambda item: item.serialize(),allplanets))

        return jsonify({'msg': 'eliminaste el favorito correctamente'}), 200    

    return jsonify({'msg': 'No existe el favorito a eliminar'}), 400

# #TERMINA EL DELETE DE PLANET

# #EMPIEZA EL DELETE DE PEOPLE

@app.route('/user/<int:user_id>/favorites/planets', methods=['DELETE'])
def delete_planet_favorites(user_id):

    #me traigo el body
    request_body = request.json
    #veo lo que me trae
    print(request_body)
    #traigo lo que necesito y lo verifico mostrándolo en consola
    print(request_body['planets_id'])
    
    # #Class(propiedades a las que le agrego valores)
    #instanciar el obejto a partir de la clase
    # delete_fav_planet = Favorites(user_id = user_id, people_id = None, starships_id = None, planets_id = request_body['planets_id']) #lo que tengo dentro del print de la línea 118 lo llevo a mi variable

    favs = Favorites.query.filter_by(user_id=user_id, planets_id=request_body['planets_id']).first()
    print(favs)

    # si el usuario 1 tiene el planeta 1 le respondo que eso ya existe
    if favs is not None:
        # delete_fav_planet = Favorites(user_id = user_id, people_id = None, starships_id = None, planets_id = request_body['planets_id']) #lo que tengo dentro del print de la línea 118 lo llevo a mi variable
        db.session.delete(favs)
        db.session.commit()

        # results = list(map(lambda item: item.serialize(),allplanets))

        return jsonify({'msg': 'eliminaste el favorito correctamente'}), 200    

    return jsonify({'msg': 'No existe el favorito a eliminar'}), 400

# #TERMINA EL DELETE DE PEOPLE



#ACÁ TERMINAN LAS RUTAS


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
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
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
#from models import Person

# "holi"

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

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#ACÁ EMPIEZAN LAS RUTAS

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


@app.route('/signup', methods=['POST'])
def reg_user():

    #me traigo el body
    request_body = request.json
    #veo lo que me trae
    print(request_body)
    
    users = User.query.filter_by(email=request_body['email']).first()

    # si el usuario no fue creado, lo crea; de lo contrario, envía el mensaje que ya fue creado
    if users is None:
        new_user = User(email = request_body['email'], password = request_body['password']) #lo que tengo dentro del print de la línea 118 lo llevo a mi variable
        db.session.add(new_user)
        db.session.commit()

        # print(new_user.serialize())

        return jsonify({'msg': 'el usuario con el email ' +request_body['email']+ ' ha sido creado exitosamente'}), 200    

    return jsonify({'msg': 'el usuario con el email ' +request_body['email']+ ' ya existe'})


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():

    email = request.json.get("email", None)
    password = request.json.get("password", None)

    users = User.query.filter_by(email=email).first()
    # print(users)

    if users is None:
        return jsonify({"msg": "You need to signup"}), 404
    if password != users.password:
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)
    # return jsonify({'msg': 'funciona'})


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/profile", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


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

@app.route('/user/<int:user_id>/favorites/people', methods=['DELETE'])
def delete_people_favorites(user_id):

    #me traigo el body
    request_body = request.json
    #veo lo que me trae
    print(request_body)
    #traigo lo que necesito y lo verifico mostrándolo en consola
    print(request_body['people_id'])
    
    # #Class(propiedades a las que le agrego valores)
    #instanciar el obejto a partir de la clase
    # delete_fav_planet = Favorites(user_id = user_id, people_id = None, starships_id = None, planets_id = request_body['planets_id']) #lo que tengo dentro del print de la línea 118 lo llevo a mi variable

    favs = Favorites.query.filter_by(user_id=user_id, people_id=request_body['people_id']).first()
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
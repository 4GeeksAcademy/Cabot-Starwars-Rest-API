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
from models import db, User, Planets, Characters , Favorites
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


#[GET] /characters Get a list of all the characters in the database. DONE
@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Characters.query.all()
    serialized_character = [character.serialize() for character in characters]
    return jsonify(serialized_character), 200


#[GET] /characters/<int:characters_id> Get one single person's information. DONE
@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_one_character(characters_id):
    character = Characters.query.filter_by(id=characters_id).first()
    return jsonify(character.serialize()), 200


#[GET] /planets Get a list of all the planets in the database. DONE
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    serialized_planets= [planet.serialize() for planet in planets]
    return jsonify(serialized_planets), 200


#[GET] /planets/<int:planet_id> Get one single planet's information. DONE
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planets= Planets.query.filter_by(id=planet_id).first()
    if planets is None:
        raise APIException("planet not found", status_code=404)
    return jsonify(planets.serialize()), 200

#[GET] /users Get a list of all the blog post users.
@app.route('/users', methods=['GET'])
def user_list():
    users = User.query.all()
    serialized_user = [user.serialize() for user in users]
    return jsonify(serialized_user),  200 #How Derek recommended

#GET SINGLE USER
@app.route('/users/<int:id>', methods= ['GET'])
def get_single_user(id):
    user_info = User.query.filter_by(id=id). first() 
    if id is None:
        raise APIException("User not found)", status_code=404)
    return jsonify(user_info.serialize()), 200 


#[GET] /users/<int:user_id>/favorites Get all the favorites that belong to the current user.
@app.route('/users/<int:user_id>/favorites', methods= ['GET'])
def all_user_favorites(user_id):
    user_info= User.query.filter_by(id= user_id).first()
    user_favorites = [favorite.serialize() for favorite in user_info.favorites]

    return jsonify(user_favorites), 200


#[POST] /favorite/planet/<int:planet_id> Add a new favorite planet to the current user with the planet id = planet_id.
@app.route('/favorite/<int:user_id>/planet/<int:planet_id>', methods = ['POST'])
def add_new_favorite_planet(user_id, planet_id):
    # user_info= User.query.filter_by(id= user_id).first()
    # planet_info= Planets.query.filter_by(id=planet_id).first()

    # new_favorite_user = user_info.favorites.append(planet_info)
    # db 

    user_favorite_planet= Favorites(planet_id=planet_id, user_id=user_id)

    db.session.add(user_favorite_planet)
    db.session.commit() #- stages the changes in your database

    return jsonify({"It worked": user_favorite_planet.serialize()}), 200


#[POST] /favorite/characters/<int:characters_id> Add new favorite characters to the current user with the characters id = characters_id.
@app.route('/favorite/<int:user_id>/characters/<int:character_id>', methods = ['POST'])
def add_new_favorite_character(user_id, character_id):

    user_favorite_character= Favorites(character_id=character_id, user_id=user_id)

    db.session.add(user_favorite_character)
    db.session.commit() #- stages the changes in your database

    return jsonify({"It workedx2": user_favorite_character.serialize()}), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)


#Create an API that connects to a database and implements the following endpoints (very similar to SWAPI.dev or SWAPI.tech):
#Additionally, create the following endpoints to allow your StarWars blog to have users and favorites:
#

#[DELETE] /favorite/planet/<int:planet_id> Delete a favorite planet with the id = planet_id.
#[DELETE] /favorite/characters/<int:characters_id> Delete a favorite characters with the id = characters_id.
#Your current API does not have an authentication system (yet), which is why the only way to create users is directly on the database using the Flask admin.
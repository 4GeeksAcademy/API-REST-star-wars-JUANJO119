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
from models import db, User, Character, Planet, Starship, FavoriteCharacter, FavoritePlanet, FavoriteStarship
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


#trae todos los usuarios
@app.route('/users', methods=['GET'])
def handle_hello():
    users = User.query.all()
    #print(users)
    #print(type(users[0]))
    users_serialized = []
    for user in users:
        users_serialized.append(user.serialize())
    response_body = {
        'user': users_serialized,
    }
    return jsonify(response_body), 200

#agrega nuevo usuario
@app.route('/user', methods=['POST'])
def add_user():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Envia informacion'}), 400
    if 'email' not in body:
        return jsonify({'msg': 'Campo email ogligatorio'}), 400
    if 'password' not in body:
        return jsonify({'msg': 'Campo password ogligatorio'}), 400
    new_user = User()
    new_user.email = body['email']
    new_user.password = body['password']
    new_user.is_active = True
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'msg': 'Usuario registrado', 'user': new_user.serialize()}), 200

#dime los personajes favoritos de usuarios segun id
@app.route('/user_favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    user = User.query.get(user_id)
    print(user)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
    registros_favoritos = user.favorites
    favorite_characters_serialized = []
    for registro in registros_favoritos:
        character = registro.character.serialize()
        favorite_characters_serialized.append(character)
    return jsonify({'msg': 'Todo salió bien', 'user': user.serialize() ,'favorite_characters': favorite_characters_serialized}), 200    






#trae todos los personajes
@app.route('/characters', methods=['GET'])
def all_characters():
    characters = Character.query.all()
    #print(characters)
    #print(type(characters[0]))
    characters_serialized = []
    for character in characters:
        characters_serialized.append(character.serialize())
    response_body = {
        'character': characters_serialized,
    }
    return jsonify(response_body), 200

#trae todos los planetas
@app.route('/planets', methods=['GET'])
def all_planets():
    planets = Planet.query.all()
    #print(planets)
    #print(type(planets[0]))
    planets_serialized = []
    for planet in planets:
        planets_serialized.append(planet.serialize())
    response_body = {
        'planet': planets_serialized,
    }
    return jsonify(response_body), 200

#trae todos los naves
@app.route('/starships', methods=['GET'])
def all_starships():
    starships = Starship.query.all()
    #print(starships)
    #print(type(starships[0]))
    starships_serialized = []
    for starship in starships:
        starships_serialized.append(starship.serialize())
    response_body = {
        'starship': starships_serialized,
    }
    return jsonify(response_body), 200


#agrega nuevo personaje
@app.route('/character', methods=['POST'])
def add_character():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Envia informacion'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'Campo name ogligatorio'}), 400
    if 'height' not in body:
        return jsonify({'msg': 'Campo height ogligatorio'}), 400
    if 'weigth' not in body:
        return jsonify({'msg': 'Campo weigth ogligatorio'}), 400
    new_character = Character()
    new_character.name = body['name']
    new_character.height = body['height']
    new_character.weigth = body['weigth']
    db.session.add(new_character)
    db.session.commit()
    return jsonify({'msg': 'Personaje registrado', 'character': new_character.serialize()}), 200

#agrega nuevo planeta
@app.route('/planet', methods=['POST'])
def add_planet():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Envia informacion'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'Campo name ogligatorio'}), 400
    if 'population' not in body:
        return jsonify({'msg': 'Campo population ogligatorio'}), 400
    if 'climate' not in body:
        return jsonify({'msg': 'Campo climate ogligatorio'}), 400
    new_planet = Planet()
    new_planet.name = body['name']
    new_planet.population = body['population']
    new_planet.climate = body['climate']
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({'msg': 'Planeta registrado', 'planet': new_planet.serialize()}), 200

#agrega nueva nave
@app.route('/starship', methods=['POST'])
def add_starship():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'Envia informacion'}), 400
    if 'name' not in body:
        return jsonify({'msg': 'Campo name ogligatorio'}), 400
    if 'model' not in body:
        return jsonify({'msg': 'Campo model ogligatorio'}), 400
    if 'manufacturer' not in body:
        return jsonify({'msg': 'Campo manufacturer ogligatorio'}), 400
    new_starship = Starship()
    new_starship.name = body['name']
    new_starship.model = body['model']
    new_starship.manufacturer = body['manufacturer']
    db.session.add(new_starship)
    db.session.commit()
    return jsonify({'msg': 'Nave registrada', 'starship': new_starship.serialize()}), 200









# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

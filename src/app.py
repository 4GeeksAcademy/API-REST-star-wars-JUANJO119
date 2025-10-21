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



#dime los favoritos de usuarios segun id
@app.route('/user_favorites/<int:user_id>', methods=['GET'])
def get_favorites(user_id):
    user = User.query.get(user_id)
    #print(user)
    if user is None:
        return jsonify({'msg': f'El usuario con id {user_id} no existe'}), 404
    
    registros_favoritos = user.favorites
    
    favorite_characters_serialized = []
    favorite_planets_serialized = []
    favorite_starships_serialized = [] 

    for registro in registros_favoritos:
        if registro.character:
            character = registro.character.serialize()
            favorite_characters_serialized.append(character)
        
        if registro.planet:
            planet = registro.planet.serialize()
            favorite_planets_serialized.append(planet)
            
        if registro.starship:
            starship = registro.starship.serialize()
            favorite_starships_serialized.append(starship) 

    return jsonify({
        'msg': 'Todo salió bien', 
        'user': user.serialize(), 
        'favorite_characters': favorite_characters_serialized,
        'favorite_planets': favorite_planets_serialized,
        'favorite_starships': favorite_starships_serialized
    }), 200   


# Añadir personaje favorito
@app.route('/user/<int:user_id>/favorite/character/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if user is None or character is None:
        return jsonify({'msg': 'Usuario o personaje no encontrado'}), 404

    existing_fav = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=character_id).first()
    if existing_fav:
        return jsonify({'msg': 'El personaje ya está en favoritos'}), 400

    favorite = FavoriteCharacter(user_id=user_id, character_id=character_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'msg': 'Personaje agregado a favoritos'}), 200


# Eliminar personaje favorito
@app.route('/user/<int:user_id>/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_favorite_character(user_id, character_id):
    favorite = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=character_id).first()
    if favorite is None:
        return jsonify({'msg': 'El personaje no está en favoritos'}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': 'Personaje eliminado de favoritos'}), 200


# Añadir planeta favorito
@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if user is None or planet is None:
        return jsonify({'msg': 'Usuario o planeta no encontrado'}), 404

    existing_fav = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_fav:
        return jsonify({'msg': 'El planeta ya está en favoritos'}), 400

    favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'msg': 'Planeta agregado a favoritos'}), 200


# Eliminar planeta favorito
@app.route('/user/<int:user_id>/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(user_id, planet_id):
    favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({'msg': 'El planeta no está en favoritos'}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': 'Planeta eliminado de favoritos'}), 200


# Añadir nave favorita
@app.route('/user/<int:user_id>/favorite/starship/<int:starship_id>', methods=['POST'])
def add_favorite_starship(user_id, starship_id):
    user = User.query.get(user_id)
    starship = Starship.query.get(starship_id)

    if user is None or starship is None:
        return jsonify({'msg': 'Usuario o nave no encontrado'}), 404

    existing_fav = FavoriteStarship.query.filter_by(user_id=user_id, starship_id=starship_id).first()
    if existing_fav:
        return jsonify({'msg': 'La nave ya está en favoritos'}), 400

    favorite = FavoriteStarship(user_id=user_id, starship_id=starship_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'msg': 'Nave agregada a favoritos'}), 200


# Eliminar nave favorita
@app.route('/user/<int:user_id>/favorite/starship/<int:starship_id>', methods=['DELETE'])
def delete_favorite_starship(user_id, starship_id):
    favorite = FavoriteStarship.query.filter_by(user_id=user_id, starship_id=starship_id).first()
    if favorite is None:
        return jsonify({'msg': 'La nave no está en favoritos'}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({'msg': 'Nave eliminada de favoritos'}), 200






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

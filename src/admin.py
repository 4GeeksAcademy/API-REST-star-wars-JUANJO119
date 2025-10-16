import os
from flask_admin import Admin
from models import db, User, Character, FavoriteCharacter, Planet, FavoritePlanet, Starship, FavoriteStarship
from flask_admin.contrib.sqla import ModelView

#Users
class UsersModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'email', 'password', 'is_active', 'favorites']

#Character
class CharacterModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'height', 'weigth', 'favorite_by']
class FavoriteCharacterModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'character_id', 'user', 'character']

#Planet
class PlanetModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'population', 'climate', 'favorite_by']
class FavoritePlanetModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'planet_id', 'user', 'planet']

#Starship
class StarshipModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'name', 'model', 'manufacturer', 'favorite_by']
class FavoriteStarshipModelView(ModelView):
    column_auto_select_related = True
    column_list = ['id', 'user_id', 'starship_id', 'user', 'starship']


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UsersModelView(User, db.session))
    
    admin.add_view(CharacterModelView(Character, db.session))
    admin.add_view(FavoriteCharacterModelView(FavoriteCharacter, db.session))
    
    admin.add_view(PlanetModelView(Planet, db.session))
    admin.add_view(FavoritePlanetModelView(FavoritePlanet, db.session))
    
    admin.add_view(StarshipModelView(Starship, db.session))
    admin.add_view(FavoriteStarshipModelView(FavoriteStarship, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
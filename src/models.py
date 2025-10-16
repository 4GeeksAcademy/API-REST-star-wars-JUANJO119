from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

#User
class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    
    favorites: Mapped[list['FavoriteCharacter']] = relationship(back_populates='user')
    favorites_planets: Mapped[list['FavoritePlanet']] = relationship(back_populates='user')
    favorites_starships: Mapped[list['FavoriteStarship']] = relationship(back_populates='user')

    def __repr__(self):
            return f'Usuario {self.email}'
    
    def serialize(self):
        return{
             'id': self.id,
             'email': self.email,
             'is_active': self.is_active
        }


#Character
class Character(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    height: Mapped[int] = mapped_column(Integer)
    weigth: Mapped[int] = mapped_column(Integer)
    favorite_by: Mapped[list['FavoriteCharacter']] = relationship(back_populates='character')

    def __repr__(self):
            return f'Personaje {self.name}'
    
    

class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'))
    user: Mapped['User'] = relationship(back_populates='favorites')
    character: Mapped['Character'] = relationship(back_populates='favorite_by')

    def __repr__(self):
            return f'Al usuario {self.user_id} le gusta personaje{self.character_id}'

#Planet
class Planet(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    population: Mapped[int] = mapped_column(Integer)
    climate: Mapped[str] = mapped_column(String(120))
    favorite_by: Mapped[list['FavoritePlanet']] = relationship(back_populates='planet')

class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'))
    user: Mapped['User'] = relationship(back_populates='favorites_planets')
    planet: Mapped['Planet'] = relationship(back_populates='favorite_by')

#Starship
class Starship(db.Model):
    __tablename__ = 'starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(120))
    manufacturer: Mapped[str] = mapped_column(String(120))
    favorite_by: Mapped[list['FavoriteStarship']] = relationship(back_populates='starship')

class FavoriteStarship(db.Model):
    __tablename__ = 'favorite_starships'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    starship_id: Mapped[int] = mapped_column(ForeignKey('starships.id'))
    user: Mapped['User'] = relationship(back_populates='favorites_starships')
    starship: Mapped['Starship'] = relationship(back_populates='favorite_by')
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    favorites = db.relationship("Favorites", back_populates='user')
    is_active = db.Column(db.Boolean(), nullable=False)
    user_name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__ (self):
        return "<User %r>" %self.user_name #defining a representation method for debugging by returning the user's username

    def serialize(self): #serializes user data
        #return '<User %r>' % self.email
        return {
            'id': self.id,
            'email': self.email,
            'username': self.user_name,#do not serialize password, it's a breach
            'favorites': [favorite.serialize() for favorite in self.favorites],
        }

class Planets(db.Model):
    __tablename__ = 'Planets'
    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.String(250), nullable=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    climate = db.Column(db.String(250), nullable=True)
    population = db.Column(db.String(250), nullable=True)
    terrain = db.Column(db.String(250), nullable=True)
    favorites = db.relationship("Favorites", back_populates='planet')

    def __repr__ (self):
        return "<Planets %r>" %self.name #defining a representation method for debugging by returning the user's username
    
    def serialize(self): #serializes user data
        return {
            'id': self.id,
            'name': self.name,
            'population': self.population,
            'climate': self.climate,
            'terrain': self.terrain,
            'diameter': self.diameter,
        }
    

class Characters(db.Model):
    __tablename__ = 'Characters'
    # Here we define db.columns for the table address.
    # Notice that each db.column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    hair_color = db.Column(db.String(250), nullable=True)
    eye_color = db.Column(db.String(250), nullable=True)
    name = db.Column(db.String(250), nullable=True)
    height = db.Column(db.String(250), nullable=True)
    gender = db.Column(db.String(250), nullable=True)
    favorites = db.relationship("Favorites", back_populates='character')
    

    def __repr__ (self):
        return "<Planets %r>" %self.name #defining a representation method for debugging by returning the planet name


    def serialize(self): #serializes user data
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'hair_color': self.hair_color,
            'eye_color': self.eye_color,
            'gender': self.gender
        }
    

class Favorites(db.Model):
    __tablename__ = 'Favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('Characters.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('Planets.id'), nullable=True)
    planet = db.relationship('Planets', back_populates='favorites')
    character = db.relationship('Characters', back_populates='favorites')
    user = db.relationship('User', back_populates='favorites')
    name= db.Column(db.String(250))

    def to_dict(self):
        return {}   

    def __repr__ (self):
        return "<User %r>" %self.user + "<character %r>" %self.character + "<planet %r>" %self.planet

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "user_id": self.user_id,
            "planet":self.planet.serialize() if self.planet else None,
            "characters":self.character.serialize() if self.character else None,

            # do not serialize the password, its a security breach
        }
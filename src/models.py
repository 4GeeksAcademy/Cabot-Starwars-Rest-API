from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorites = db.relationship("Favorites", back_populates='user')
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email
    
class Planets(db.Model):
    __tablename__ = 'Planets'
    id = db.Column(db.Integer, primary_key=True)
    diameter = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    climate = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    favorites = db.relationship("Favorites", back_populates='planets')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'population': self.population,
            'climate': self.climate,
            'terrain': self.terrain,
        }
    

class Characters(db.Model):
    __tablename__ = 'Characters'
    # Here we define db.columns for the table address.
    # Notice that each db.column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    hair_color = db.Column(db.String(250), nullable=False)
    eye_color = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    height = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(250), nullable=False)
    favorites = db.relationship("Favorites", back_populates='characters')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'height': self.height,
            'hair_color': self.hair_color,
            'eye_color': self.eye_color,
            'gender': self.gender,
        }
    

class Favorites(db.Model):
    __tablename__ = 'Favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('Characters.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('Planets.id'), nullable=True)
    planets = db.relationship('Planets', back_populates='favorites')
    characters = db.relationship('Characters', back_populates='favorites')
    user = db.relationship('User', back_populates='favorites')

    def to_dict(self):
        return {}    

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
from sqlalchemy import Column, Integer, Float, String
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash

from application import app
from application import login


# DB setup
db = SQLAlchemy(app=app)
ma = Marshmallow(app=app)


# Star model
class Star(db.Model):
    __tablename__ = 'STARS'

    star_id = Column(Integer, primary_key=True)
    star_name = Column(String, unique=True)
    location = Column(Float)
    mass = Column(Float)        # kg
    diameter = Column(Float)    # km
    abs_magnitude = Column(String)


# Planet model
class Planet(db.Model):
    __tablename__ = 'PLANETS'

    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String, unique=True)
    home_star = Column(String)
    no_of_moons = Column(Integer)
    mass = Column(Float)            # kg
    diameter = Column(Float)        # km
    distance = Column(Float)        # km
    orbital_period = Column(Float)  # days


# User model
class User(UserMixin, db.Model):
    __tablename__ = 'USERS'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    user_name = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login.user_loader
def load_user(id_num):
    return User.query.get(int(id_num))


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'user_name', 'email', 'password')


class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'home_star', 'no_of_moons', 'mass', 'diameter', 'distance', 'orbital_period')


class StarSchema(ma.Schema):
    class Meta:
        fields = ('star_id', 'star_name', 'location', 'mass', 'diameter', 'abs_magnitude')



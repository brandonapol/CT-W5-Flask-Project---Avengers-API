# imports 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
import secrets
from icecream import ic

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Creating a database for users
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    #We never take first or last name!!!
    first_name = db.Column(db.String(150), nullable=True, default='')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    # takes email from the signup.html page via flask forms
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True )
    character = db.relationship('Hero', backref = 'owner', lazy = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, email, first_name='', last_name='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex()

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'


class Hero(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    comics_appeared_in = db.Column(db.String(200), nullable = True)
    super_power = db.Column(db.String(100), nullable = True)
    date_created = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self,name,description,comics_appeared_in,super_power,date_created,user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.comics_appeared_in = comics_appeared_in
        self.super_power = super_power
        self.date_created = date_created
        self.user_token = user_token


    def __repr__(self):
        return f'The following vehicle has been added to the collection: {self.name}'

    def set_id(self):
        return (secrets.token_urlsafe())

# Creation of API Schema via the Marshmallow object 
class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name','description', 'comics_appeared_in', 'super_power', 'date_created']

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)
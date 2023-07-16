from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return (self.user_id)

class Pokemon(db.Model):
    pokemon_id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    ability = db.Column(db.String, nullable=False)
    hp = db.Column(db.String, nullable=False)
    attack = db.Column(db.String, nullable=False)
    defense = db.Column(db.String, nullable=False)
    sprite = db.Column(db.String, nullable=False)
    date_discovered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, name, ability, hp, attack, defense, sprite):
        self.name = name
        self.ability = ability
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.sprite = sprite

class Caught_Pokemon(db.Model):
    catch_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.pokemon_id'))
    date_caught = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, user_id, pokemon_id):
        self.user_id = user_id
        self.pokemon_id = pokemon_id


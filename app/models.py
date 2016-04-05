from . import db
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from datetime import datetime, timedelta

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	date_of_birth = db.Column(db.DateTime())
	gender = db.Column(Enum('m', 'f'))
	email = db.Column(db.String(80))
	password = db.Column(db.String)

	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

class Meal(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	category = db.Column(Enum('breakfast', 'lunch', 'dinner', 'other'))
	calories = db.Column(db.Float)
	image = db.Column(db.String(100))
	serving_size = db.Column(db.Float)

	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

class Recipe(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	rating = db.Column(db.Flao)
	preparation_time = db.Column(db.Float)

	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

class Ingredient(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	quantity = db.Column(db.Float)
	note = db.Column(db.String(1000))

	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

class Instruction(db.Model):
	id = db.Column(db.Integer, primary_key=True)	
	number = db.Column(db.Integer)
	value = db.Column(db.String(1000))

	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

class MealPlan(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

class Inventory(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

class SupermarketList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

from . import db
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum
from datetime import datetime, timedelta

class User(db.Model):
	userid = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(80))
	last_name = db.Column(db.String(80))
	gender = db.Column(Enum('m', 'f'))
	email = db.Column(db.String(80))
	password = db.Column(db.String)
	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

	def __init__(self,userid,first_name,last_name,gender,email,password,updated_at,created_at):
		self.userid = userid
		self.first_name = first_name
		self.last_name = last_name
		self.gender = gender
		self.email = email
		self.password = password
		self.updated_at = updated_at
		self.created_at = created_at

class Meal(db.Model):
	mid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	category = db.Column(Enum('breakfast', 'lunch', 'dinner', 'other'))
	calories = db.Column(db.Float)
	image = db.Column(db.String(100))
	serving_size = db.Column(db.Float)

	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

	def __init__(self,mid,name,category,calories,image,serving_size,updated_at,created_at):
		self.mid = mid
		self.name = name
		self.category = category
		self.calories = calories
		self.image = image
		self.serving_size = serving_size
		self.updated_at = updated_at
		self.created_at = created_at

class Recipe(db.Model):
	rid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	rating = db.Column(db.Flao)
	preparation_time = db.Column(db.Float)
	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

	def __init__(self,rid,name,rating,preparation_time,updated_at,created_at):
		self.rid = rid
		self.name = name
		self.rating = rating
		self.preparation_time = preparation_time
		self.updated_at = updated_at
		self.created_at = created_at

class Ingredient(db.Model):
	Ingred_id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	quantity = db.Column(db.Float)
	note = db.Column(db.String(1000))
	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

	def __init__(self,Ingred_id,name,quantity,note,updated_at,created_at):
		self.Ingred_id = Ingred_id
		self.name = name
		self.quantity = quantity
		self.note = note
		self.updated_at = updated_at
		self.created_at = created_at

class Instruction(db.Model):
	Instruc_id = db.Column(db.Integer, primary_key=True)	
	number = db.Column(db.Integer)
	value = db.Column(db.String(1000))
	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

	def __init__(self,Instruc_id,number,value,updated_at,created_at):
		self.Instruc_id = Instruc_id
		self.number = number
		self.value = value
		self.updated_at = updated_at
		self.created_at = created_at

class MealPlan(db.Model):
	mpid = db.Column(db.Integer, primary_key=True)
	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

	def __init__(self,mpid,updated_at,created_at):
		self.mpid = mpid
		self.updated_at = updated_at
		self.created_at = created_at

class Inventory(db.Model):
	Inid = db.Column(db.Integer, primary_key=True)
	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

	def __init__(self,Inid,updated_at,created_at):
		self.Inid = Inid
		self.updated_at = updated_at
		self.created_at = created_at


class SupermarketList(db.Model):
	sid = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))
	updated_at =db.Column(db.DateTime, server_default=datetime.utcnow(), onupdate=datetime.utcnow())
	created_at = db.Column(db.DateTime, server_default=datetime.utcnow())

	def __init__(self,sid,name,updated_at,created_at):
		self.sid = sid
		self.name = name
		self.updated_at = updated_at
		self.created_at = created_at
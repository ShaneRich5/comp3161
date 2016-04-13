import MySQLdb as mdb 
import sys
from faker import Factory
import random

def all_users():
	cur, conn = initialize_connection()

	cur.execute('SELECT * FROM user');
	results = cur.fetchall()

	print results

	cleanup_connection(conn)

def all_ingredients():
	cur, conn = initialize_connection()

	cur.execute('SELECT * FROM ingredient');
	results = cur.fetchall()

	print results

	cleanup_connection(conn)

def all_recipe():
	cur, conn = initialize_connection()

	cur.execute('SELECT * FROM recipe');
	results = cur.fetchall()

	print results

	cleanup_connection(conn)

def show_user(email):
	cur, conn = initialize_connection()
	cur.execute("SELECT * FROM user WHERE email = '{}'".format(email))
	cleanup_connection(conn)

def show_recipe(id):
	cur, conn = initialize_connection()
	cur.execute("SELECT * FROM recipe WHERE recipe_id = '{}'".format(id))
	cleanup_connection(conn)

def show_ingredient(id):
	cur, conn = initialize_connection()
	cur.execute("SELECT * FROM ingredient WHERE ingredient_id = '{}'".format(id))
	cleanup_connection(conn)

def save_user(user):
	cursor, connection = initialize_connection()

	first_name = user['first_name']
	last_name = user['last_name']
	email = user['email']
	password = user['password']
	dob = user['dob']
	gender = user['gender']

	cur.execute("""
		INSERT INTO 
		user(first_name, last_name, email, password, dob, gender) 
		values("{}", "{}", "{}", "{}", "{}", "{}");
		""".format(first_name, last_name, email, password, dob, gender))

	cleanup_connection(connection)

def save_ingredient(ingredient):
	cursor, connection = initialize_connection()

	name = ingredient['name']
	quantity = ingredient['quantity']
	units = ingredient['units']
	description = ingredient['description']

	cur.execute("""
		INSERT INTO 
		ingredient(name, quantity, units, description) 
		values("{}", {}, "{}", "{}");
		""".format(name, quantity, units, description))

	cleanup_connection(connection)

def save_recipe(recipe):
	cursor, connection = initialize_connection()

	name = recipe['name']
	rating = recipe['rating']
	preparation_time = recipe['preparation_time']
	
	cur.execute("""
		INSERT INTO
		recipe(name, rating, preparation_time)
		values("{}", {}, {});
		""".format(name, rating, preparation_time))

	cleanup_connection(connection)

def initialize_connection():
	try:
		con = mdb.connect('localhost', 'root', 'root')
		cursor = con.cursor()
	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		return cursor, con

def cleanup_connection(conn):
	if conn:
		conn.close()
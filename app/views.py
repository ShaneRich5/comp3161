from app import app
from flask import render_template, request, flash, session
from helpers import *
from werkzeug.datastructures import MultiDict

import MySQLdb as mdb 
import sys
import random


import datetime

# ====================================
#				Basic Pages
# ====================================
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about', methods=['GET'])
def about():
	return render_template('about.html')

@app.route('/register', methods=['GET'])
def register():	
	return render_template('register.html')

@app.route('/login', methods=['GET'])
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('email', None)
	return render_template('home')

# ====================================
#				Post Request
# ====================================
@app.route('/register', methods=['POST'])
def save_user():
	h.save_user(request.form)
	session['email'] = request.form['email']
	return render_template('home.html')

@app.route('/login', methods=['POST'])
def authenticate():
	authenticate(request.form)
	session['email'] = request.form['email']
	return render_template('home.html')

@app.route('/recipes', methods=['POST'])
def recipe_save():
	email = session['email']
	save_recipe(request.form, email)
	return render_template('recipe_all.html')

@app.route('/ingredients', methods=['POST'])
def ingredient_save():
	save_ingredient(request.form)
	return render_template('ingredients_all.html')

# ====================================
#				Query Pages
# ====================================
@app.route('/users', methods=['GET'])
def user_all():
	users = all_users()
	return render_template('users_all', users=users)

@app.route('/users/<user_id>', methods=['GET'])
def user_show_by_id(user_id):
	users = show_user(user_id)
	return render_template('users_all')

@app.route('/ingredients', methods=['GET'])
def ingredients_all():
	ingredients = all_ingredients()
	return render_template('ingredients_all')

@app.route('/ingredients/<ingredient_id>', methods=['GET'])
def ingredient_show_by_id(ingredient_id):
	ingredient = show_ingredient(ingredient_id)
	return render_template('ingredient_show')

@app.route('/recipes', methods=['GET'])
def recipes_all():
	email = request.args.get('user') # this should be an email address
	recipes = all_recipes(email=email)
	return render_template('recipes_all')

@app.route('/recipes/<recipe_name>', methods=['GET'])
def recipe_show_by_name(recipe_name):
	recipe = show_recipe(recipe_name)
	return render_template('recipe_show')

# ====================================
#				Search Page
# ====================================
@app.route('/search')
def search():
	return 'Search'

# ====================================
#				Error Pages
# ====================================
@app.errorhandler(404)
def page_not_found(error):
	return 'This page does not exist', 404

# @app.route('/Register',methods=['GET,POST'])
# def register():
#     form = SignUpForm(csrf_enabled=False)
#     if request.method == 'POST':
#         if form.validate()==False:
#             flash('All fields are required.')
#             return render_template('register.html',form=form)
#         else:
#             cur = mysql.connection.cursor()
#             cur.execute("SELECT * FROM members WHERE firstname='"+form.firstname.data + "' and lastname='"+form.lastname.data+"'and gender='"+form.gender.data +"' and email='" +form.email.data+"'")
#             data = cur.fetchone()
#             if data == None:
#                 query = "INSERT INTO user (first_name,last_name,gender,email,password,recipeId,updated_at,created_at) VALUES(form.firstname.data,form.lastname.data,form.gender.data,form.email.data,form.password.data,"","",datetime.now())"
#                 cur.execute(query)
#                 return "Registered"
#             return "User already Registered"

# =============================
# DB Helper methods
# =============================
def all_users():
	cur, conn = initialize_connection()
	cur.execute('SELECT * FROM user');
	results = cur.fetchall()
	print results
	cleanup_connection(conn)
	return results

def all_ingredients():
	cur, conn = initialize_connection()
	cur.execute('SELECT * FROM ingredient');
	results = cur.fetchall()
	print results
	cleanup_connection(conn)
	return results

def all_recipe(email=None):
	cur, conn = initialize_connection()
	query = 'SELECT * FROM recipe r'
	
	if email:
		query += ' WHERE r.email={}'.format(email)
	
	cur.execute(query);

	results = cur.fetchall()
	print results 
	cleanup_connection(conn)
	return results

def show_user(email):
	cur, conn = initialize_connection()
	cur.execute("SELECT * FROM user WHERE email = '{}'".format(email))
	result = cur.fetchone()
	cleanup_connection(conn)
	return result

def show_recipe(id):
	cur, conn = initialize_connection()
	cur.execute("SELECT * FROM recipe WHERE recipe_id = '{}'".format(id))
	result = cur.fetchone()
	cleanup_connection(conn)
	return result

def show_ingredient(id):
	cur, conn = initialize_connection()
	cur.execute("SELECT * FROM ingredient WHERE ingredient_id = '{}'".format(id))
	result = cur.fetchone()
	cleanup_connection(conn)
	return result

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

	cur.execute("""
		SELECT * FROM user u WHERE u.email={}
		""".format(email))

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

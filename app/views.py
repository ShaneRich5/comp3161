from app import app
from flask import render_template, request,flash
import helpers
from werkzeug.datastructures import MultiDict

import datetime

# ====================================
#				Basic Pages
# ====================================
@app.route('/')
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

# ====================================
#				Form Pages
# ====================================
@app.route('/register', methods=['POST'])
def save_user():
	helpers.save_user(request.form)

@app.route('/login', methods=['POST'])
def authenticate():
	helpers.authenticate(request.form)
	return render_template('home.html')

# ====================================
#				Query Pages
# ====================================
@app.route('/users', methods=['GET'])
def user_all():
	users = helpers.retrieve_all_users()
	return render_template('users_all')

@app.route('/users/<user_id>', methods=['GET'])
def user_show_by_id(user_id):
	users = helpers.retrieve_all_users()
	return render_template('users_all')

@app.route('/ingredients', methods=['GET'])
def ingredients_all():
	ingredients = helpers.retrieve_all_ingredients()
	return render_template('ingredients_all')

@app.route('/ingredients/<ingredient_id>', methods=['GET'])
def ingredient_show_by_id(ingredient_id):
	ingredients = helpers.retrieve_all_ingredients()
	return render_template('ingredient_show')

@app.route('/recipes', methods=['GET'])
def recipes_all():
	recipes = helpers.retrieve_all_recipes()
	return render_template('recipes_all')

@app.route('/recipes/<recipe_name>', methods=['GET'])
def recipe_show_by_name(recipe_name):
	recipe = helpers.retrieve_all_recipe()
	return render_template('recipe_show')

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


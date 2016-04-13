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

@app.route("/generateMealPlan/",methods=["POST","GET"])
def mealplan():
    c, conn = connection() 
    c.execute("INSERT INTO mealplan (countMeal) VALUES (35)")
    a = str(c.lastrowid)
    c.execute("SELECT meal_id FROM meal WHERE type = 'B' ORDER BY RAND() LIMIT 7 ")
    breakfasts = c.fetchall()
    c.execute("SELECT meal_id FROM meal WHERE type = 'L' ORDER BY RAND() LIMIT 7 ")
    lunch = c.fetchall()
    c.execute("SELECT meal_id FROM meal WHERE type = 'D' ORDER BY RAND() LIMIT 7 ")
    dinner = c.fetchall()
    c.execute("SELECT meal_id FROM meal WHERE type = 'S' ORDER BY RAND() LIMIT 14 ")
    snacks = c.fetchall()
    i = 0
    u= 0
    y=0
    t=0
    while i <= (len(snacks))-1:
        snack = str(snacks[i][0])
        
        #c.execute("INSERT INTO generates(mealplan_id,meal_id) VALUES (%d,%s)", 1,snacks[i][0])
        c.execute("INSERT INTO generates (meal_id,mealplan_id) VALUES (%s, %s)",(int(snack),a))
        i += 1
    while u <= (len(dinner))-1:
        dinner = str(dinner[u][0])
        c.execute("INSERT INTO generates (meal_id,mealplan_id) VALUES (%s, %s)",(int(dinner),a))
        u+=1
    while y <= (len(lunch))-1:
        lunch = str(lunch[y][0])
        c.execute("INSERT INTO generates (meal_id,mealplan_id) VALUES (%s, %s)",(int(lunch),a))
        y+=1
    while t <= (len(breakfasts))-1:
        breakfast = str(breakfasts[t][0])
        c.execute("INSERT INTO generates (meal_id,mealplan_id) VALUES (%s, %s)",(int(breakfast),a))
        t+=1
    return "str(breakfast[t][0])"

# keniel
@app.route('/contact/',methods=['GET','POST'])
def contact():
    form = ContactForm(csrf_enabled=False)
    if request.method=='POST':
         if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html',form=form)

         else:
            fromname = form.name.data
            fromaddr = form.Email.data
            subject = form.Subject.data
            msg = form.Message.data
            sendemail(fromaddr,fromname,subject,msg)

            return 'Form posted.'
    elif request.method=='GET':
         return render_template('contact.html', form=form)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

    return wrap

@app.route('/shoppinglist/')
def shoppinglist():
    """Render the website's shoppinglist page."""
    return render_template('index-1.html')


@app.route('/email/')
def email():
    """Render the website's email page."""
    return render_template('emailForm.html')

@app.route('/login/',methods=["GET","POST"])
def login():
    """Render the website's login page."""
    try:
        form = LoginForm(csrf_enabled=False)
        if request.method == "POST":
            if form.validate()==False:
                flash('All fields are required.')
                return render_template('login.html',form=form)
            else:
                c, conn = connection()
                data = c.execute("SELECT * FROM user WHERE email = '"+thwart(form.Email.data)+"'")

                data = c.fetchone()[2]
                user_id = c.fetchone()[0]
            
                if bcrypt.check_password_hash(data,form.password.data):
                    session['logged_in'] = True
                    session['email'] = form.Email.data
                    session['user_id'] = str(user_id)

                    flash("You are now logged in")
                    return render_template("home.html")

                else:
                    error = "Invalid credentials, try again."
                    return render_template("login.html",  form=form ,error = error)

            gc.collect()

        elif request.method=='GET':
            return render_template('login.html', form=form)

    except Exception as e:
        #flash(e)
        error = "Invalid credentials, try again."
        return render_template("login.html",  form=form ,error = error)  
        

@app.route('/register/', methods=["GET","POST"])
def register():
    try:
        form = RegistrationForm(csrf_enabled=False)
        if request.method == "POST":
            if form.validate() == False:
                flash('All fields are required.')
                return render_template('register.html',form=form)
            else:
                firstname = form.firstname.data
                lastname = form.lastname.data
                gender = form.gender.data
                email = form.email.data
                password = bcrypt.generate_password_hash((str(form.password.data)))

                c, conn = connection()
                x = c.execute("SELECT * FROM user WHERE email = '"+thwart(email)+"'")


                if int(x) > 0:
                    flash("That email is already taken, please choose another")
                    return render_template('register.html', form=form)

                else:
                    c.execute("INSERT INTO user (email, password,first_name ,last_name, gender) VALUES (%s, %s, %s, %s,%s)",
                             (thwart(email),thwart(password), thwart(firstname), thwart(lastname), thwart(gender)))
                    
                    conn.commit()
                    flash("Thanks for registering!")
                    c.execute("SELECT user_id FROM user WHERE email = '"+thwart(email)+"'")
                    data = c.fetchone()[0]
                    c.close()
                    conn.close()
                    gc.collect()

                    session['logged_in'] = True
                    session['user'] = email
                    session['user_id'] =  str(data)
                    return render_template("home.html")

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))
    
@app.route('/search/',methods=["POST","GET"])
def search():
    if request.method == "POST":
        c,conn = connection()
        c.execute("SELECT * FROM recipe WHERE name LIKE '"+ request.form['search']+"%'")
        return render_template("results.html", records=c.fetchall())
    return render_template("search.html")


###
# The functions below should be applicable to all Flask apps.
###
@app.route('/recipe/<recipeId>',methods=["POST","GET"])
def recipe(recipeId):
    if request.method == "GET":
        lst = []
        c,conn = connection()
        c.execute("SELECT name,rating,preparation_time FROM recipe WHERE recipe_id = '"+ recipeId +"'")
        data = c.fetchall()
        recipe_name = str(data[0][0])
        recipe_rating = str(data[0][1])
        recipe_preparation_time = str(data[0][2])
        c.execute("SELECT name, type, calories,image,serving_size FROM meal WHERE recipe_id = '"+ recipeId +"'")
        data = c.fetchall()
        meal_name = str(data[0][0])
        meal_type = str(data[0][1])
        meal_calories = str(data[0][2])
        meal_image = str(data[0][3])
        meal_serving_size = str(data[0][4])
        image = '\static\uploads\ '+ meal_image
        c.execute("SELECT * FROM instruction WHERE recipe_id = '"+ recipeId +"'")
        date = c.fetchall()
        for i in range (0,len(date)):
            lst.append(str(date[i][0])+","+str(date[i][1]))
        recipe = {'recipe_name' : recipe_name,'recipe_rating' : recipe_rating, 'recipe_preparation_time':recipe_preparation_time,'meal_name':meal_name,
        'meal_type': meal_type,'meal_calories': meal_calories,'meal_image' : image , 'meal_serving_size': meal_serving_size, 'instructions':str(lst)}
        return render_template("norecipe.html",recipe=recipe)
    #     image = '/static/uploads/' + data
    #     recipe = {'recipe_id': c.fetchone(1), 'name': c.fetchone(2), 'rating': c.fetchone(3), 'preparation_time':c.fetchone(4)}
    # return render_template("norecipe.html", recipe=recipe)

@app.route('/addrecipe/',methods=["POST","GET"])
@login_required
def addrecipe():
    try:
        form = RecipeForm(csrf_enabled=False)
        if request.method == "POST":
            if form.validate() == False:
                flash('All fields are required.')
                return render_template('recipeform.html',form=form)
            else:
                name = form.name.data
                rating = form.rating.data
                preparation_time = form.preparation_time.data
                instruction_technique = form.instruction_technique.data
                ingredient_name = form.ingredient_name.data
                quantity = form.quantity.data
                note = form.note.data
                step = form.step.data
                

                c, conn = connection()
                x = c.execute("SELECT * FROM recipe WHERE name = '"+thwart(name)+"'")


                if int(x) > 0:
                    flash("That recipe has already been added")
                    return render_template('recipeform.html', form=form)

                else:
                    c.execute("INSERT INTO ingredients (firstname, lastname, gender ,email, password) VALUES (%s, %s, %s, %s,%s)",
                              (thwart(firstname), thwart(lastname), thwart(gender), thwart(email), thwart(password)))
                    c.execute("INSERT INTO recipe (firstname, lastname, gender ,email, password) VALUES (%s, %s, %s, %s,%s)",
                              (thwart(firstname), thwart(lastname), thwart(gender), thwart(email), thwart(password)))
                    
                    conn.commit()
                    flash("Thanks for registering!")
                    c.close()
                    conn.close()
                    gc.collect()

                    session['logged_in'] = True
                    session['user'] = email

                    return render_template("home.html")

        return render_template("register.html", form=form)

    except Exception as e:
        return(str(e))


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)

@app.route("/timeinfo/")
def timeinfo():
    return time.strftime("%a, %d %b %Y")

@app.route("/logout/")
@login_required
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('home'))

@app.route("/generateMealPlan/",methods=["POST","GET"])
def mealplan():
        c, conn = connection() 
        c.execute("INSERT INTO mealplan (countMeal) VALUES (35)")
        a = str(c.lastrowid)
        c.execute("SELECT meal_id FROM meal WHERE type = 'B' ORDER BY RAND() LIMIT 7 ")
        breakfasts = c.fetchall()
        c.execute("SELECT meal_id FROM meal WHERE type = 'L' ORDER BY RAND() LIMIT 7 ")
        lunch = c.fetchall()
        c.execute("SELECT meal_id FROM meal WHERE type = 'D' ORDER BY RAND() LIMIT 7 ")
        dinner = c.fetchall()
        c.execute("SELECT meal_id FROM meal WHERE type = 'S' ORDER BY RAND() LIMIT 14 ")
        snacks = c.fetchall()
        i = 0
        u= 0
        y=0
        t=0
        while i <= (len(snacks))-1:
            snack = str(snacks[i][0])
            
            #c.execute("INSERT INTO generates(mealplan_id,meal_id) VALUES (%d,%s)", 1,snacks[i][0])
            c.execute("INSERT INTO generates (meal_id,mealplan_id) VALUES (%s, %s)",(int(snack),a))
            i += 1
        while u <= (len(dinner))-1:
            dinner = str(dinner[u][0])
            c.execute("INSERT INTO generates (meal_id,mealplan_id) VALUES (%s, %s)",(int(dinner),a))
            u+=1
        while y <= (len(lunch))-1:
            lunch = str(lunch[y][0])
            c.execute("INSERT INTO generates (meal_id,mealplan_id) VALUES (%s, %s)",(int(lunch),a))
            y+=1
        while t <= (len(breakfasts))-1:
            breakfast = str(breakfasts[t][0])
            c.execute("INSERT INTO generates (meal_id,mealplan_id) VALUES (%s, %s)",(int(breakfast),a))
            t+=1
        return "str(breakfast[t][0])"

@app.route("/mealplan/",methods=["GET","POST"])
def viewmealplan():
    c,conn = connection()
    a = date.today()
    c.execute("SELECT mealplan_id FROM mealplan WHERE '"+a+"' between created_at and enddate ")
    data = str(c.fetchall())
    return data

@app.route("/meals/",methods=["GET","POST"])
def meal():
    return render_template("index-2.html")


@app.route("/supermarket/",methods=["POST","GET"])
def supermarket():
    try:
        if request.method == "GET":
            c,conn = connection()
            c.execute("SELECT ingredient.name, ingredient.quantity FROM  mealplan JOIN generates JOIN meal JOIN recipe ingredient WHERE ingredient.name NOT IN (SELECT * FROM KITCHEN)")
            return render_template("supermarket.html", lst=c.fetchall())
    except Exception as e:
        return(str(e))
    

        

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response

# ====================================
#				Error Pages
# ====================================
@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404



# ====================================
#				Search Page
# ====================================
@app.route('/search')
def search():
	return 'Search'

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

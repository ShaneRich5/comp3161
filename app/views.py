"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

from app import app,mysql, bcrypt
from flask import render_template, request, redirect, url_for,flash, session , jsonify
from functools import wraps
import time, sendemail
from form import ContactForm, RegistrationForm, LoginForm
from dbconnect import connection
from MySQLdb import escape_string as thwart
import logging
from logging.handlers import RotatingFileHandler
from datetime import *
import gc
from .sendemail import *


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

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


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8888")
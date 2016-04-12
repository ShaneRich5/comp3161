from app import app
from flask import render_template, request,flash
import helpers

import datetime

@app.route('/')
def home():
    return render_template('home.html')


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


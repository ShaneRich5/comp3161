from app import app, db
from flask import render_template, request 

@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home_page():
	return render_template('home.html')
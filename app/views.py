from app import app, mysql
from flask import render_template, request 

@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM pdo_ret.members''')
    rv = cur.fetchall()
    return str(rv)
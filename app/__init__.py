from flask import Flask
from flask.ext.mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "CHANGEME"
mysql = MySQL()
mysql.init_app(app)

from app import views
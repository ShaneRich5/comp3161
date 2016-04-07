from flask import Flask
from flask.ext.mysqldb import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pdo_ret'
app.config['MYSQL_HOST'] = 'localhost'
mysql.init_app(app)

from app import views
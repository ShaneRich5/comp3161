from flask import Flask
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'pdo_ret'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

from app import views
# MYSQL
mysql_db_username = 'placeholder'
mysql_db_password = 'placeholder'
mysql_db_name = 'placeholder'
mysql_db_hostname = 'placeholder'

DEBUG = True
PORT = 5000
HOST = "0.0.0.0"
SQLALCHEMY_ECHO = False
SECRET_KEY = "SOME SECRET"

# MySQL
SQLALCHEMY_DATABASE_URI = "mysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=mysql_db_username,
																					DB_PASS=mysql_db_password,
                                                                                    DB_ADDR=mysql_db_hostname,
                                                                                    DB_NAME=mysql_db_name)
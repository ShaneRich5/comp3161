class Config(Object):
	DEBUG = False
	TESTING = False
	SECRET_KEY = "changeme"
	SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/comp3161'

class DevConfig(Config):
	TESTING = True
	DEBUG = True
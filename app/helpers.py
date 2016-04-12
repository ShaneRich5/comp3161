import MySQLdb as mdb 
import sys
from faker import Factory
import random


def retrieve_all_users():
	cur, conn = initialize_connection()

	

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
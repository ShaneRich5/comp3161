# from app import app

import MySQLdb as mdb 
import sys

def migrate_database():
	try:
		con = mdb.connect('localhost', 'root', 'root')
		cur = con.cursor()

		drop_db = 'drop database if exists comp3161'
		create_db = 'create database comp3161'
		select_db = 'use comp3161'

		initialize_db = [
			drop_db, create_db, select_db
		]

		for stmt in initialize_db:
			cur.execute(stmt)

		create_user_table = """CREATE TABLE user(
			userid integer(50) not null unique,
			first_name varchar(80) not null,
			last_name varchar(80) not null,
			gender char(1) not null,
			email varchar(80) not null,
			password varchar(80) not null,
			recipeId integer(50) ,
			updated_at date not null,
			created_at date not null,
			Primary Key(userid)
		);"""

		create_meal_table = """CREATE TABLE meal(
			mid integer(50) not null unique,
			name varchar(80) not null,
			type char(1) not null,
			recipeId integer(50) not null,
			calories varchar(20) not null,
			image varchar(80) not null,
			serving_size varchar(30) not null,
			Primary Key(mid)
		);"""

		create_meal_table = """CREATE TABLE meal(
			mid integer(50) not null unique,
			name varchar(80) not null,
			type char(1) not null,
			recipeId integer(50) not null,
			calories varchar(20) not null,
			image varchar(80) not null,
			serving_size varchar(30) not null,
			Primary Key(mid)
		);"""

		create_recipe_table = """CREATE TABLE recipe(
			rid integer(50) not null unique,
			name  varchar(80) not null,
			rating  integer(20) not null,
			preparation_time integer(20) not null,
			ingredientId integer(50) not null,
			instructionId integer(50) not null,
			updated_at date not null,
			created_at date not null,
			Primary Key(rid)
		);"""

		create_ingredient_table = """CREATE TABLE ingredient(
			ingred_id integer(50) not null unique,
			name varchar(80) not null,
			quantity integer(50) not null,
			note varchar(80) not null,
			updated_at date not null,
			created_at date not null,
			Primary Key(ingred_id)
		);"""

		create_instruction_table = """CREATE TABLE instruction(
			instruc_id integer(50) not null unique,
			technique varchar(80) not null,
			step  integer(50) not null,
			recipeId integer(50) not null,
			updated_at date not null,
			created_at date not null,
			Primary Key(instruc_id)
		);"""

		create_inventory_table = """CREATE TABLE inventory(
			inid integer(50) not null unique,
			quantity integer(20) not null,
			category varchar(80) not null,
			updated_at date not null,
			mealplanId integer(80) not null,
			created_at date not null,
			Primary Key(inid)
		);"""

		create_mealplan_table = """CREATE TABLE mealplan(
			mpid integer(50) not null unique,
			mealId integer(50) not null,
			countMeal integer(50) not null,
			updated_at date not null,
			created_at date not null,
			Primary Key(mpid)
		);"""

		create_supermarket_table = """CREATE TABLE supermarketlist(
			sid integer(50) not null unique,
			name varchar(80) not null,
			updated_at date not null,
			quantity integer(50) not null,
			mealplanId integer(50) not null,
			inventoryId integer(50) not null,
			created_at date not null,
			Primary Key(sid)
		);"""

		create_adds_table = """CREATE TABLE adds(
			userid integer(80) not null,
			recipeId integer(80) not null,
			created_at date not null,
			Primary Key(userid,recipeId)
		);"""

		statements = [create_user_table, create_meal_table, 
			create_recipe_table, create_ingredient_table, create_instruction_table,
			create_inventory_table, create_mealplan_table, create_supermarket_table,
			create_adds_table
		]

		for stmt in statements:
			cur.execute(stmt)

	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		if con:
			con.close()

migrate_database()




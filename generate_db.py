# from app import app

import MySQLdb as mdb 
import sys
from faker import Factory
import random

# Globals
fake = Factory.create()

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
			userid integer(50) not null unique AUTO_INCREMENT,
			first_name varchar(80) not null,
			last_name varchar(80) not null,
			gender varchar(10) not null,
			email varchar(80) not null,
			password varchar(80) not null,
			recipeId integer(50) ,
			updated_at datetime not null,
			created_at datetime not null,
			Primary Key(userid)
		);"""

		create_meal_table = """CREATE TABLE meal(
			mid integer(50) not null unique AUTO_INCREMENT,
			name varchar(80) not null,
			type char(1) not null,
			recipeId integer(50) not null,
			calories varchar(20) not null,
			image varchar(80) not null,
			serving_size varchar(30) not null,
			Primary Key(mid)
		);"""

		# create_meal_table = """CREATE TABLE meal(
		# 	mid integer(50) not null unique,
		# 	name varchar(80) not null,
		# 	type char(1) not null,
		# 	recipeId integer(50) not null,
		# 	calories varchar(20) not null,
		# 	image varchar(80) not null,
		# 	serving_size varchar(30) not null,
		# 	Primary Key(mid)
		# );"""

		create_recipe_table = """CREATE TABLE recipe(
			rid integer(50) not null unique AUTO_INCREMENT,
			name  varchar(80) not null,
			rating  integer(20) not null,
			preparation_time integer(20) not null,
			# ingredientId integer(50) not null,
			# instructionId integer(50) not null,
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

def generate_timestamps():
	return fake.date_time(), fake.date_time()

def populate_database():
	try:
		con = mdb.connect('localhost', 'root', 'root')
		cur = con.cursor()
		cur.execute('use comp3161')
		
		gender_opt = ['M', 'F']

		user_insert_stmt = """INSERT INTO 
				user(first_name, last_name, gender, email, password, created_at, updated_at)
				values ("{}", "{}", '{}', '{}', '{}', '{}', '{}');"""

		# populate user
		for i in range(0, 500000):
			first_name = fake.first_name()
			last_name = fake.last_name()
			gender = gender_opt[random.randrange(0, 2)]
			email = fake.email()
			password = first_name
			created_at, updated_at = generate_timestamps()

			user_insert_stmt.format(first_name, last_name, gender, email, password, created_at, updated_at)
			cur.execute(user_insert_stmt)

		recipe_insert_stmt = """INSERT INTO
				recipe(name, rating, preparation_time, created_at, updated_at)
				values ("{}", {}, {}, '{}', '{}');"""

		# populate recipe
		for i in range(0, 1000000):
			name = fake.word
			rating = random.randrange(0, 11)
			preparation_time = random.randrange(30, 121)
			created_at, updated_at = generate_timestamps()

			recipe_insert_stmt.format(name, rating, preparation_time, created_at, updated_at)
			cur.execute(recipe_insert_stmt)

		con.commit()

		

	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0], e.args[1])
		con.rollback()
		sys.exit(1)
	finally:
		if con:
			con.close()



migrate_database()
populate_database()


# [method for method in dir(fake) if callable(getattr(fake, method))]
# ['_Generator__format_token', '__class__', '__delattr__', '__format__', '__getattribute__', '__hash__', '__init__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'add_provider', 'address', 'am_pm', 'binary', 'boolean', 'bothify', 'bs', 'building_number', 'catch_phrase', 'century', 'chrome', 'city', 'city_prefix', 'city_suffix', 'color_name', 'company', 'company_email', 'company_suffix', 'country', 'country_code', 'credit_card_expire', 'credit_card_full', 'credit_card_number', 'credit_card_provider', 'credit_card_security_code', 'currency_code', 'date', 'date_time', 'date_time_ad', 'date_time_between', 'date_time_between_dates', 'date_time_this_century', 'date_time_this_decade', 'date_time_this_month', 'date_time_this_year', 'day_of_month', 'day_of_week', 'domain_name', 'domain_word', 'ean', 'ean13', 'ean8', 'email', 'file_extension', 'file_name', 'firefox', 'first_name', 'first_name_female', 'first_name_male', 'format', 'free_email', 'free_email_domain', 'geo_coordinate', 'get_formatter', 'get_providers', 'hex_color', 'image_url', 'internet_explorer', 'ipv4', 'ipv6', 'iso8601', 'job', 'language_code', 'last_name', 'last_name_female', 'last_name_male', 'latitude', 'lexify', 'linux_platform_token', 'linux_processor', 'locale', 'longitude', 'mac_address', 'mac_platform_token', 'mac_processor', 'md5', 'military_apo', 'military_dpo', 'military_ship', 'military_state', 'mime_type', 'month', 'month_name', 'name', 'name_female', 'name_male', 'null_boolean', 'numerify', 'opera', 'paragraph', 'paragraphs', 'parse', 'password', 'phone_number', 'postalcode', 'postalcode_plus4', 'postcode', 'prefix', 'prefix_female', 'prefix_male', 'profile', 'provider', 'pybool', 'pydecimal', 'pydict', 'pyfloat', 'pyint', 'pyiterable', 'pylist', 'pyset', 'pystr', 'pystruct', 'pytuple', 'random_digit', 'random_digit_not_null', 'random_digit_not_null_or_empty', 'random_digit_or_empty', 'random_element', 'random_int', 'random_letter', 'random_number', 'randomize_nb_elements', 'rgb_color', 'rgb_color_list', 'rgb_css_color', 'safari', 'safe_color_name', 'safe_email', 'safe_hex_color', 'secondary_address', 'seed', 'sentence', 'sentences', 'set_formatter', 'sha1', 'sha256', 'simple_profile', 'slug', 'ssn', 'state', 'state_abbr', 'street_address', 'street_name', 'street_suffix', 'suffix', 'suffix_female', 'suffix_male', 'text', 'time', 'time_delta', 'timezone', 'tld', 'unix_time', 'uri', 'uri_extension', 'uri_page', 'uri_path', 'url', 'user_agent', 'user_name', 'uuid4', 'windows_platform_token', 'word', 'words', 'year', 'zipcode', 'zipcode_plus4']

drop Database if exists DATABASE_PROJECT;

CREATE DATABASE DATABASE_PROJECT;

USE DATABASE_PROJECT;

CREATE TABLE user(
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
);

CREATE TABLE meal(
	mid integer(50) not null unique,
	name varchar(80) not null,
	type char(1) not null,
	recipeId integer(50) not null,
	calories varchar(20) not null,
	image varchar(80) not null,
	serving_size varchar(30) not null,
	Primary Key(mid)
);

CREATE TABLE recipe(
	rid integer(50) not null unique,
	name  varchar(80) not null,
	rating  integer(20) not null,
	preparation_time integer(20) not null,
	ingredientId integer(50) not null,
	instructionId integer(50) not null,
	updated_at date not null,
	created_at date not null,
	Primary Key(rid)
);

CREATE TABLE ingredient(
	ingred_id integer(50) not null unique,
	name varchar(80) not null,
	quantity integer(50) not null,
	note varchar(80) not null,
	updated_at date not null,
	created_at date not null,
	Primary Key(ingred_id)
);

CREATE TABLE instruction(
	instruc_id integer(50) not null unique,
	technique varchar(80) not null,
	step  integer(50) not null,
	recipeId integer(50) not null,
	updated_at date not null,
	created_at date not null,
	Primary Key(instruc_id)
);

CREATE TABLE inventory(
	inid integer(50) not null unique,
	quantity integer(20) not null,
	category varchar(80) not null,
	updated_at date not null,
	mealplanId integer(80) not null,
	created_at date not null,
	Primary Key(inid)
);

CREATE TABLE mealplan(
	mpid integer(50) not null unique,
	mealId integer(50) not null,
	countMeal integer(50) not null,
	updated_at date not null,
	created_at date not null,
	Primary Key(mpid)
);

CREATE TABLE supermarketlist(
	sid integer(50) not null unique,
	name varchar(80) not null,
	updated_at date not null,
	quantity integer(50) not null,
	mealplanId integer(50) not null,
	inventoryId integer(50) not null,
	created_at date not null,
	Primary Key(sid)
);

CREATE TABLE adds(
	userid integer(80) not null,
	recipeId integer(80) not null,
	created_at date not null,
	Primary Key(userid,recipeId)
);




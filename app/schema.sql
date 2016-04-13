drop database if exists comp3161;
create database comp3161;
use comp3161;

CREATE TABLE user(
	user_id integer(50) not null unique AUTO_INCREMENT,
	email varchar(100) not null,
	password varchar(80) not null,
	first_name varchar(80) not null,
	last_name varchar(80) not null,
	dob datetime not null,
	gender varchar(10) not null,
	primary key(user_id)
);

CREATE TABLE recipe(
	recipe_id integer(50) not null unique AUTO_INCREMENT,
	name varchar(80) not null,
	rating integer(20) not null,
	preparation_time integer(20) not null,
	Primary Key(recipe_id)
);

CREATE TABLE adds(
	user_id integer(80) not null,
	recipe_id integer(50) not null,
	primary key(user_id, recipe_id),
	foreign key(user_id) references user(user_id) on update cascade on delete cascade,
	foreign key(recipe_id) references recipe(recipe_id) on update cascade on delete cascade
);

CREATE TABLE instruction(
	sequence integer not null,
	action varchar(80) not null,
	recipe_id integer not null,
	primary key(sequence, recipe_id),
	foreign key(recipe_id) references recipe(recipe_id) on update cascade on delete cascade
);

CREATE TABLE ingredient(
	name varchar(80) not null,
	quantity integer(50) not null,
	units varchar(80) not null,
	description varchar(80) not null,
	Primary Key(name)
);

CREATE TABLE inventory(
	inventory_id integer(50) not null unique,
	quantity integer(20) not null,
	category varchar(80) not null,
	updated_at date not null,
	mealplanId integer(80) not null,
	created_at date not null,
	Primary Key(inid)
);

CREATE TABLE mealplan(
	mealplan_id integer(50) not null unique,
	meal_id integer(50) not null,
	countMeal integer(50) not null,
	updated_at date not null,
	created_at date not null,
	Primary Key(mealplan_id)
);

CREATE TABLE meal(
	meal_id integer(50) not null unique AUTO_INCREMENT,
	name varchar(80) not null,
	type char(1) not null,
	calories varchar(20) not null,
	image varchar(80) not null,
	serving_size varchar(30) not null,
	recipe_id integer(50) not null,
	primary key(meal_id),
	foreign key(recipe_id) references recipe(recipe_id) on update cascade on delete cascade
);
	
CREATE TABLE generates(
	meal_id integer(50) not null,
	mealplan_id integer(50) not null,
	primary key(meal_id, mealplan_id),
	foreign key (meal_id) references meal(meal_id) on update cascade on delete cascade,
	foreign key (mealplan_id) references mealplan(mealplan_id) on update cascade on delete cascade
);

CREATE TABLE supermarketlist(
	supermarket_id integer(50) not null unique,
	name varchar(80) not null,
	updated_at date not null,
	quantity integer(50) not null,
	mealplanId integer(50) not null,
	inventoryId integer(50) not null,
	created_at date not null,
	primary key(supermarket_id)
);

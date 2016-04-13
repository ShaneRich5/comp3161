delimiter //

# retrieve all instructions for a given recipe
create procedure retrieve_instructions (IN recipe_id integer)
begin
	select * from instructions i where i.recipe_id=recipe_id;
end //

create procedure count_recipes ()
begin
	select count(*) from recipe;
end //

# calculate calorie count for meal plan
-- create procedure calculate_mealplan_calories (IN mealplan_id integer)
-- begin
-- 	select sum(r.calories) from recipe r 
-- 	join meal m where r.id=m.recipe_id 
-- 	join generates g where g.meal_id=g.mealplan_id and g.mealplan_id=mealplan_id;
-- end //

delimiter ;


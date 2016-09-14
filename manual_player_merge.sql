-- manual_player_merge.sql

-- Despite my best efforts, there will be some players who will enter under wildly different tags that will make it impossible to assign them to the same player id right off the bat.
-- In this script, we go through and track the changes I am forced to make.

-- Usage: mysql nc_smash4 < manual_player_merge.sql

-- example: if "Dandy Penguin" was the main tag of "Stingers"
-- goal: overwrite stingers p_id with dandy penguin's p_id

-- set @dp_id = (select p_id from players where main_tag = 'dandy penguin');
-- update players set p_id = @dp_id where main_tag = 'stingers' ;

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 



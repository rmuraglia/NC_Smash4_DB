-- manual_player_merge.sql

-- NOTE: THIS ENDED UP ACTUALLY BEING IMPLEMENTED IN PYTHON IN MANUAL_PLAYER_MERGE.PY
-- it was simply easier to write a function in python for it, but I kept this skeleton of a script to illustrate how to save and use variables in sql

-- Despite my best efforts, there will be some players who will enter under wildly different tags that will make it impossible to assign them to the same player id right off the bat.
-- In this script, we go through and track the changes I am forced to make.

-- Usage: mysql nc_smash4 < manual_player_merge.sql

-- example: Trey Monk usually enters under the name "Haise" but now occasionally enters as "Centipede" or "OneEyedKing".
-- goal: set "Centipede" and "OneEyedKing" p_id equal to "Haise" p_id

-- set @orig_id = (select p_id from players where main_tag = 'haise');
-- update players set p_id = @orig_id where main_tag = 'centipede' ;
-- update players set p_id = @orig_id where main_tag = 'oneeyedking' ;

-- now we can easily select all of Trey Monk's results by searching for the IDs associated with his p_id (which we can find by searching for any of his tags)
-- select id from players where p_id = <Trey's p_id>
-- use IDs returned from previous query to trace back his challonge tag ID for each tournament, which leads to his sets.

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 



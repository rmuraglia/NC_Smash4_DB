-- init_s4.sql

-- to remember root or leaf, think that the leaves have no foreign keys

-- drop tables in order from root to leaves if they exist
drop table if exists player_tournament_junction;
drop table if exists sets;
drop table if exists tournaments;
drop table if exists tags;
drop table if exists seasons;
drop table if exists players;

-- create tables in order from leaves to root
create table players (
    id int not null auto_increment,
    p_id int, 
    main_tag varchar(128),
    real_name varchar(128),
    primary key (id)
);
-- p_id will be manually merged to same value for players who enter under many pseudonyms. Will then query for all 'id' associated with their 'p_id' and select games based on that 'id' set.

create table seasons (
    id tinyint not null,
    start_date date,
    end_date date,
    rank01 int, rank02 int, rank03 int, rank04 int, rank05 int,
    rank06 int, rank07 int, rank08 int, rank09 int, rank10 int,
    rank11 int, rank12 int, rank13 int, rank14 int, rank15 int,
    rank16 int, rank17 int, rank18 int, rank19 int, rank20 int,
    primary key (id)
);

create table tags (
    id int not null,
    tag varchar(128),
    player_id int,
    primary key (id),
    foreign key (player_id) references players(id)
);

create table tournaments (
    id int not null,
    title varchar(128),
    tourney_date date,
    season tinyint,
    num_entrants smallint,
    url varchar(128),
    primary key (id),
    foreign key (season) references seasons(id)
);

create table sets (
    id int not null,
    tourney_id int not null,
    round tinyint,
    p1_id int not null,
    p2_id int not null,
    p1_score tinyint,
    p2_score tinyint,
    winner tinyint,
    p1_prev_set int,
    p2_prev_set int,
    p1_prev_lose bool,
    p2_prev_lose bool,
    -- underway_at datetime,
    -- completed_at datetime,
    primary key (id),
    foreign key (p1_id) references tags(id),
    foreign key (p2_id) references tags(id),
    foreign key (tourney_id) references tournaments(id)
);

create table player_tournament_junction (
    tourney_id int not null,
    player_id int not null,
    seed smallint,
    final_rank smallint,
    primary key (tourney_id, player_id),
    foreign key (tourney_id) references tournaments(id),
    foreign key (player_id) references players(id)
);
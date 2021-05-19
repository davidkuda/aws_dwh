CREATE TABLE IF NOT EXISTS songplays (
	songplay_id INTEGER SORTKEY DISTKEY,
	start_time TIMESTAMP,
	user_id INTEGER,
	level VARCHAR(20),
	song_id INTEGER,
	artist_id INTEGER,
	session_id INTEGER,
	location VARCHAR(50),
	user_agent VARCHAR
);

CREATE TABLE IF NOT EXISTS  users (
	user_id INTEGER SORTKEY,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	gender VARCHAR(20),
	level VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS songs (
	song_id INTEGER SORTKEY,
	title VARCHAR(50),
	artist_id INTEGER,
	year SMALLINT,
	duration SMALLINT
);

CREATE TABLE IF NOT EXISTS artists (
	artist_id INTEGER SORTKEY,
	name VARCHAR(50),
	location VARCHAR(50),
	latitude DECIMAL,
	longitude DECIMAL
);

CREATE TABLE IF NOT EXISTS time (
	start_time TIMESTAMP,
	hour SMALLINT,
	day SMALLINT,
	week SMALLINT,
	month SMALLINT,
	year SMALLINT,
	weekday SMALLINT
);

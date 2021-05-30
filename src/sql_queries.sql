CREATE TABLE IF NOT EXISTS songplays (
	songplay_id INTEGER PRIMARY KEY NOT NULL SORTKEY DISTKEY,
	start_time TIMESTAMP NOT NULL REFERENCES time(start_time),
	user_id INTEGER NOT NULL REFERENCES users(user_id),
	level VARCHAR(20) NOT NULL,
	song_id INTEGER NOT NULL REFERENCES songs(song_id),
	artist_id INTEGER NOT NULL REFERENCES artists(artist_id),
	session_id INTEGER NOT NULL,
	location VARCHAR(50) NOT NULL,
	user_agent VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS  users (
	user_id INTEGER PRIMARY KEY NOT NULL SORTKEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	gender VARCHAR(20) NOT NULL,
	level VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS songs (
	song_id INTEGER PRIMARY KEY NOT NULL SORTKEY,
	title VARCHAR(50) NOT NULL,
	artist_id INTEGER NOT NULL,
	year SMALLINT NOT NULL,
	duration SMALLINT NOT NULL
);

CREATE TABLE IF NOT EXISTS artists (
	artist_id INTEGER PRIMARY KEY NOT NULL SORTKEY,
	name VARCHAR(50) NOT NULL,
	location VARCHAR(50) NOT NULL,
	latitude DECIMAL NOT NULL,
	longitude DECIMAL NOT NULL
);

CREATE TABLE IF NOT EXISTS time (
	start_time TIMESTAMP PRIMARY KEY NOT NULL,
	hour SMALLINT NOT NULL,
	day SMALLINT NOT NULL,
	week SMALLINT NOT NULL,
	month SMALLINT NOT NULL,
	year SMALLINT NOT NULL,
	weekday SMALLINT NOT NULL
);

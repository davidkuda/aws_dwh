CREATE TABLE IF NOT EXISTS songplays (
	songplay_id IDENTITY(0,1) PRIMARY KEY NOT NULL SORTKEY DISTKEY,
	start_time TIMESTAMP NOT NULL REFERENCES time(start_time),
	user_id INTEGER NOT NULL REFERENCES users(user_id),
	level VARCHAR(20) NOT NULL,
	song_id INTEGER NOT NULL REFERENCES songs(song_id),
	artist_id INTEGER NOT NULL REFERENCES artists(artist_id),
	session_id INTEGER NOT NULL,
	location VARCHAR(50) NOT NULL,
	user_agent VARCHAR NOT NULL
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

CREATE TABLE IF NOT EXISTS  users (
	user_id INTEGER PRIMARY KEY NOT NULL SORTKEY,
	first_name VARCHAR(50) NOT NULL,
	last_name VARCHAR(50) NOT NULL,
	gender VARCHAR(20) NOT NULL,
	level VARCHAR(20) NOT NULL
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

CREATE TABLE IF NOT EXISTS "staging_log_data" (
    "artist" TEXT,
    "auth" VARCHAR(12) NOT NULL,
    "firstName" TEXT NOT NULL,
    "gender" TEXT NOT NULL,
    "itemInSession" INTEGER NOT NULL,
    "length" DECIMAL,
    "level" VARCHAR(12) NOT NULL,
    "location" TEXT NOT NULL,
    "method" VARCHAR(7) NOT NULL,
    "page" TEXT,
    "registration" VARCHAR(12),
    "sessionId" INTEGER NOT NULL,
    "song" TEXT,
    "status" SMALLINT NOT NULL,
    "timestamp" BIGINT NOT NULL,
    "userAgent" TEXT NOT NULL,
    "userId" INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS "staging_song_data" (
    "artist_id" VARCHAR NOT NULL,
    "artist_latitude" DECIMAL,
    "artist_longitude" DECIMAL,
    "artist_name" VARCHAR,
    "duration" DECIMAL,
    "num_songs" INTEGER,
    "song_id" VARCHAR,
    "title" VARCHAR,
    "year" INTEGER
);

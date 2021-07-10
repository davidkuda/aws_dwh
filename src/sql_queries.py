import configparser

from aws_client.aws_client import get_aws_instance


read_s3_role_arn = get_aws_instance().get_iam_role_arn()


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create = ("""
CREATE TABLE IF NOT EXISTS "staging_events" (
    "artist" VARCHAR,
    "auth" VARCHAR(12),
    "firstName" VARCHAR,
    "lastName" VARCHAR,
    "gender" CHAR,
    "itemInSession" INTEGER,
    "length" DECIMAL,
    "level" VARCHAR(12),
    "location" VARCHAR,
    "method" VARCHAR(7),
    "page" VARCHAR,
    "registration" BIGINT,
    "sessionId" INTEGER,
    "song" VARCHAR,
    "status" SMALLINT,
    "ts" BIGINT,
    "userAgent" VARCHAR,
    "userId" INTEGER
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS "staging_songs" (
    "artist_id" VARCHAR NOT NULL,
    "artist_latitude" DECIMAL,
    "artist_location" VARCHAR,
    "artist_longitude" DECIMAL,
    "artist_name" VARCHAR,
    "duration" DECIMAL,
    "num_songs" INTEGER,
    "song_id" VARCHAR,
    "title" VARCHAR,
    "year" INTEGER
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id INTEGER IDENTITY(0,1) PRIMARY KEY NOT NULL SORTKEY DISTKEY,
    start_time TIMESTAMP REFERENCES time(start_time),
    user_id VARCHAR(18) REFERENCES users(user_id),
    level VARCHAR(20),
    song_id VARCHAR(18) REFERENCES songs(song_id),
    artist_id VARCHAR(18) REFERENCES artists(artist_id),
    session_id INTEGER,
    location VARCHAR(50),
    user_agent VARCHAR
)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS  users (
	user_id INTEGER PRIMARY KEY SORTKEY,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	gender VARCHAR(20),
	level VARCHAR(20)
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR(18) PRIMARY KEY NOT NULL SORTKEY,
    title VARCHAR NOT NULL,
    artist_id VARCHAR(18) NOT NULL REFERENCES artists(artist_id),
    year SMALLINT NOT NULL,
    duration SMALLINT NOT NULL
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR PRIMARY KEY NOT NULL SORTKEY,
    name VARCHAR,
    location VARCHAR,
    latitude DECIMAL,
    longitude DECIMAL
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP PRIMARY KEY NOT NULL,
    hour SMALLINT NOT NULL,
    day SMALLINT NOT NULL,
    week SMALLINT NOT NULL,
    month SMALLINT NOT NULL,
    year SMALLINT NOT NULL,
    weekday SMALLINT NOT NULL
);
""")

# STAGING TABLES

staging_events_copy = f"""
COPY staging_events
FROM 's3://udacity-dend/log-data/'
CREDENTIALS 'aws_iam_role={read_s3_role_arn}'
REGION 'us-west-2'
JSON 'auto ignorecase';
"""

staging_songs_copy = (f"""
COPY staging_songs
FROM 's3://udacity-dend/song_data/'
CREDENTIALS 'aws_iam_role={read_s3_role_arn}'
REGION 'us-west-2'
JSON 'auto ignorecase';
""")

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (
    user_id, 
    level,
    start_time,
    song_id,
    artist_id,
    session_id,
    location,
    user_agent
)

SELECT
    userId as user_id, 
    level,
    TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' as start_time,
    song_id,
    ss.artist_id,
    sessionId as session_id,
    location,
    userAgent as user_agent
    
FROM staging_events AS se
JOIN staging_songs AS ss
    ON se.artist = ss.artist_name
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users (
    user_id,
    first_name,
    last_name,
    gender,
    level           
    )

SELECT 
    DISTINCT userId,
    firstName,
    lastName,
    gender,
    level

    FROM staging_events AS es1
        WHERE userId IS NOT null
        AND ts = (SELECT max(ts) 
                  FROM staging_events AS es2 
                  WHERE es1.userId = es2.userId)

ORDER BY userId DESC;
""")

song_table_insert = ("""
INSERT INTO songs (
    song_id,
    title,
    artist_id,
    year,
    duration
)

SELECT
    song_id,
    title,
    artist_id,
    year,
    duration
FROM staging_songs;
""")

artist_table_insert = ("""
INSERT INTO artists (
    artist_id,
    name,
    --location,
    latitude,
    longitude
)

SELECT
    artist_id,
    artist_name,
    --artist_location,
    artist_latitude,
    artist_longitude
    
FROM staging_songs;
""")

time_table_insert = ("""
INSERT INTO time (
    start_time,
    hour,
    day,
    week,
    month,
    year,
    weekday
)

SELECT  
    DISTINCT TIMESTAMP 'epoch' + ts/1000 * INTERVAL '1 second' as start_time,
    EXTRACT(hour FROM start_time) AS hour,
    EXTRACT(day FROM start_time) AS day,
    EXTRACT(week FROM start_time) AS week,
    EXTRACT(month FROM start_time) AS month,
    EXTRACT(year FROM start_time) AS year,
    EXTRACT(week FROM start_time) AS weekday
    
FROM staging_events
WHERE staging_events.page = 'NextSong';
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create,
                        staging_songs_table_create,
                        user_table_create,
                        artist_table_create,
                        song_table_create,
                        time_table_create,
                        songplay_table_create]

drop_table_queries = [staging_events_table_drop,
                      staging_songs_table_drop,
                      songplay_table_drop,
                      user_table_drop,
                      artist_table_drop,
                      song_table_drop,
                      time_table_drop]

copy_table_queries = [staging_events_copy, staging_songs_copy]

insert_table_queries = [songplay_table_insert,
                        user_table_insert,
                        song_table_insert,
                        artist_table_insert,
                        time_table_insert]

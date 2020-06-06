import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP table IF EXISTS staging_events CASCADE;"
staging_songs_table_drop = "DROP table IF EXISTS staging_songs CASCADE;"
songplay_table_drop = "DROP table IF EXISTS songplays CASCADE;"
user_table_drop = "DROP table IF EXISTS users CASCADE;"
song_table_drop = "DROP table IF EXISTS songs CASCADE;"
artist_table_drop = "DROP table IF EXISTS artists CASCADE;"
time_table_drop = "DROP table IF EXISTS time CASCADE;"


# CREATE TABLES

staging_events_table_create= ("""
    CREATE TABLE IF NOT EXISTS staging_events (
        artist              VARCHAR,
        auth                VARCHAR,
        firstName           VARCHAR,
        gender              VARCHAR,
        itemInSession       INTEGER,
        lastName            VARCHAR,
        length              NUMERIC,
        level               VARCHAR,
        location            VARCHAR,
        method              VARCHAR,
        page                VARCHAR,
        registration        NUMERIC,
        sessionId           INTEGER,
        song                VARCHAR,
        status              INTEGER,
        ts                  BIGINT,
        userAgent           VARCHAR,
        userId              INTEGER
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs           INTEGER, 
        artist_id           VARCHAR, 
        artist_latitude     NUMERIC, 
        artist_longitude    NUMERIC, 
        artist_location     VARCHAR,
        artist_name         VARCHAR,
        song_id             VARCHAR,
        title               VARCHAR,
        duration            NUMERIC, 
        year                INTEGER
    );
""")

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id        INTEGER              IDENTITY(0,1) PRIMARY KEY,
        start_time         TIMESTAMP            NOT NULL SORTKEY DISTKEY, 
        user_id            INTEGER              NOT NULL, 
        level              VARCHAR, 
        song_id            VARCHAR              NOT NULL,
        artist_id          VARCHAR              NOT NULL, 
        session_id         INTEGER, 
        location           VARCHAR, 
        user_agent         VARCHAR
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id            INTEGER  SORTKEY PRIMARY KEY, 
        first_name         VARCHAR, 
        last_name          VARCHAR, 
        gender             VARCHAR, 
        level              VARCHAR
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id           VARCHAR  SORTKEY PRIMARY KEY, 
        title             VARCHAR  NOT NULL, 
        artist_id         VARCHAR  NOT NULL, 
        year              INTEGER  NOT NULL, 
        duration          NUMERIC  NOT NULL
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id        VARCHAR  SORTKEY PRIMARY KEY, 
        name             VARCHAR  NOT NULL, 
        location         VARCHAR, 
        latitude         NUMERIC, 
        longitude        NUMERIC
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time      TIMESTAMP DISTKEY SORTKEY PRIMARY KEY, 
        hour            INTEGER, 
        day             INTEGER, 
        week            INTEGER, 
        month           INTEGER,
        year            INTEGER,
        weekday         INTEGER
    );
""")

# STAGING TABLES

staging_events_copy = ("""
    COPY staging_events FROM {data_bucket}
    credentials 'aws_iam_role={iam_arn}'
    JSON {log_json_path};
""").format(data_bucket=config['S3']['LOG_DATA'], iam_arn=config['IAM_ROLE']['ARN'], log_json_path=config['S3']['LOG_JSONPATH'])
# Formatting for milliseconds: https://docs.aws.amazon.com/redshift/latest/dg/r_FORMAT_strings.html

staging_songs_copy = ("""
    COPY staging_songs FROM {data_bucket}
    credentials 'aws_iam_role={iam_arn}'
    JSON 'auto' truncatecolumns;
""").format(data_bucket=config['S3']['SONG_DATA'], iam_arn=config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT DISTINCT TIMESTAMP 'epoch' + e.ts/1000 * INTERVAL '1 second' AS start_time,
           e.userId             AS user_id,
           e.level              AS level,
           s.song_id            AS song_id,
           s.artist_id          AS artist_id,
           e.sessionId          AS session_id,
           e.location           AS location,
           e.userAgent          AS user_agent
    FROM
         staging_events e
    JOIN staging_songs s
        ON (e.song=s.title AND e.artist=s.artist_name)
    WHERE e.page = 'NextSong';   
""")

user_table_insert = ("""
    INSERT INTO users (user_id, first_name, last_name, gender, level)
    SELECT DISTINCT userId    AS user_id,
           firstName          AS first_name,
           lastName           AS last_name,
           gender             AS gender,
           level              AS level
    FROM
        staging_events
    WHERE page ='NextSong';
""")

song_table_insert = ("""
    INSERT INTO songs (song_id, title, artist_id, year, duration)
    SELECT DISTINCT song_id,
           title,
           artist_id,
           year,
           duration
    FROM staging_songs;       
""")

artist_table_insert = ("""
    INSERT INTO artists (artist_id, name, location, latitude, longitude)
    SELECT DISTINCT artist_id,
           artist_name,
           artist_location,
           artist_latitude,
           artist_longitude
    FROM staging_songs;
""")

time_table_insert = ("""
    INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT DISTINCT start_time,
           EXTRACT (hour from start_time)    AS hour,
           EXTRACT (day from start_time)     AS day,
           EXTRACT (week from start_time)    AS week,
           EXTRACT (month from start_time)   AS month,
           EXTRACT (year from start_time)    AS year,
           EXTRACT (weekday from start_time) AS weekday
    FROM
        songplays; 
""")

# Analytics - get counts of each table
staging_events_count = ("""
    SELECT COUNT(*) FROM staging_events;
""")

staging_songs_count = ("""
    SELECT COUNT(*) FROM staging_songs;
""")

songplays_count = ("""
    SELECT COUNT(*) FROM songplays;
""")

users_count = ("""
    SELECT COUNT(*) FROM users;
""")

songs_count = ("""
    SELECT COUNT(*) FROM songs;
""")

artists_count = ("""
    SELECT COUNT(*) FROM artists;
""")

time_count = ("""
    SELECT COUNT(*) FROM time;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, songplay_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
table_count_queries = [staging_events_count, staging_songs_count, songplays_count, users_count, songs_count, artists_count, time_count]

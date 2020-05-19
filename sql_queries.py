import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
#ARN = config.get("IAM_ROLE", "ARN")

# DROP TABLES

staging_events_table_drop = "DROP table IF EXISTS staging_events"
staging_songs_table_drop = "DROP table IF EXISTS staging_songs"
songplay_table_drop = "DROP table IF EXISTS songplay"
user_table_drop = "DROP table IF EXISTS users"
song_table_drop = "DROP table IF EXISTS songs"
artist_table_drop = "DROP table IF EXISTS artists"
time_table_drop = "DROP table IF EXISTS time"

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
        ts                  TIMESTAMP,
        userAgent           VARCHAR,
        userid              INTEGER
    );
""")

staging_songs_table_create = ("""
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs           VARCHAR, 
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
    CREATE TABLE IF NOT EXISTS songplay (
        songplay_id        BIGINT IDENTITY(0,1),
        start_time         TIMESTAMP, 
        user_id            INTEGER REFERENCES users(user_id), 
        level              VARCHAR, 
        song_id            VARCHAR REFERENCES songs(song_id),
        artist_id          VARCHAR REFERENCES artists(artist_id), 
        session_id         INTEGER NOT NULL, 
        location           VARCHAR, 
        user_agent         VARCHAR
    );
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INT        PRIMARY KEY, 
        first_name         VARCHAR, 
        last_name          VARCHAR, 
        gender             VARCHAR, 
        level              VARCHAR
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id           VARCHAR PRIMARY KEY, 
        title             VARCHAR, 
        artist_id         VARCHAR NOT NULL, 
        year              INTEGER, 
        duration          NUMERIC
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id        VARCHAR PRIMARY KEY, 
        name             VARCHAR NOT NULL, 
        location         VARCHAR, 
        latitude         NUMERIC, 
        longitude        NUMERIC
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time (
        start_time      TIMESTAMP, 
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
    copy staging_events from {data_bucket}
    credentials 'aws_iam_role={iam_arn}'
    region 'us-west-2' format as JSON {log_json_path}
    timeformat as 'epochmillisecs';
""").format(data_bucket=config['S3']['LOG_DATA'], iam_arn=config['IAM_ROLE']['ARN'], log_json_path=config['S3']['LOG_JSONPATH'])
# Formatting for milliseconds: https://docs.aws.amazon.com/redshift/latest/dg/r_FORMAT_strings.html

staging_songs_copy = ("""
    copy staging_events from {data_bucket}
    credentials 'aws_iam_role={iam_arn}'
    region 'us-west-2';
""").format(data_bucket=config['S3']['SONG_DATA'], iam_arn=config['IAM_ROLE']['ARN'])

# FINAL TABLES

songplay_table_insert = ("""
    INSERT INTO songplays (
        songplay_id, 
        start_time, 
        user_id, 
        level, 
        song_id,
        artist_id, 
        session_id, 
        location, 
        user_agent)
    VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
    INSERT INTO users (
        user_id, 
        first_name, 
        last_name, 
        gender, 
        level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id)
    DO UPDATE
        SET level = users.level
""")

song_table_insert = ("""
    INSERT INTO songs (
       song_id, 
       title,
       artist_id,
       year,
       duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
""")

artist_table_insert = ("""
    INSERT INTO artists (
       artist_id, 
       name,
       location,
       latitude,
       longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
""")

time_table_insert = ("""
    INSERT INTO time (
       start_time, 
       hour,
       day,
       week,
       month,
       year,
       weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, user_table_create, song_table_create, artist_table_create, songplay_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

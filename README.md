# Project 3: Data Warehouse

## Introduction

This project was provided as part of Udacity's Data Engineering Nanodegree program.

A music streaming startup, *Sparkify*, has grown their user base and song database and want to move their processes and data onto the __cloud__. Their data resides in __S3__, in a directory of __JSON logs__ on user activity on the app, as well as a directory with __JSON metadata__ on the songs in their app.

As their data engineer, you are tasked with building an __ETL pipeline__ that extracts their data from S3, stages them in __Redshift__, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you you by the analytics team from Sparkify and compare your results with their expected results.

## Project Description

The goal of this project was to use AWS and Python to build an ETL pipeline for a database hosted on Redshift. To complete this project, I had to load data from S3 to staging tables on Redshift and execute __SQL__ statements that created the analytics tables from these staging tables, and then finally run queries to compare my results to the expected results.

### To run the Python scripts, follow instructions below:

1. Configure the `dwh.cfg` file with your AWS Redshift configured user name `DB_USER`, password `DB_PASSWORD`, host `HOST`, database name `DB_NAME`, port `DB_PORT`, and Amazon Resource Name `ARN`. See "Configure dwh.cfg file" section below.
1. In a terminal*, run the command `python create_cluster.py` to run the create_cluster.py script. This sets up the Redshift connection along with all necessary permissions. Before proceeding to the next steps, go to AWS Redshift Clusters and wait for the dwhcluster Cluster Status to read "available."
2. In a terminal*, run the command `python create_tables.py` to run the create_tables.py script. This sets up the database, staging tables and the analytical tables in Redshift.
2. In a terminal*, run the command `python etl.py` to run the etl.py script. This loads the staging tables and then creates the final analytic tables.
2. In a terminal*, run the command `python analytics.py` to run the analytics.py script. This loads the staging tables and then creates the final analytic tables.
3. Check whether or not all of the results of the queries match the expected results.
4. Be sure to delete the cluster on Redshift; otherwise you will continue to be billed.

&ast; Alternatively, you can run these scripts directly in a Jupyter Notebook using the format: `! python my_script.py`.

## Configure dwh.cfg file
Fill in missing fields.
```
[CLUSTER]
HOST= ''
DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_PORT=5439

[IAM_ROLE]
ARN=

[S3]
LOG_DATA='s3://udacity-dend/log_data/'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data/'

[AWS]
KEY= 
SECRET= 

[DWH] 
DWH_CLUSTER_TYPE=multi-node
DWH_NUM_NODES=4
DWH_NODE_TYPE=dc2.large

DWH_IAM_ROLE_NAME=dwhRole
DWH_CLUSTER_IDENTIFIER=dwhCluster
DWH_DB=dwh
DWH_DB_USER=dwhadmin
DWH_DB_PASSWORD=Passw0rd
DWH_PORT=5439
```

## Schema Design for the Database

The __Star schema__ design was used to create this database. The design includes 1 Fact table (songplays) and 4 Dimension tables (users, songs, artists, and time) and 2 staging tables (staging events and staging_songs). The _sql_queries.py_ file contains all of the PostgreSQL queries such as `CREATE TABLE` , `DROP table IF EXISTS` , `INSERT INTO` , `copy` and `SELECT` required to create the tables, including the staging tables. The _create_tables.py_ file is used to create the sparkifydb database, and all of the required tables that are defined in the _sql_queries.py_ script. The _etl.py_ script loads the staging tables and then inserts the data from the staging tables into the final analytical tables. The two staging tables are created first in Redshift. The final analytical tables are also created in Redshift.

![](https://github.com/AmiriMc/Data_Engineering_Data_Warehouse/blob/master/StarSchema.png?raw=t)

## ETL Pipeline
The _etl.py_ script sets up the ETL pipeline. ETL (Extract, Transform, and Load) methods were used to populate the _songs_ and _artists_ tables from the data within the JSON song files (`data/song_data/`) and to populate the _users_ and _time_ tables from the JSON log files (`data/log_data/`). A `SELECT` query gathers the `song_id` and `artist_id` information based on the title, artist name, and song duration from the log file.

## Example Queries
Some useful example queries:
* Get total number of rows in the `staging_events` table: `SELECT COUNT(*) FROM staging_events;`
* Get total number of rows in the `staging_songs` table: `SELECT COUNT(*) FROM staging_songs;`
* Get total number of rows in the `songplays` table: `SELECT COUNT(*) FROM songplays;`
* Get total number of rows in the `users` table: `SELECT COUNT(*) FROM users;`
* Get total number of songs in the `songs` table: `SELECT COUNT(*) FROM songs;`
* Get total number of artists in the `artists` table: `SELECT COUNT(*) FROM artists;`
* Get total number of rows in the `time` table: `SELECT COUNT(*) FROM time;`

These queries can be ran in three different ways: 1) command line interface (CLI), 2) from within a Jupyter Notebook, or 3) directly in the Redshift console, using the Query editor.

## Query Results

| Table            | Number of Rows |
|---               | --:            |
| staging_events   | 8056           |
| staging_songs    | 14,896         |
| songplays        | 333            |
| users            | 104            |
| songs            | 14,896         |
| artists          | 10,025         |
| time             | 333            |
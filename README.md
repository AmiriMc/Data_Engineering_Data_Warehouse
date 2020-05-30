# Project 3: Data Warehouse

## Introduction

This project was provided as part of Udacity's Data Engineering Nanodegree program.

A music streaming startup, *Sparkify*, has grown their user base and song database and want to move their processes and data onto the __cloud__. Their data resides in __S3__, in a directory of __JSON logs__ on user activity on the app, as well as a directory with __JSON metadata__ on the songs in their app.

As their data engineer, you are tasked with building an __ETL pipeline__ that extracts their data from S3, stages them in __Redshift__, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you you by the analytics team from Sparkify and compare your results with their expected results.

## Project Description

The goal of this project was to use AWS and Python to build an ETL pipeline for a database hosted on Redshift. To complete this project, I had to load data from S3 to staging tables on Redshift and execute __SQL__ statements that created the analytics tables from these staging tables, and then finally run queries to compare my results to the expected results.

### To run the Python scripts, follow instructions below:

1. Configure the `dwh.cfg` file with your AWS Redshift configured user name `DB_USER`, password `DB_PASSWORD`, host `HOST`, database name `DB_NAME`, port `DB_PORT`, and Amazon Resource Name `ARN`.
1. In a terminal, run the command `python create_tables.py` to run the create_tables.py script. This sets up the database, staging tables and the analytical tables in Redshift.
2. In a terminal, run the command `python etl.py` to run the etl.py script. This extracts the data from 
3. Check whether or not all of the results of the queries match the expected results.
4. Be sure to delete the cluster on Redshift; otherwise you will continue to be billed.

## Schema Design for the Database

The __Star schema__ design was used to create this database. The design includes 1 Fact table (songplays) and 4 Dimension tables (users, songs, artists, and time). The _sql_queries.py_ file contains all of the PostgreSQL queries such as `CREATE TABLE` , `DROP table IF EXISTS` , `INSERT INTO` , `copy` and `SELECT`. The _create_tables.py_ file is used to create the sparkifydb database, and all of the required tables that are defined in the _sql_queries.py_ script.

![](https://github.com/AmiriMc/Data_Engineering_Data_Modeling_with_Postgres/blob/master/StarSchema.png?raw=t)

## ETL Pipeline
The _etl.py_ script sets up the ETL pipeline. ETL (Extract, Transform, and Load) methods were used to populate the _songs_ and _artists_ tables from the data within the JSON song files (`data/song_data/`) and to populate the _users_ and _time_ tables from the JSON log files (`data/log_data/`). A `SELECT` query gathers the `song_id` and `artist_id` information based on the title, artist name, and song duration from the log file.

## Example Queries
Some useful example queries tested in Jupyter:
* Get total number of users: `SELECT COUNT(user_id) FROM users`
* Get total number of female 'F' (or male 'M') users: `SELECT COUNT(gender) FROM users WHERE gender = 'F'`
* Get year of oldest/newest ('MIN' or 'MAX') activity : `SELECT MIN(year) FROM time`
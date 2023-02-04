# Data Modeling with Appache Cassandra

## Introduction
A startup called Sparkify has been collecting on songs and user activity on their new music streaming app. Currently they have a directory of JSON logs on user activity, as well as a directory with JSON metadata on the songs in their app. Sparkify's analytics team is particularly interested in understanding what songs users are listening to. The task will be to create a Postgres database with tables designed to optimize queries on song play analysis. This includes creating a database schema and ETL pipeline.

## Database Schema
The Star schema is used for this project. There are several benefits for using the Star schema. These includes having denormalize tables, simplified queries, and fast aggregation of the data. The Star schema is usually less ideal for handling one-to-many or many-to-many relationships between the tables. Hence, the following tables are created to have only one-to-one relationships.

**Fact Table**

songplays - records in log data associated with song plays i.e. records with page NextSong
- songplay_id (int) Primary Key : ID for each songplay
- start_time (timestamp) : Start time of songplay session
- user_id (int) : User's ID
- level (varchar) : User's membership level {free | paid}
- song_id (varchar) : Song's ID
- artist_id (varchar) : Artist's ID
- session_id (int) : ID of user's current session
- location (varchar) : User's location
- user_agent (varchar) : User's software agent

**Dimension Tables**

users - users in the app
- user_id (int) : ID of user
- first_name (varchar) : User's first name
- last_name (varchar) : User's last name
- gender (varchar) : User's gender
- level (varchar) : User membership level {free | paid}

songs - songs in music database
- song_id (varchar) : Song's ID
- title (varchar) : Song's title
- artist_id (varchar) : Artist's ID
- year (int) : Year of song release
- duration (float) : Duration of song

artists - artists in music database
- artist_id (varchar) : Artist's ID
- name (varchar) : Artist's name
- location (varchar) : Artist's location
- latitude (float) : Latitude of artist's location
- longitude (float) : Longitude of artist's location

time - timestamps of records in songplays broken down into specific units
- start_time (timestamp) : Starting timestamp for songplay
- hour (int) : The hour of the songplay's start
- day (int) : The day of the songplay's start
- week (int) : The week of the songplay's start
- month (int) : The month of the songplay's start
- year (int) : The year of the songplay's start
- weekday (int) : The day of the week of the songplay's start


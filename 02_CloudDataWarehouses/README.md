# Data Warehouse with AWS Redshift

## Introduction
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

The task for this project will be to build an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms the data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.

The project will automate the creation of the AWS Redshift clusters using the AWS SDK boto3. The technique to create infrastructure (e.g. machines, users, roles, folders and processes) with code is known as Infrastructure-as-Code (IaC).

AWS Redshift is a cloud-managed Data Warehouse storage based on a modified version of postgresql. Redshift is a column-oriented storage and it is able to process the database on a column by column basis and perform aggregation operation on them, without the need to process the entire row. Redshift is also a Massively Parallel Processing (MPP) database, which allows for parallelization of a single query execution on multiple CPUs/machines.

## Database Schema
The Star schema is used for the analytics tables on the AWS Redshift cluster, since the schema optimizes queries on song play analysis. There are other benefits for using the Star schema. These includes having denormalize tables, simplified queries, and fast aggregation of the data. The Star schema is usually less ideal for handling one-to-many or many-to-many relationships between the tables. Hence, the following tables are created to have only one-to-one relationships. Below is a list of the analytics tables.

### Fact Table

**songplays:** records in log data associated with song plays i.e. records with page NextSong
- songplay_id BIGINT IDENTITY(0,1) PRIMARY KEY: : ID for each songplay
- start_time TIMESTAMP NOT NULL: Start time of songplay session
- user_id INT NOT NULL : User's ID
- level VARCHAR: User's membership level {free | paid}
- song_id VARCHAR: Song's ID
- artist_id VARCHAR: Artist's ID
- session_id VARCHAR: ID of user's current session
- location VARCHAR: User's location
- user_agent VARCHAR: User's software agent

###  Dimension Tables
**users:** users in the app
- user_id INT PRIMARY KEY: ID of user
- first_name VARCHAR: User's first name
- last_name VARCHAR: User's last name
- gender VARCHAR: User's gender
- level VARCHAR: User membership level {free | paid}


**songs:** songs in music database
- song_id VARCHAR PRIMARY KEY: Song's ID
- title VARCHAR: Song's title
- artist_id VARCHAR: Artist's ID
- year INT: Year of song release
- duration NUMERIC: Duration of song
- artists - artists in music database

**artists:** artists in music database
- artist_id VARCHAR PRIMARY KEY: Artist's ID
- name VARCHAR: Artist's name
- location VARCHAR: Artist's location
- latitude VARCHAR: Latitude of artist's location
- longitude VARCHAR: Longitude of artist's location


**time:** timestamps of records in songplays broken down into specific units
- start_time TIMESTAMP PRIMARY KEY: Starting timestamp for songplay
- hour INT: The hour of the songplay's start
- day INT: The day of the songplay's start
- week INT: The week of the songplay's start
- month INT: The month of the songplay's start
- year INT: The year of the songplay's start
- weekday INT: The day of the week of the songplay's start

Below is a list of the two staging tables created on the Redshift cluster.

**staging_events:** staging table for the JSON files in the log_data directory on S3
- artist VARCHAR
- auth VARCHAR
- firstNAME VARCHAR
- gender VARCHAR
- itemInSession (int)
- lastName VARCHAR
- length NUMERIC
- level VARCHAR
- location VARCHAR
- method VARCHAR
- page VARCHAR
- registration BIGINT
- sessionId INT
- song VARCHAR
- status INT
- ts BIGINT
- userAgent VARCHAR
- userId INT

**staging_songs:** staging table for the JSON files in the song_data directory on S3
- num_songs BIGINT
- artist_id VARCHAR
- artist_latitude VARCHAR
- artist_longitude VARCHAR
- artist_location VARCHAR
- artist_name VARCHAR
- song_id VARCHAR
- title VARCHAR
- duration NUMERIC
- year INT

### S3 (JSON Format)
There are two directories of JSON files.

**1.) song_data:**
JSON files in this directory contain song metadata. This dataset is a subset of the Million Song Dataset. The files are partitioned by the first three letters of each song's track ID. For example, here are filepaths to two files in this dataset.

```sh
song_data/A/B/C/TRABCEI128F424C983.json
song_data/A/A/B/TRAABJL12903CDCF1A.json
```

An example of what a single song file, TRAABJL12903CDCF1A.json, looks like.

```sh 
{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
```

**2.) log_data:** 
JSON files in this directory contain logs on user activity. These log datasets are generated using by this event simulator based on the songs in the dataset above, and they will simulate app activity logs from an imaginary music streaming app based on configuration settings. The log files in the dataset are partitioned by year and month. For example, here are filepaths to two files in this dataset.

- log_data/2018/11/2018-11-12-events.json
- log_data/2018/11/2018-11-13-events.json

An example of what log data looks like.
![alt text](https://github.com/ThomasWeikert/Data_Engineering_with_AWS/blob/main/02_CloudDataWarehouses/images/log-data.png)


**log_json_path.json:** A JSONPath file mapping the JSON elements in the log_data to the appropriate columns in the Redshuft staging table staging_events .

### ETL Pipeline
The ETL pipeline will load the JSON files in the log_data directory on S3 into a staging table staging_events using a JSONPath file log_json_path.json to map the JSON elements to the columns in the staging_events table. Next, the ETL pipeline will load the JSON files in the song_data directory on S3 into s a staging table staging_songs. Finally, the ETL pipeline will load the data from the staging tables and insert the appropriate data into the analytics tables: songplay, users, songs, artists and time .

### Repository Structure
- **create_cluster.py** : Python script to create the Redshift clusters using the AWS python SDK boto3
- **create_tables.py** : Python script to create the fact and dimension analytics tables on Redshift
- **delete_cluster.py** : Python script to delete the Redshift clusters using the AWS python SDK
- **etl.py** : Python script to run the ETL pipeline that will load the data from S3 into staging tables on Redshift. It will then load the data from the staging tables to the analytics tables on Redshift
- **query_data.py** : Script containing SQL test queries and results for song play analysis
- **sql_queries.py** : Script containing the SQL statements
- **dwh.cfg** : The configuration file
- **README.md** : A report outlining the summary of the project, instructions on running the Python scripts, and an explanation of the files in the repository. It also provides details on the database schema design as well as the ETL pipeline
- **images**: Folder containing images used in this readme


## How to Run
1.) Fill in the settings under the AWS and DWH tags in the configuration file dwh.cfg.

```sh 
[CLUSTER]
host =
db_name =
db_user =
db_password =
db_port =

[IAM_ROLE]
arn =

[S3]
log_data = 's3://udacity-dend/log_data'
log_jsonpath = 's3://udacity-dend/log_json_path.json'
song_data = 's3://udacity-dend/song_data'

[AWS]
key =
secret =

[DWH]
dwh_cluster_type = multi-node
dwh_num_nodes = 4
dwh_node_type = dc2.large
dwh_iam_role_name =
dwh_cluster_identifier =
dwh_db =
dwh_db_user =
dwh_db_password =
dwh_port = 5439
``` 

2.) In the main directory, run ```create_cluster.py``` to create the Redshift clusters using the AWS python SDK boto3.
```sh 
python create_cluster.py
```
3.) Run ```create_tables.py``` to connect to the database and create the staging and analytics tables mentioned in the database schema. Running the script will also update the settings under the CLUSTER and IAM_ROLE tags in the configuration file ```dwh.cfg``` .
```sh 
python create_tables.py 
```
4.) Run ```etl.py``` to load the data from S3 to the staging tables on Redshift, and then load the data from the staging tables to the analytics tables while still on Redshift.
```sh 
python etl.py
```
5.) Run ```query_data.py``` to execute basic SQL queries for song play analysis to test the database and the ETL pipeline.
```sh 
python query_data.py
```

6.) At the end of the project, you can delete the Redshift cluster by running ```delete_cluster.py```.
```sh 
python delete_cluster.py
```

### Sample Queries
Here are some basic examples of SQL queries for song play analysis and their results.

1.) Count staging songs
```sh
SELECT count(*) FROM staging_songs
```
Result:
```sh
(14896,)
```

2.) Count staging events
```sh
SELECT count(*) FROM staging_events
```
Result:
```sh
(8056,)
```

3.) Top 5 users
```sh
SELECT * FROM users LIMIT 5
```
Results:
```sh
(83, 'Stefany', 'White', 'F', None)
(15, 'Lily', 'Koch', 'F', None)
(81, 'Sienna', 'Colon', 'F', None)
(23, 'Morris', 'Gilmore', 'M', None)
(28, 'Brantley', 'West', 'M', None)
```

4.) Top 5 artists
```sh
SELECT * FROM artists LIMIT 5
```
Results
```sh
('ARAK1CO1187FB3F08C', 'Jaga Jazzist', '', None, None)
('ARSN5BN1187B98D0FA', 'Frameshift', '', None, None)
('ARS2SEI1187B993255', 'Slut', '', None, None)
('ARBR4UG1187B9B5A9D', 'Casper & The Cookies', '', None, None)
('AR1GYND1187B9A9CD3', 'Diesel Boy', 'Santa Rosa, California', '38.437730000000002', '-122.71241999999999')
```
5.) Top 5 songs
```sh
SELECT * FROM songs LIMIT 5
```
Results
```sh
('SOMWFVO12A8C134A7F', 'Who Threw The Whiskey In The Well', 'ARG3GZM1187B98EE7A', 2003, Decimal('178'))
('SOEXLIP12A8C133FF2', "He Don't Care", 'ARIMS5H1187FB3ECCD', 2000, Decimal('279'))
('SOBRYNJ12A81C20FFF', 'La Palma De Coco', 'ARRLMTZ1187B9AB6DD', 0, Decimal('152'))
('SOGCDYR12AC961854A', 'You And Your Heart', 'ARC8CQZ1187B98DECA', 2010, Decimal('196'))
('SOTCWTN12AB017EB37', 'The Rush (Long Time Coming) [Drop the Lime Remix]', 'ARP9ZS01187B9AA28F', 2006, Decimal('332'))
```

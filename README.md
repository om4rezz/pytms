# pytms

# activate the venv >> $ source venv/bin/activate

# install the requirements >> $ pip install -r requirements.txt

Data downloaded from API to MySQL tables have been done with the following parameters

<api_secret>  : w5a6tj96tbvq39u74wmtyamd

<zip_code> : 78701

<start_date> : 2020-11-11

<line_up_id> : USA-TX42500-X

<date_time> : Current date with time (ISO 8601) eg. 2020-11-11T09:30Z

# Download the data of theatre_movies >> 
localhost:5000/api/get_theatre_movies/2020-11-11/78701/w5a6tj96tbvq39u74wmtyamd

# Download the data of tv_airing_movies >> 
localhost:5000/api/get_tv_movies/USA-TX42500-X/2020-11-11T19%3A00Z/w5a6tj96tbvq39u74wmtyamd

# list movies based on genres >> 
localhost:5000/api/movies/theatre_movie/Horror/list 
OR
localhost:5000/api/movies/tv_movie/Horror/list

# Top genres >> 
localhost:5000/api/top_5_genres

======================================================

The MySQL database is called pytms
you may find its dump in the root directory with the name : pytms_database_dump.sql

======================================================

# NOTE:
This is my first time to use pandas lib and its dataframe. I covered it from an on-the-fly article.. It's amazing for real! Execuse me if i misused it. I gonna ramp myself up using series and dataframe of pandas.

======================================================

from flask import Blueprint
from .models import *
import requests
import pandas as pd

api = Blueprint('main', __name__, url_prefix='/api')


@api.route('/')
def main_index():
    return "Blueprint views.py Hello!"


@api.route('/get_theatre_movies/<string:startDate>/<string:zip>/<string:api_key>')
def get_theatre_movies(startDate, zip, api_key):
    print('==========================')
    print(startDate, zip, api_key)
    print('==========================')

    PARAMS = {
        'startDate': startDate,
        'zip': zip,
        'api_key': api_key
    }

    URL = 'http://data.tmsapi.com/v1.1/movies/showings'

    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    print('Length: %d' % len(data))
    TheatreMovie.insert_bulk(data)
    return "get_theatre_movies"


@api.route('/get_tv_movies/<string:lineupId>/<string:startDateTime>/<string:api_key>')
def get_tv_movies(lineupId, startDateTime, api_key):
    print('==========================')
    print(lineupId, startDateTime, api_key)
    print('==========================')

    PARAMS = {
        'lineupId': lineupId,
        'startDateTime': startDateTime,
        'api_key': api_key
    }

    URL = 'http://data.tmsapi.com/v1.1/movies/airings'

    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    print('Length: %d' % len(data))
    TVMovie.insert_bulk(data)
    return "get_tv_movies"


@api.route('/movies/<string:type>/<string:genre>/list')
def list_movies_based_on_genre(type, genre):
    if type == 'theatre_movie':
        sql_query = 'select theatre_movie.id, theatre_movie.title from theatre_movie, genre, theatre_movie_genre  where  theatre_movie.id = theatre_movie_genre.theatre_movie_id and genre.id = theatre_movie_genre.genre_id and genre.title = \'%s\'' % genre
    else:
        sql_query = 'select tv_movie.id, tv_movie.title from tv_movie, genre, tv_movie_genre  where  tv_movie.id = tv_movie_genre.tv_movie_id and genre.id = tv_movie_genre.genre_id and genre.title = \'%s\'' % genre

    print(sql_query)
    df = pd.read_sql_query(sql_query, db.engine.connect().connection)
    print(str(df))

    return "Dataframe instance is printed in the console."


@api.route('/top_5_genres')
def list_top_5_genres():
    sql_query = """select theatre_movie.id, theatre_movie.title, theatre_movie.release_year, 
    GROUP_CONCAT(genre.title SEPARATOR ', ') genres 
    from theatre_movie 
    LEFT JOIN theatre_movie_genre 
    ON theatre_movie.id = theatre_movie_genre.theatre_movie_id 
    LEFT JOIN genre 
    ON theatre_movie_genre.genre_id = genre.id 
    GROUP BY theatre_movie.id"""

    df = pd.read_sql_query(sql_query, db.engine.connect().connection)
    print(df['genres'].value_counts().head(5))

    return "Dataframe instance is printed in the console."

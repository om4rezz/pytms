from .extensions import db
from .helper_functions import set_movie_genres, set_movie_theatres, insert_related_genres, insert_related_theatres

theatre_movie_genre = db.Table(
    'theatre_movie_genre',
    db.Column('theatre_movie_id', db.Integer, db.ForeignKey('theatre_movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
)

tv_movie_genre = db.Table(
    'tv_movie_genre',
    db.Column('tv_movie_id', db.Integer, db.ForeignKey('tv_movie.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
)

theatre_movie_theatre = db.Table(
    'theatre_movie_theatre',
    db.Column('theatre_movie_id', db.Integer, db.ForeignKey('theatre_movie.id'), primary_key=True),
    db.Column('theatre_id', db.Integer, db.ForeignKey('theatre.id'), primary_key=True),
)


class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    theatre_movies = db.relationship('TheatreMovie', secondary=theatre_movie_genre, backref='theatre_genres')
    tv_movies = db.relationship('TVMovie', secondary=tv_movie_genre, backref='tv_genres')


class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    movies = db.relationship('TheatreMovie', secondary=theatre_movie_theatre, backref='movie_theatres')


class TheatreMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    release_year = db.Column(db.Integer)
    description = db.Column(db.Text)
    genres = db.relationship('Genre', secondary=theatre_movie_genre, backref='genre_movies')
    theatres = db.relationship('Theatre', secondary=theatre_movie_theatre, backref='related_movies')

    @staticmethod
    def insert_bulk(bulk_of_movies):
        for movie in bulk_of_movies:
            # Insert related theatres if not existed
            insert_related_theatres(movie)

            # Insert related genres if not existed
            insert_related_genres(movie, 'theatre_movie')

            # insert theatre movie
            theatre_movie = TheatreMovie(
                title=movie['title'],
                release_year=movie['releaseYear'] if 'releaseYear' in movie.keys() else None,
                description=movie['longDescription'] if 'longDescription' in movie.keys() else None,
            )

            db.session.add(theatre_movie)
            db.session.commit()

            # add genres and theatres to movie
            if 'genres' in movie.keys():
                set_movie_genres(theatre_movie, movie['genres'])
            set_movie_theatres(theatre_movie, movie['showtimes'])


class TVMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    release_year = db.Column(db.Integer)
    description = db.Column(db.Text)
    channel = db.Column(db.String(5))
    genres = db.relationship('Genre', secondary=tv_movie_genre, backref='movies')

    @staticmethod
    def insert_bulk(bulk_of_movies):
        for movie in bulk_of_movies:
            # Insert related genres if not existed
            insert_related_genres(movie, 'tv_movie')

            # insert theatre movie
            tv_movie = TVMovie(
                title=movie['program']['title'],
                release_year=movie['program']['releaseYear'] if 'releaseYear' in movie['program'].keys() else None,
                description=movie['program']['longDescription'] if 'longDescription' in movie['program'].keys() else None,
                channel=movie['station']['channel']
            )

            db.session.add(tv_movie)
            db.session.commit()

            # add genres and theatres to movie
            if 'genres' in movie['program'].keys():
                set_movie_genres(tv_movie, movie['program']['genres'])

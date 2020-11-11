from . import models
from .extensions import db


def set_movie_genres(movie, genres):
    for g in genres:
        movie.genres.append(models.Genre.query.filter_by(title=g).first())
        db.session.commit()


def set_movie_theatres(movie, showtimes):
    for item in showtimes:
        movie.theatres.append(models.Theatre.query.filter_by(name=item['theatre']['name']).first())
        db.session.commit()


def insert_related_genres(movie, movie_type):
    if movie_type == 'theatre_movie' and 'genres' in movie.keys():
        genres = movie['genres']
    elif movie_type == 'tv_movie' and 'genres' in movie['program'].keys():
        genres = movie['program']['genres']
    else:
        return

    for item in genres:
        g = models.Genre.query.filter_by(title=item).first()
        if g:
            pass
        else:
            g = models.Genre(title=item)
            db.session.add(g)
            db.session.commit()


def insert_related_theatres(movie):
    for item in movie['showtimes']:
        th = models.Theatre.query.filter_by(name=item['theatre']['name']).first()
        if th:
            pass
        else:
            th = models.Theatre(name=item['theatre']['name'])
            db.session.add(th)
            db.session.commit()

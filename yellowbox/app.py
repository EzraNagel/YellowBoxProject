import os
import sys
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
import json

from sqlalchemy import *


# Database credentials
user = 'yellowbox_user'
password = 'password'
host = 'localhost'
port = '3306'
database = 'yellowbox_db'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(BigInteger, primary_key=True)
    belongs_to_collection = db.Column(Text, nullable=True)
    budget = db.Column(BigInteger, nullable=True)
    genres = db.Column(Text, nullable=True)
    homepage = db.Column(String(255), nullable=True)
    imdb_id = db.Column(String(10), nullable=True)
    original_language = db.Column(String(2), nullable=False)
    original_title = db.Column(String(255), nullable=False)
    overview = db.Column(Text, nullable=True)
    popularity = db.Column(Float, nullable=True)
    poster_path = db.Column(String(255), nullable=True)
    production_companies = db.Column(Text, nullable=True)
    release_date = db.Column(String(10), nullable=True)
    revenue = db.Column(BigInteger, nullable=True)
    runtime = db.Column(Integer, nullable=True)
    spoken_languages = db.Column(Text, nullable=True)
    tagline = db.Column(Text, nullable=True)
    title = db.Column(String(255), nullable=False)
    vote_average = db.Column(Float, nullable=True)
    vote_count = db.Column(Integer, nullable=True)

    def __repr__(self):
        return f"<Movie(title={self.title}, id={self.id})>"


class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    movieId = db.Column(BigInteger, nullable=True)
    rating = db.Column(Float, nullable=True)
    timestamp = db.Column(BigInteger, nullable=True)

    def __repr__(self):
        return f"<Rating(movieId={self.movieId}, rating={self.rating})>"


class Credit(db.Model):
    __tablename__ = 'credits'
    
    id = db.Column(BigInteger, primary_key=True)
    cast = db.Column(Text, nullable=True)
    crew = db.Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Credit(id={self.id})>"


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(BigInteger, primary_key=True)
    username = db.Column(String(50), nullable=False)
    password = db.Column(String(255), nullable=False)
    email = db.Column(String(100), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id})>"


class Disk(db.Model):
    __tablename__ = "disks"

    id = db.Column(BigInteger, primary_key=True)
    movieId = db.Column(BigInteger, nullable=False)
    location = db.Column(Integer, nullable=True)
    condition = db.Column(String(50), nullable=True)

    def __repr__(self):
        return f"<Disk(id={self.id})>"


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(BigInteger, primary_key=True)
    movieId = db.Column(BigInteger, nullable=False)
    customerId = db.Column(BigInteger, nullable=False)
    checkoutDate = db.Column(BigInteger, nullable=False)
    returnDate = db.Column(BigInteger, nullable=False)
    rating = db.Column(Float, nullable=True)
    review = db.Column(Text, nullable=True)

    def __repr__(self):
        return f"<Order(id={self.id})>"

class Kiosk(db.Model):
    __tablename__ = 'kiosks'

    id = db.Column(BigInteger, primary_key=True)
    address = db.Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Kiosk(id={self.id}, address={self.address})>"

@app.route('/')
def base():

    top_movies = db.session.query(
        Movie,
        db.func.avg(Rating.rating).label('average_rating')
    ).join(Rating, Movie.id == Rating.movieId, isouter=True)
    top_movies = top_movies.group_by(Movie.id).order_by(db.desc('average_rating')).limit(20).all()
    
    collections = db.session.query(Movie.belongs_to_collection).distinct().all()
    
    parsed_collections = []
    for collection_json, in collections:
        if collection_json:
            try:
                collection_data = json.loads(collection_json.replace("'", "\""))
                parsed_collections.append({
                    'name': collection_data.get('name'),
                    'poster_path': collection_data.get('poster_path')
                })
            except json.JSONDecodeError:
                pass
    
                
    return render_template('base.html', movies=top_movies, collections=parsed_collections)



@app.route('/movies')
def movies():
    movie_list = Movie.query.all()
    return render_template('movies.html', movies=movie_list)

@app.route('/movies_search_results', methods=['GET'])
def movies_search_results():
    title = request.args.get('title', '')
    run_time_min = request.args.get('run_time_min', type=int)
    run_time_max = request.args.get('run_time_max', type=int)
    popularity_min = request.args.get('popularity_min', type=float)
    popularity_max = request.args.get('popularity_max', type=float)
    release_date_min = request.args.get('release_date_min', type=str)
    release_date_max = request.args.get('release_date_max', type=str)
    rating_min = request.args.get('rating_min', type=float)
    rating_max = request.args.get('rating_max', type=float)

    query = db.session.query(Movie)

    if title:
        query = query.filter(Movie.title.ilike(f'%{title}%'))
    if run_time_min is not None and run_time_max is not None:
        query = query.filter(Movie.runtime.between(run_time_min, run_time_max))
    if popularity_min is not None and popularity_max is not None:
        query = query.filter(Movie.popularity.between(popularity_min, popularity_max))
    if release_date_min and release_date_max:
        query = query.filter(Movie.release_date.between(release_date_min, release_date_max))
    if rating_min is not None and rating_max is not None:
        query = query.filter(Movie.vote_average.between(rating_min, rating_max))

    movies = query.all()

    return render_template('movies_search_results.html', movies=movies)




@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = Movie.query.get_or_404(movie_id)  
    return render_template('movie_detail.html', movie=movie)

@app.route('/kiosks')
def kiosks():


    return render_template('kiosks.html')

@app.route('/DVDs')
def DVDs():


    return render_template('DVDs.html')

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)

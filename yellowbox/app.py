import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, JSON, Text, Date, Float, create_engine

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)


user = 'user'
password = 'password'
host = 'localhost'
port = '3306'
database = 'yellowboxdb'

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(BigInteger, primary_key=True)
    belongs_to_collection = db.Column(JSON, nullable=True)
    budget = db.Column(BigInteger, nullable=True)
    genres = db.Column(JSON, nullable=True)
    homepage = db.Column(db.String, nullable=True)
    imdb_id = db.Column(db.String(10), nullable=True)
    original_language = db.Column(db.String(2), nullable=False)
    original_title = db.Column(db.String, nullable=False)
    overview = db.Column(Text, nullable=True)
    popularity = db.Column(Float, nullable=True)
    poster_path = db.Column(db.String, nullable=True)
    production_companies = db.Column(JSON, nullable=True)
    release_date = db.Column(Date, nullable=True)
    revenue = db.Column(BigInteger, nullable=True)
    runtime = db.Column(db.Integer, nullable=True)
    spoken_languages = db.Column(JSON, nullable=True)
    tagline = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=False)
    vote_average = db.Column(Float, nullable=True)
    vote_count = db.Column(db.Integer, nullable=True)

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
    cast = db.Column(JSON, nullable=True)
    crew = db.Column(JSON, nullable = True)
    
    def __repr__(self):
        return f"<Credit(movie_id={self.id})>"


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

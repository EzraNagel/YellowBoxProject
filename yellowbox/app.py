import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import BigInteger, JSON, Text, Date

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
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
    popularity = db.Column(db.Float, nullable=True)
    poster_path = db.Column(db.String, nullable=True)
    production_companies = db.Column(JSON, nullable=True)
    release_date = db.Column(Date, nullable=True)
    revenue = db.Column(BigInteger, nullable=True)
    runtime = db.Column(db.Integer, nullable=True)
    spoken_languages = db.Column(JSON, nullable=True)
    tagline = db.Column(db.String, nullable=True)
    title = db.Column(db.String, nullable=False)
    vote_average = db.Column(db.Float, nullable=True)
    vote_count = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"<Movie(title={self.title}, id={self.id})>"
    
class Rating(db.Model):
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    movieId = db.Column(BigInteger, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.BigInteger, nullable=True)

    def __repr__(self):
        return f"<Rating(movieId={self.movieId}, userId={self.userId})>"

class Credit(db.Model):
    __tablename__ = 'credits'
    
    id = db.Column(BigInteger, primary_key=True)
    cast = db.Column(JSON, nullable=True)
    crew = db.Column(JSON, nullable = True)
    
    def __repr__(self):
        return f"<Credit(movieId={self.movieId})>"

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(BigInteger, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"User(id={self.id})>"

class Disk(db.Model):
    __tablename__ = "disks"

    id = db.Column(BigInteger, primary_key=True)
    movieId = db.Column(BigInteger, nullable=False)
    location = db.Column(db.Integer, nullable=True)
    condition = username = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<Disk(id={self.id})>"

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(BigInteger, primary_key=True)
    movieId = db.Column(BigInteger, nullable=False)
    customerId = db.Column(BigInteger, nullable=False)
    checkoutDate = db.Column(db.BigInteger, nullable=False)
    returnDate = db.Column(db.BigInteger, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    review = db.Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Order(id={self.id})>"

@app.route('/')
def base():

    return render_template('base.html')

@app.route('/movies')
def movies():

    return render_template('movies.html')

@app.route('/kiosks')
def kiosks():

    return render_template('kiosks.html')

@app.route('/DVDs')
def DVDs():

    return render_template('DVDs.html')

if __name__ == "__main__":
    app.run(debug=True)
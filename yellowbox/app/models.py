from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, JSON, Text, Date, Float, String, Integer
from datetime import datetime

from app import db

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    belongs_to_collection = db.Column(Text, nullable=True)
    budget = db.Column(BigInteger, nullable=True)
    genres = db.Column(Text, nullable=True)
    homepage = db.Column(String(255), nullable=True)
    imdb_id = db.Column(String(10), nullable=True)
    original_language = db.Column(String(2), nullable=True)
    original_title = db.Column(String(255), nullable=True)
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
    
    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    movieId = db.Column(BigInteger, nullable=False)  
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
        return f"ID(id={self.id})>"
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(BigInteger, primary_key=True)
    username = db.Column(String(255), nullable=False)
    password = db.Column(String(255), nullable=False)
    email = db.Column(String(255), nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class Disk(db.Model):
    __tablename__ = 'disks'

    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    movieId = db.Column(BigInteger, nullable=False)
    kiosk_id = db.Column(Integer, nullable=True)
    condition = db.Column(String(50), nullable=True)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Disk(id={self.id}, movieId={self.movieId}, location={self.location}, condition={self.condition})>"


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(BigInteger, primary_key=True)
    movieId = db.Column(BigInteger, nullable=False)
    customerId = db.Column(BigInteger, nullable=False)
    checkoutDate = db.Column(BigInteger, nullable=False)
    returnDate = db.Column(BigInteger, nullable=True)
    rating = db.Column(Float, nullable=True)
    review = db.Column(Text, nullable=True)

    def __repr__(self):
        return f"<Order(id={self.id}, movieId={self.movieId}, customerId={self.customerId})>"


class Kiosk(db.Model):
    __tablename__ = 'kiosks'

    id = db.Column(BigInteger, primary_key=True)
    address = db.Column(String(255), nullable=False)

    def __repr__(self):
        return f"<Kiosk(id={self.id}, address={self.address})>"
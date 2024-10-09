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


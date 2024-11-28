from flask import render_template, json, session, request, redirect
import json
import sys
from . import base
from app.models import db, Movie, User
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange


@base.route('/')
def home():

    top_movies = db.session.query(
        Movie
    ).order_by(db.desc(Movie.vote_average)).limit(20).all()

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

    return render_template('base/home.html', movies=top_movies, collections=parsed_collections)

@base.route("/login", methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        login_error = None

        user = db.session.query(User).filter_by(username=username).first()

        if user and user.password:
            session['logged_in'] = True
            session['userID'] = user.id
            session['username'] = user.username
            session['email'] = user.email

            return redirect('/')
        else:
            login_error = 'Invalid username or password.'

        return render_template('base/login.html', login_error=login_error)

    return render_template('base/login.html')


@base.route('/logout')
def logout():
    session.clear()
    return redirect('/')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=10)], render_kw={"placeholder": "Rating (1-10)"})
    review_text = TextAreaField('Review', validators=[DataRequired()], render_kw={"placeholder": "Leave a review..."})
    submit = SubmitField('Submit Review')
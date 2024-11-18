from flask import render_template, json
import json
from . import base
from app.models import db, Movie


@base.route('/')
def base():

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
from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.sql import func
from datetime import datetime
from . import movies
from app.models import db, Movie, Disk, Kiosk, Order
import json

@movies.route('/view')
def movies_view():
    movie_list = Movie.query.all()
    return render_template('movies/view.html', movies=movie_list)

@movies.route('/search', methods=['GET', 'POST'])
def search():
    movies = []
    if request.method == 'GET':
        title = request.args.get('title')
        run_time_min = request.args.get('run_time_min')
        run_time_max = request.args.get('run_time_max')
        popularity_min = request.args.get('popularity_min')
        popularity_max = request.args.get('popularity_max')
        release_date_min = request.args.get('release_date_min')
        release_date_max = request.args.get('release_date_max')
        rating_min = request.args.get('rating_min')
        rating_max = request.args.get('rating_max')

        query = db.session.query(Movie)

        if title:
            query = query.filter(Movie.title.ilike(f'%{title}%'))
        if run_time_min:
            query = query.filter(Movie.runtime >= int(run_time_min))
        if run_time_max:
            query = query.filter(Movie.runtime <= int(run_time_max))
        if popularity_min:
            query = query.filter(Movie.popularity >= float(popularity_min))
        if popularity_max:
            query = query.filter(Movie.popularity <= float(popularity_max))
        if release_date_min:
            query = query.filter(Movie.release_date >= release_date_min)
        if release_date_max:
            query = query.filter(Movie.release_date <= release_date_max)
        if rating_min:
            query = query.filter(Movie.vote_average >= float(rating_min))
        if rating_max:
            query = query.filter(Movie.vote_average <= float(rating_max))

        movies = query.all()

    return render_template('movies/search.html', movies=movies)

@movies.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    
    if request.method == 'POST':
        movie.title = request.form.get('title')
        movie.overview = request.form.get('overview')
        movie.release_date = request.form.get('release_date')
        movie.budget = request.form.get('budget', type=int)
        movie.revenue = request.form.get('revenue', type=int)
        movie.runtime = request.form.get('runtime', type=int)
        movie.vote_average = request.form.get('vote_average', type=float)
        movie.vote_count = request.form.get('vote_count', type=int)
        movie.genres = request.form.get('genres')
        movie.original_language = request.form.get('original_language')
        movie.poster_path = request.form.get('poster_path')
        movie.belongs_to_collection = request.form.get('belongs_to_collection')
        movie.homepage = request.form.get('homepage')
        movie.imdb_id = request.form.get('imdb_id')
        movie.popularity = request.form.get('popularity', type=float)
        movie.spoken_languages = request.form.get('spoken_languages')
        movie.tagline = request.form.get('tagline')
        movie.production_companies = request.form.get('production_companies')

        db.session.commit()

        return redirect(url_for('movies.movie_detail', movie_id=movie.id))
    
    return render_template('movies/edit_movie.html', movie=movie)


@movies.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form.get('title')
        overview = request.form.get('overview')
        release_date = request.form.get('release_date')
        budget = request.form.get('budget', type=int)
        revenue = request.form.get('revenue', type=int)
        runtime = request.form.get('runtime', type=int)
        vote_average = request.form.get('vote_average', type=float)
        vote_count = request.form.get('vote_count', type=int)
        genres = request.form.get('genres')
        original_language = request.form.get('original_language')
        poster_path = request.form.get('poster_path')
        belongs_to_collection = request.form.get('belongs_to_collection')
        homepage = request.form.get('homepage')
        imdb_id = request.form.get('imdb_id')
        popularity = request.form.get('popularity', type=float)
        spoken_languages = request.form.get('spoken_languages')
        tagline = request.form.get('tagline')
        production_companies = request.form.get('production_companies')

        new_movie = Movie(
            title=title,
            overview=overview,
            release_date=release_date,
            budget=budget,
            revenue=revenue,
            runtime=runtime,
            vote_average=vote_average,
            vote_count=vote_count,
            genres=genres,
            original_language=original_language,
            poster_path=poster_path,
            belongs_to_collection=belongs_to_collection,
            homepage=homepage,
            imdb_id=imdb_id,
            popularity=popularity,
            spoken_languages=spoken_languages,
            tagline=tagline,
            production_companies=production_companies
        )

        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('movies.movies'))

    return render_template('movies/add_movie.html')


@movies.route('/collection_items')
def collection_items():
    collection_name = request.args.get('collection_name')
    
    movies = db.session.query(Movie).filter(Movie.belongs_to_collection.contains(collection_name)).all()

    
    return render_template('movies/collection_items.html', movies=movies)
    
    
@movies.route('/movies_search_results', methods=['GET'])
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
    elif run_time_min is not None:
        query = query.filter(Movie.runtime >= run_time_min)
    elif run_time_max is not None:
        query = query.filter(Movie.runtime <= run_time_max)
    if popularity_min is not None and popularity_max is not None:
        query = query.filter(Movie.popularity.between(popularity_min, popularity_max))
    elif popularity_min is not None:
        query = query.filter(Movie.popularity >= popularity_min)
    elif popularity_max is not None:
        query = query.filter(Movie.popularity <= popularity_max)
    if release_date_min or release_date_max:
        if release_date_min and release_date_max:
            query = query.filter(Movie.release_date.between(release_date_min, release_date_max))
        elif release_date_min:
            query = query.filter(Movie.release_date >= release_date_min)
        elif release_date_max:
            query = query.filter(Movie.release_date <= release_date_max)
    if rating_min is not None and rating_max is not None:
        query = query.filter(Movie.vote_average.between(rating_min, rating_max))
    elif rating_min is not None:
        query = query.filter(Movie.vote_average >= rating_min)
    elif rating_max is not None:
        query = query.filter(Movie.vote_average <= rating_max)

    movies = query.all()

    return render_template('movies/movies_search_results.html', movies=movies)


@movies.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = db.session.query(Movie).get(movie_id)
    
    avg_rating = db.session.query(func.avg(Order.rating)).filter(Order.movieId == movie_id).scalar()
    avg_rating = round(avg_rating, 2) if avg_rating else "No ratings yet"
    
    reviews = db.session.query(Order).filter(Order.movieId == movie_id).all()
    print(reviews)

    available_disks = db.session.query(Disk, Kiosk.address).join(Kiosk, Kiosk.id == Disk.kiosk_id).filter(Disk.movieId == movie_id, Disk.status == False).all()

    return render_template('movies/movie_detail.html', movie=movie, avg_rating=avg_rating, available_disks=available_disks, reviews = reviews)


@movies.app_template_filter('datetimeformat')
def datetimeformat(value):
    if value:
        return datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
    return 'N/A'

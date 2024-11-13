import os
import sys
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import json
from sqlalchemy import *
from sqlalchemy import BigInteger, JSON, Text, Date, Float



# Database credentials
user = 'yellowbox_user'
password = 'password'
host = 'localhost'
port = '3306'
database = 'yellowbox_db'

app = Flask(__name__)

app.secret_key = os.urandom(24)


app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

## Database Table Models

class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
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
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
        return f"ID(id={self.id})>"
    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(BigInteger, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f"User(id={self.id})>"


class Disk(db.Model):
    __tablename__ = "disks"

    id = db.Column(BigInteger, primary_key=True, autoincrement=True)
    movieId = db.Column(BigInteger, nullable=False)
    location = db.Column(Integer, nullable=True)
    condition = db.Column(String(50), nullable=True)

    def __repr__(self):
        return f"<Disk(id={self.id}, movieId={self.movieId}, location={self.location}, condition={self.condition})>"


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


## App routes

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
    
                
    return render_template('home.html', movies=top_movies, collections=parsed_collections)


@app.route('/movies')
def movies():
    movie_list = Movie.query.all()
    return render_template('movies.html', movies=movie_list)


@app.route('/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
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

        return redirect(url_for('movie_detail', movie_id=movie.id))
    
    return render_template('edit_movie.html', movie=movie)


@app.route('/add_movie', methods=['GET', 'POST'])
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

        return redirect(url_for('movies'))

    return render_template('add_movie.html')


@app.route('/collection_items')
def collection_items():
    collection_name = request.args.get('collection_name')
    
    movies = db.session.query(Movie).filter(Movie.belongs_to_collection.contains(collection_name)).all()

    
    return render_template('collection_items.html', movies=movies)
    
    
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

    kiosks = db.session.query(Kiosk).all()
    return render_template('kiosks.html', kiosks=kiosks)

@app.route('/kiosk/<int:kiosk_id>')
def kiosk_disks(kiosk_id):
    kiosk = db.session.query(Kiosk).get(kiosk_id)
    if kiosk is None:
        flash("Kiosk not found.")
        return redirect(url_for('kiosks'))

    disks = db.session.query(Disk.id, Disk.condition, Movie.title).join(Movie, Disk.movieId == Movie.id).filter(Disk.location == kiosk_id).all()

    return render_template('kiosk_disks.html', kiosk=kiosk, disks=disks)


# This would be connected to a button next each disks on the kiosk disk page that would pass the discs id to remove it
# but for some reason the ids aren't being assigned when they are added so it doesnt work
@app.route('/remove_disk/<int:disk_id>', methods=['POST'])
def remove_disk(disk_id):
    disk = Disk.query.get(disk_id)
    db.session.delete(disk)
    db.session.commit()
    return redirect(url_for('kiosk_disks', kiosk_id=disk.location))


@app.route('/DVDs')
def DVDs():
    condition_options = ['New', 'Good', 'Fair', 'Poor']
    disks = db.session.query(Disk.id, Disk.condition, Movie.title, Kiosk.address).join(Movie, Disk.movieId == Movie.id).join(Kiosk, Disk.location == Kiosk.id).all()
    movies = db.session.query(Movie).all()
    kiosks = db.session.query(Kiosk).all()
    
    return render_template('DVDs.html', disks = disks, movies=movies, kiosks=kiosks, condition_options=condition_options)


@app.route('/add_disk', methods=['POST'])
def add_disk():
    movie_id = request.form.get('movieId')
    location_id = request.form.get('location', None)
    condition = request.form.get('condition', None)

    new_disk = Disk(
        movieId=int(movie_id),
        location=int(location_id) if location_id else None,
        condition=condition
    )
    

    db.session.add(new_disk)
    db.session.commit()

    movie = db.session.query(Movie).filter_by(id=movie_id).first()
    kiosk = db.session.query(Kiosk).filter_by(id=location_id).first()
    
    return redirect(url_for('success_add', movie_title=movie.title, kiosk_address=kiosk.address))


@app.route('/success_add')
def success_add():
    movie_title = request.args.get('movie_title')
    location = request.args.get('kiosk_address')

    return render_template('success_add.html', movie_title=movie_title, location=location)


@app.route('/new_customer', methods=['GET', 'POST'])
def new_customer():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if not username or not password or not email:
            return "All fields are required", 400

        new_user = User(username=username, password=password, email=email)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('base'))
        except Exception as e:
            db.session.rollback()
            print(f"Error adding customer: {e}")
            return "There was an issue adding the customer"

    return render_template('new_customer.html')

@app.route('/update_customer/<int:customer_id>', methods=['GET', 'POST'])
def update_customer(customer_id):
    customer = User.query.get_or_404(customer_id)

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        if not username or not email:
            return "Username and email are required", 400

        customer.username = username
        customer.password = password
        customer.email = email

        try:
            db.session.commit()
            return redirect(url_for('base'))
        except Exception as e:
            db.session.rollback()
            print(f"Error updating customer: {e}")
            return "There was an issue updating the customer", 500

    return render_template('update_customer.html', customer=customer)


@app.route('/view_customer/<int:customer_id>', methods=['GET'])
def view_customer(customer_id):
    customer = User.query.get_or_404(customer_id)

    return render_template('view_customer.html', customer=customer)


if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
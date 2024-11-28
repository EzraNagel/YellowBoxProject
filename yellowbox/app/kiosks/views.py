from flask import Flask, render_template, request, redirect, url_for
from . import kiosks
from app.models import db, Kiosk, Disk, Movie 
from datetime import datetime


@kiosks.route('/kiosks')
def kiosks_view():

    kiosks = db.session.query(Kiosk).all()
    return render_template('kiosks/kiosks.html', kiosks=kiosks)

@kiosks.route('/kiosk/<int:kiosk_id>')
def kiosk_disks(kiosk_id):
    kiosk = db.session.query(Kiosk).get(kiosk_id)
    if kiosk is None:
        return redirect(url_for('kiosks'))

    disks = db.session.query(Disk.id, Disk.condition, Movie.title).join(Movie, Disk.movieId == Movie.id).filter(Disk.kiosk_id == kiosk_id).all()

    return render_template('kiosks/kiosk_disks.html', kiosk=kiosk, disks=disks)


@kiosks.route('/remove_disk/<int:disk_id>', methods=['POST'])
def remove_disk(disk_id):
    disk = Disk.query.get(disk_id)
    db.session.delete(disk)
    db.session.commit()
    return redirect(url_for('kiosks.kiosks_view', kiosk_id=disk.location))


@kiosks.route('/add_disk', methods=['POST'])
def add_disk():
    movie_id = request.form.get('movieId')
    location_id = request.form.get('location', None)
    condition = request.form.get('condition', None)

    new_disk = Disk(
        movieId=int(movie_id),
        kiosk_id=int(location_id) if location_id else None,
        condition=condition
    )
    

    db.session.add(new_disk)
    db.session.commit()

    movie = db.session.query(Movie).filter_by(id=movie_id).first()
    kiosk = db.session.query(Kiosk).filter_by(id=location_id).first()
    
    return redirect(url_for('kiosks.success_add', movie_title=movie.title, kiosk_address=kiosk.address))


@kiosks.route('/success_add')
def success_add():
    movie_title = request.args.get('movie_title')
    location = request.args.get('kiosk_address')

    return render_template('kiosks/success_add.html', movie_title=movie_title, location=location)

@kiosks.route('/DVDs')
def DVDs():
    condition_options = ['New', 'Good', 'Fair', 'Poor']
    disks = db.session.query(Disk, Movie.title, Kiosk.address).join(Movie, Disk.movieId == Movie.id).join(Kiosk, Disk.kiosk_id == Kiosk.id).all()
    movies = db.session.query(Movie).all()
    kiosks = db.session.query(Kiosk).all()
    
    return render_template('kiosks/DVDs.html', disks = disks, movies=movies, kiosks=kiosks, condition_options=condition_options)

@kiosks.app_template_filter('datetimeformat') 
def datetimeformat(value):
    if value:
        return datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
    return 'N/A'
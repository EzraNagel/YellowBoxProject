from flask import Blueprint, render_template, request, redirect, url_for, session
from . import orders
from app.models import db, Order, Movie, User, Disk, Kiosk
from datetime import datetime


@orders.route('/rental_history/<int:movie_id>')
def rental_history(movie_id):
    rentals = db.session.query(
        Order,
        User.id,
        Kiosk.address
    ).join(User, Order.customerId == User.id) \
     .join(Kiosk, Order.movieId == movie_id) \
     .filter(Order.movieId == movie_id).all()

    movie = Movie.query.get_or_404(movie_id)
    return render_template('orders/rental_history.html', rentals=rentals, movie=movie)

from flask import request, redirect, url_for
from datetime import datetime

@orders.route('/rent_movie/<int:movie_id>', methods=['POST'])
def rent_movie(movie_id):
    customer_id = request.form.get('customer_id')
    disc_id = request.form.get('disc_id')  

    disk = db.session.query(Disk).filter_by(id=disc_id, movieId=movie_id, status='available').first()

    if not disk:
        return redirect(url_for('DVDs'))

    new_order = Order(
        movieId=movie_id,
        customerId=customer_id,
        checkoutDate=int(datetime.utcnow().timestamp()),
        returnDate=None, 
    )

    db.session.add(new_order)
    db.session.commit()

    disk.status = True  
    db.session.commit()

    return redirect(url_for('orders.orders'))


@orders.route('/return_movie/<int:order_id>', methods=['POST'])
def return_movie(order_id):
    order = Order.query.get_or_404(order_id)
    order.returnDate = int(datetime.utcnow().timestamp())

    db.session.commit()
    
    return redirect(url_for('customers.view_customer', customer_id=order.customerId))


@orders.route('/orders', methods=['GET'])
def orders():
    user_id = session.get('userID')
    if not user_id:
        return redirect('/login')

    orders = Order.query.filter_by(customerId=user_id).all()

    for order in orders:
        order.movie = Movie.query.get(order.movieId)

    return render_template('orders/orders.html', orders=orders)
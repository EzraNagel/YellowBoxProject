from flask import Blueprint, render_template, request, redirect, url_for, session
from . import orders
from app.models import db, Order, Movie, User, Disk, Kiosk
from datetime import datetime
from ..base.views import ReviewForm


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

@orders.route('/rent_movie/<int:movie_id>', methods=['POST'])
def rent_movie(movie_id):
    customer_id = session.get('userID')  
    
    if not customer_id:
        return redirect(url_for('base.login'))   
     
    disk_id = request.form.get('disk_id')  

    disk = db.session.query(Disk).filter_by(id=disk_id, movieId=movie_id, status=False).first()

    if not disk:
        return redirect(url_for('kiosks.DVDs'))

    new_order = Order(
        movieId=movie_id,
        disk_id=disk.id,
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
    disk = Disk.query.get_or_404(order.disk_id)
    
    disk.status = False

    db.session.commit()
    
    return redirect(url_for('orders.orders', customer_id=order.customerId))

@orders.route('/order_page/<int:order_id>', methods=['GET', 'POST'])
def order_page(order_id):
    order = Order.query.get_or_404(order_id)
    movie = Movie.query.get_or_404(order.movieId)
    form = ReviewForm()

    if form.validate_on_submit():
        order.rating = form.rating.data
        order.review = form.review_text.data
        db.session.commit()
        return redirect(url_for('orders.orders'))

    return render_template('orders/order_page.html', order=order, movie=movie, form=form)

@orders.route('/orders', methods=['GET'])
def orders():
    user_id = request.args.get('user_id')
    if not user_id:
        user_id = session.get('userID')
    if not user_id:
        return redirect('/login')

    orders = Order.query.filter_by(customerId=user_id).all()

    for order in orders:
        order.movie = Movie.query.get(order.movieId)

    return render_template('orders/orders.html', orders=orders)


from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from . import customers
from datetime import datetime
from app.models import db, User, Order, Movie


@customers.route('/new_customer', methods=['GET', 'POST'])
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

    return render_template('customers/new_customer.html')

@customers.route('/update_customer/<int:customer_id>', methods=['GET', 'POST'])
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
            return redirect(url_for('users'))
        except Exception as e:
            db.session.rollback()
            print(f"Error updating customer: {e}")
            return "There was an issue updating the customer", 500

    return render_template('customers/update_customer.html', customer=customer)


@customers.route('/view_customer/<int:customer_id>', methods=['GET'])
def view_customer(customer_id):
    customer = db.session.query(User).filter(User.id == customer_id).first()
    customer_orders = (
        db.session.query(Order, Movie)
        .join(Movie, Order.movieId == Movie.id)
        .filter(Order.customerId == customer.id)
        .all()
    )
    history_link = url_for('orders.orders', user_id=customer.id)
    return render_template('customers/view_customer.html', customer=customer, customer_orders=customer_orders, history_link=history_link)


@customers.route('/all_customers', methods=['GET'])
def all_customers():
    users = db.session.query(User).all()
    customer_data = []
    for user in users:
        current_rentals = (
            db.session.query(Order, Movie)
            .join(Movie, Order.movieId == Movie.id)
            .filter(Order.customerId == user.id, Order.returnDate == 0)
            .all()
        )
        customer_data.append({
            "customer": user,
            "current_rentals": current_rentals,
        })
    return render_template('customers/all_customers.html', customer_data=customer_data)

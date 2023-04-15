from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import order, user

# dateFormat = "%#m/%#d/%Y %I:%M %p"
dateFormat = "%#m/%#d/%Y %I:%M %p"

@app.route('/')
def index():
    return redirect('/cookies')
    #goes to cookies route.

@app.route('/cookies')
def dashboard():
    return render_template('dashboard.html', all_orders = order.Order.get_all(), dtf = dateFormat)

@app.route('/order/new')
def new_order():
    return render_template('create.html', all_users = user.User.get_all())

@app.route('/order/create', methods = ['post'])
def create_order():
    print(request.form)
    order.Order.save(request.form)
    return redirect ('/cookies')
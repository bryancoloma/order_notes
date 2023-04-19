from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import order, user
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
    if order.Order.validate_order(request.form):
    # validate order - if this renders true, save.
    # request.form - order_data argument being passed from.
        order.Order.save(request.form)
        # if 'is_valid' = True, save info.
        return redirect ('/cookies')
    return redirect('/order/new')
    # if 'is_valid' != true redirect back to order/new

@app.route('/cookies/delete/<int:order_id>')
def delete_order(order_id):
    order.Order.delete({'id':order_id})
    return redirect('/cookies')

@app.route('/cookies/edit/<int:order_id>')
def edit_order(order_id):
    return render_template('edit.html', order = order.Order.get_by_id({'id':order_id}))

@app.route('/order/update', methods=['POST'])
def update_order():
    print(request.form)
    
    return redirect('/cookies')
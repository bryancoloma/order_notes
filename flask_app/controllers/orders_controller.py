from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import order, user
dateFormat = "%-m/%-d/%Y %I:%M %p"

@app.route('/cookies')
def dashboard():
    # return render_template('dashboard.html', all_orders = order.Order.get_all(), dtf = dateFormat) - using get_all method
    return render_template('dashboard.html', all_orders = order.Order.get_all_join_creator(), dtf = dateFormat) #using get_all_join_creator method.


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

@app.route('/order/update/<int:order_id>', methods=['POST'])
def update_order(order_id):
    print(request.form)
    if order.Order.validate_order(request.form):
        data = {
            'type' : request.form['type'],
            'box_quantity' : request.form['box_quantity'],
            'id' : order_id
        }
        # Getting the ID from the order_id (URL) to request.form.
        order.Order.update(data)
        # data - data dictionary.
        return redirect('/cookies')
    return redirect(f'/cookies/edit/{order_id}')
    # Use f-string on string variables inside a string. 

@app.route('/user/show/<int:user_id>')
def show_user(user_id):
    return render_template('show.html', user = user.User.get_by_id({'id' : user_id}))
    #'id' - coming from the get_by_id WHERE %(id)s.
    # user_id - coming from show_user parameter.

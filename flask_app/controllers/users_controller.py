from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models import order, user
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

dateFormat = "%-m/%-d/%Y %I:%M %p"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods =['POST'])
def reg():
    # Use conditional to check if the user validation passed/True.
    if user.User.validate_user(request.form):
    # add request.form to avoid positional argument error.
        hashed_pass =   bcrypt.generate_password_hash(request.form['password'])
        # password is the string we want to hash.
        data = {
            'first_name' : request.form['first_name'],
            'last_name' : request.form['last_name'],
            'email' :request.form['email'],
            'password' : hashed_pass
        }
        # create a dictionary to use the request.form data to create a dictionary add the hashed password.
        user_id = user.User.save(data)
        # save -   insert data that always returns an ID, so use user_id as the varialbe for the result.
        session['user_id'] = user_id
        #save the id result to session.
        return redirect('/cookies')
    return redirect('/')

@app.route('/login', methods = ['POST'])
def login():
    pass
    return redirect('/')

#* 
#! test
#TODO
#? 
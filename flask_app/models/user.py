from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import order
from flask import flash
import re	# the regex module
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# Email pattern includes upper and lower case letters with 0-9, with "_" and "."

mydb = "orders"

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.orders = [] # list of orders the user have. Can have many orders/list.

    @classmethod
    def get_all(cls):
        query = """
        SELECT *
        FROM users;
        """
        results = connectToMySQL(mydb).query_db(query)
        output = []
        for user_dictionary in results:
            output.append(cls(user_dictionary))
        return output
    
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users
        (first_name, last_name, email, password)
        VALUES
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """
        results = connectToMySQL(mydb).query_db(query, data)
        #data - represents request.form and is used to pass in to the connectToMySQL method call. Only used when query has a variable.
        #data needs to match data from save(cls, data)
        # results - returns the ID of the new input
        print(results)
    
    # One side that has a many.
    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT *
        FROM users
        JOIN orders
        ON users.id = creator_id
        WHERE users.id = %(id)s;
        """
        results = connectToMySQL(mydb).query_db(query, data)
        this_user = cls(results[0])
        # creates a user object.
        print(this_user)
        # prints the user object.
        for row in results:
            order_data = {
                    'id' : row['orders.id'],
                    'type' : row['type'],
                    'box_quantity' : row['box_quantity'],
                    'created_at' : row['orders.created_at'],
                    'updated_at' : row['orders.updated_at'],
                    'creator_id' : row['creator_id'],
            }
            this_order = order.Order(order_data)
            print(this_order)
            this_user.orders.append(this_order)
            print(this_user.orders)
        return this_user
    
    @staticmethod
    # @staticmethod - used for validations
    def validate_user(request):
    # request - information coming from the form/request.form.
        is_valid = True
        # print(request['type'])
        # print to check/test info from key. Needs to be called in orders_controller.
        if len(request['first_name']) < 1:
        # request = parameter
            is_valid = False
            flash ('First Name Name is required', 'regError')
            # regError - key to add to html category to specifically populate error on one side (on registration or login side only)
        if  len(request['last_name'])< 1:  
            is_valid = False
            flash ('Last Name is required', 'regError')
        if len(request['email']) < 1:
            is_valid = False
            flash ('Email is required', 'regError')
        elif not EMAIL_REGEX.match(request['email']): 
        # to check if email is valid.
        # EMAIL_REGEX - coming from the module.
            is_valid = False
            flash ('Invalid Email.', 'regError')
        if len(request['password']) < 1:
            is_valid = False
            flash ('Password is required.', 'regError')
        elif request['password'] != request['confirm_password']:
        # to confirm if password confiramtion matches password.
            is_valid = False
            flash ('Passwords must match.', 'regError')
        if User.get_by_email(request)
        # to check if email is already in db
            is_valid = False
            flash ('Choose another email.', 'regError')
            print('email validation')
        return is_valid
        # return to show validate is still true.

    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s;
        """
        result = connectToMySQL(mydb).query_db(query, data)
        if len(result) <1:
            return False
        return cls(result[0])
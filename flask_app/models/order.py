from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

mydb = "orders"

class Order:
    def __init__(self, data):
        self.id = data['id']
        # self.customer_name = data['customer_name']
        self.type = data['type']
        self.box_quantity = data['box_quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id'] # can join to the user table.
        self.creator = None # creator info of the order, from creator_id.
        # self.creator - save the users pulled from the query. A new attribute that's not part of the class that can hold data we're bringing back.

    @classmethod  
    def save(cvls, data):
        query = """
        INSERT INTO orders
        (type, box_quantity, creator_id)
        VALUES 
        (%(type)s, %(box_quantity)s, %(creator_id)s)
        """
        results = connectToMySQL(mydb).query_db(query, data)
        #data needed since the query need to add the variables
        print(results)

    @classmethod
    def get_all(cls):
        query = """
        SELECT *
        FROM orders;
        """
        results = connectToMySQL(mydb).query_db(query)
        output = []
        for order_dictionary in results:
            output.append(cls(order_dictionary))
        return output
    
    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM orders
        WHERE id = %(id)s;
        """
        results = connectToMySQL(mydb).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT *
        FROM orders
        WHERE id = %(id)s;
        """
        results = connectToMySQL(mydb).query_db(query, data)
        return cls(results[0])
        #return the specific id to show on the edit form.

    @staticmethod
    # @staticmethod - used for validations
    def validate_order(order_data):
    # order_data - information coming from the form/request.form.
        is_valid = True
        # print(order_data['type'])
        # print to check/test info from key. Needs to be called in orders_controller.
        if len(order_data['type']) < 1:
            is_valid = False
            flash ('Cookie type is required.')
            #message when cookie type is less than 1 character.
        elif len(order_data['type'])< 2:
            is_valid = False
            flash ('Cookie type must be atleast 2 characters')
        if len(order_data['box_quantity']) < 1:
            is_valid = False
            flash ('Quantity Required')
        elif int(order_data['box_quantity']) <= 0:
            is_valid = False
            flash ('Quantity must be atleast 1.')
        return is_valid
        # return to show validate is still true.

    @classmethod
    def update(cls, data):
        query = """
        UPDATE orders
        SET 
        type = %(type)s,
        box_quantity = %(box_quantity)s
        WHERE id =%(id)s;
        """
        #SET = column name equals variable name from request.form
        results = connectToMySQL(mydb).query_db(query, data)


    @classmethod
    def get_all_join_creator(cls):
        query = """
        SELECT *
        FROM orders
        JOIN users
        ON  orders.creator_id = users.id ;
        """
        # ON - Where orders are associated to a specific user.
        results = connectToMySQL(mydb).query_db(query)
        print(results)
        output = []
        for order_dictionary in results:
            # print(order_dictionary)
            # prints dictionary from the for loop. Each row from the database.
            this_order = cls(order_dictionary)
            # this_order - variable for the order, that creates an object order out of it. 
            print(this_order)
            # turns dictionary and prints out order object.
            user_data = {
                    'id' : order_dictionary['users.id'],
                    'first_name' : order_dictionary['first_name'],
                    'last_name' : order_dictionary['last_name'],
                    'email' : order_dictionary['email'],
                    'password' : order_dictionary['password'],
                    'created_at' : order_dictionary['users.created_at'],
                    'updated_at' : order_dictionary['users.updated_at'],
            }
            # To provide values for all the values for the dictionary from the loop.
            # user.___ - to connect specifically to the correct table. Coming from the dictionary.
            order_user = user.User(user_data)
            # create the creator object/user constructor.
            print(order_user)
            # turns dicitionary and prints out user objects.
            this_order.creator = order_user
            # access the attribute of this_order called creator is equal to a class object of the user info.
            # empty creator object from the user = user object.
            print(this_order.creator)
            # prints out the same value as the user object.+
            output.append(this_order)
        print(output)
        # prints a list of class objects.
        return output


from flask_app.config.mysqlconnection import connectToMySQL

mydb = "orders"

class Order:
    def __init__(self, data):
        self.id = data['id']
        # self.customer_name = data['customer_name']
        self.type = data['type']
        self.box_quantity = data['box_quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator_id = data['creator_id']

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
    # order_data - information coming from the form.
        is_valid = True
        # print(order_data['type'])
        # print to check info from key. Needs to be called in orders_controller.
        if len(order_data['type']) < 1:
            is_valid = False

        return is_valid
        # return to show validate is still true.
        
        # Accesing the 'key' attributes from the order_data. 
        


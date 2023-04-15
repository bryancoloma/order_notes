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
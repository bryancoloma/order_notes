from flask_app.config.mysqlconnection import connectToMySQL

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
# a cursor is the object we use to interact with the database
import pymysql.cursors
# this class will give us an instance of a connection to our database
# used to interact with the database.
class MySQLConnection:
    def __init__(self, db):
    #Constructor
        # change the user and password as needed
        connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    password = 'rootroot', 
                                    db = db,
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = False)
        # establish the connection to the database
        self.connection = connection
    # the method to query the database
    def query_db(self, query:str, data:dict=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)
                #prints "Running Query" and shows the actual query being used on the terminal.
                cursor.execute(query)

                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                    # Returns the ID of the new record.

                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                    # Shows dictionary of key value pair from database

                else:
                    # if query shows UPDATE and DELETE queries will return nothing
                    self.connection.commit()

            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
                #Shows False with "Something went wrong" and "e" will show the error being returned
            finally:
                # close the connection
                self.connection.close() 
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection
def connectToMySQL(db):
    return MySQLConnection(db)
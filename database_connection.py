import mysql.connector as connector


def open_database():
    try:
        connection = connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="123Andrei",
            db="farmacy",
        )
    except connector.DatabaseError as exception:
        print("Database connection problem")
        raise exception

    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        cursor = connection.cursor(dictionary=True, buffered=True)
        ret_value = function(cursor, *args, **kwargs)
        connection.commit()
        connection.close()
        return ret_value

    return wrapper

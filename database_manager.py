import datetime

import database_connection


@database_connection.connection_handler
def get_user(cursor, username):
    query = """
            SELECT *
            FROM farmacy.users
            WHERE username=%(username)s
            ;"""
    cursor.execute(query, {"username": username})
    return cursor.fetchone()


@database_connection.connection_handler
def insert_user(cursor, username, password):
    query = """
                INSERT INTO users(username, password)
                VALUES(%(username)s, %(password)s )
                ;"""
    cursor.execute(
        query, {"username": username, "password": password}
    )




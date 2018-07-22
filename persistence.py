import connection
from datetime import datetime


@connection.connection_handler
def add_user(cursor, username, password):
    cursor.execute("""
                    INSERT INTO users (username, password)
                    VALUES (%(username)s, %(password)s);
                   """, {"username": username,
                         "password": password})


@connection.connection_handler
def add_vote(cursor, planet_id, planet_name, user_id):
    cursor.execute("""
                    INSERT INTO planet_votes (planet_id, planet_name, user_id, submission_time)
                    VALUES (%(planet_id)s, %(planet_name)s, %(user_id)s, %(submission_time)s);
                   """, {"planet_id": planet_id,
                         "planet_name": planet_name,
                         "user_id": user_id,
                         "submission_time": (datetime.now(),)
                         })


@connection.connection_handler
def get_statistics(cursor):
    cursor.execute("""
                    SELECT planet_name, COUNT(planet_id) AS votes FROM planet_votes
                    GROUP BY planet_name ORDER BY votes DESC
                   """)
    return cursor.fetchall()


@connection.connection_handler
def check_if_username_exists(cursor, username):
    cursor.execute("""
                    SELECT id FROM users
                    WHERE username = %(username)s;
                   """, {"username": username})
    return len(cursor.fetchall()) != 0

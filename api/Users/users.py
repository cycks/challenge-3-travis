from datetime import datetime, timedelta
import jwt
from flask import request, jsonify, Blueprint
from flask_classful import FlaskView
from models import connection, my_cursor


assign_my_users_routes = Blueprint("assign_my_users_routes", __name__)


@assign_my_users_routes.route('api/auth/signup', methods=['POST'])
def register():
    """Extracts user details from the post request, runs helper functions,
    and inserts the user's details into the database."""
    details_from_post = request.get_json()
    first_name = details_from_post.get("first_name", None)
    last_name = details_from_post.get("last_name", None)
    email = details_from_post.get("email", None)
    password = details_from_post.get("password", None)
    password2 = details_from_post.get("password2", None)
    user_name = details_from_post.get('user_name', None)
    if password == password2:
        try:
            my_cursor.execute("""SELECT EMAIL FROM USERS WHERE EMAIL = %s AND
                               USERNAME = %s""", (email, user_name,))
            my_cursor.execute("""INSERT INTO USERS (FIRSTNAME, LASTNAME,
                USERNAME,EMAIL, PASSWORD,
                DATETIMEREGISTERED)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                              (first_name, last_name, user_name, email,
                               password, datetime.now()))
            connection.commit()
            return jsonify({"message": "Successfully registered."})
        except BaseException:
            return jsonify({"message": "user_name or email already taken."})
    else:
        return jsonify({"message": "passwords must match"})


@assign_my_users_routes.route('api/auth/login/v2', methods=['GET', 'POST'])
def login():
    """Extracts user details from the post request, runs helper functions to
    confirm the user is registered, and inserts the user's details into the
    database."""
    details_from_post = request.get_json()
    email = details_from_post.get("email", None)
    password = details_from_post.get("password", None)
    try:
        my_cursor.execute("""SELECT ID FROM USERS WHERE (EMAIL = %s AND
              PASSWORD = %s)""", (email, password,))
        user_id = my_cursor.fetchone()
        connection.commit()
        jwt.encode({'user':user_id[0], 'exp': datetime.utcnow() +
                                              timedelta(minutes=10)},
                   "This is not the owner")
        return jsonify({"message": "user successfully logged in."})
    except BaseException:
        return jsonify({"message": "Invalid credentials."})

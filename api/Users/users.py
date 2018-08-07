"""Module Containing my Users"""
from datetime import datetime, timedelta

import jwt
from flask import jsonify, Blueprint

from models import create_user, check_user_in_database, my_cursor, validate_user_contents
from . import user_details

assign_my_users_routes = Blueprint("assign_my_users_routes", __name__)


@assign_my_users_routes.route('/api/v2/auth/signup', methods=['POST', 'GET'])
def register():
    """Extracts user details from the post request, runs helper functions,
    and inserts the user's details into the database."""
    details = user_details.UserDetails()
    if details.get_password() == details.get_password2():
        # if validate_user_contents(first_name, last_name, user_name,
        #                           email, password) is False:
        #     return jsonify({"message": """No entry should be greater than
        #                                50 or less than five"""})
        if create_user(details.get_first_name, details.get_last_name(),
                       details.get_user_name(), details.get_email(),
                       details.get_password()) is True:
            return jsonify({"message": "Successfully registered."}), 201
        return jsonify({"message": "username or email already taken."}), 403
    return jsonify({"message": "passwords must match"}), 403


@assign_my_users_routes.route('/api/v2/auth/login', methods=['POST'])
def login():
    """Extracts user details from the post request, runs helper functions to
    confirm the user is registered, generates an access token for the user and
    responds with an appropriate message."""
    details = user_details.UserDetails()
    user_id = check_user_in_database(details.get_email(), details.get_password())
    if user_id:
        user_token = jwt.encode({'user': user_id[0],
                                 'exp': datetime.utcnow() + timedelta(minutes=40)},
                                "This is not the owner")
        return jsonify({"user_token": user_token.decode('utf-8'), "user": user_id}), 200
    return jsonify({"message": "Invalid credentials."}), 401


@assign_my_users_routes.route('/api/v2/auth/profile', methods=['GET'])
def fetch_user_profile():
    """Extracts user details from the post request, runs helper functions to
    confirm the user is registered, and fetches the user's details from the
    database."""
    details = user_details.UserDetails()
    user_id = details.get_user_id
    if isinstance(user_id, bool) is False:
        my_cursor.execute("""SELECT FIRSTNAME, LASTNAME, USERNAME,EMAIL
                          FROM USERS WHERE ID = %s;""", (user_id,))
        one_entry = my_cursor.fetchall()
        return jsonify({"message": one_entry}), 200
    return jsonify({"message" " Invalid token please login first"}), 401

from datetime import datetime, timedelta
from flask import request, jsonify
from models import connection, my_cursor
from run import app


def register():
  """Extracts user details from the post request, runs helper functions,
  and inserts the user's details into the databse."""
  details_from_post = request.get_json()
  firstname = details_from_post.get("firstname", None)
  lastname = details_from_post.get("lastname", None)
  email = details_from_post.get("email", None)
  password = details_from_post.get("password", None)
  password2 = details_from_post.get("password2", None)
  username = details_from_post.get('username', None)
  if password == password2:
    my_cursor.execute("""SELECT * FROM USERS WHERE EMAIL = %s AND 
    USERNAME = %s""", (email, username,))
    detail = my_cursor.fetchone()
    connection.commit()
    if detail is None:
      my_cursor.execute("""INSERT INTO USERS (FIRSTNAME, LASTNAME,
                USERNAME,EMAIL, PASSWORD,
                DATETIMEREGISTERED)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (firstname, lastname, username, email,
                password, datetime.now()))
      connection.commit()
      return jsonify({"message": "Successfully registered."})
    else:
      return jsonify({"message": "username or email already taken."})
  else:
    return jsonify({"message": "passwords must match"})


def login():
  """Extracts user details from the post request, runs helper functions to
  confirm the user is registered, and inserts the user's details into the
  databse."""
  details_from_post = request.get_json()
  email = details_from_post.get("email", None)
  password = details_from_post.get("password", None)
  my_cursor.execute("""SELECT * FROM USERS WHERE (EMAIL = %s AND
            PASSWORD = %s)""", (email, password,))
  user = my_cursor.fetchone()
  connection.commit()
  if user is None:
      return jsonify({"message": "Invalid credentials."})
  else:
      return jsonify({"message": "user succesfully logged in."})

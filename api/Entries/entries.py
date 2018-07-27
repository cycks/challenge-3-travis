from datetime import datetime, timedelta
from flask import request, jsonify, Blueprint
from models import connection, my_cursor


assign_my_entries_routes = Blueprint("assign_my_entries_routes", __name__)


def authorize_user_with_token():
    """Tries to generate an access token and informs the user if the token
    is invalid"""
    access_token = request.args.get('token')
    try:
        user_token = jwt.decode(access_token, "This is not the owner")
        return user_token
    except:
        return jsonify({'message': "Missing Token or invalid"})


@assign_my_entries_routes.route('api/entries/v2', methods=['POST'])
def add_entries():
    """Extracts user details from the post request, runs helper 
    functions to confirm the user is registered, and inserts the
    user's details into the database."""
    return jsonify({"message":authorize_user_with_token()})
    details_from_post = request.get_json()
    email = details_from_post.get("email", None)
    title = details_from_post.get("title", None)
    contents = details_from_post.get("contents", None)
    date_of_event = details_from_post.get("date_of_event", None)
    reminder_time = details_from_post.get("reminder_time", None)
    user_id = details_from_post.get("user_id", None)
    check_nulls = {"email":email, "title":title, "contents":contents,
                   "date_of_event":date_of_event,
                   "reminder_time": reminder_time,
                   "user_id": user_id}
    for k in check_nulls:
        if check_nulls[k] is not None:
            return jsonify({"message": k+" is empty"})
    my_cursor.execute("""INSERT INTO ENTRIES (TITLE, CONTENTS, DATEOFEVENT,
                                     TIMETOMODIFY, REMINDERTIME, USERID)
                                     VALUES (%s, %s, %s, %s, %s, %s);""",
                      (title, contents, date_of_event,
                       datetime.now() + timedelta(hours=24), reminder_time,
                       user_id))
    connection.commit()
    return jsonify({"message":"contents updated"})


@assign_my_entries_routes.route('api/entries/v2/<int:entryId>', methods=['GET'])
def get_one_entry(entryId):
    """Extracts contents from the post request and responds with the
    entry."""
    user_id = 1
    entry_id = entryId
    my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT, REMINDERTIME
            FROM ENTRIES WHERE (ID = %s AND USERID = %s)""",
                      (entry_id, user_id,))
    one_entry = my_cursor.fetchone()
    if one_entry is not None:
        return jsonify({"message": one_entry})
    return jsonify({"message": "The entry does not exist"})


@assign_my_entries_routes.route('/entries', methods=['GET'])
def get_all_entries():
    """Uses a default user id to query the database and display all the entries
    associated with the user."""
    user_id = 1
    my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT, REMINDERTIME
                      FROM ENTRIES WHERE USERID = %s;""", (user_id,))
    one_entry = my_cursor.fetchall()
    if one_entry is not None:
        return jsonify({"message": one_entry})
    return jsonify({"message": "Your diary has no entries"})


@assign_my_entries_routes.route('api/entries/v2/<int:entryId>', methods=['PUT'])
def modify_entry(entryId):
    details_from_post = request.get_json()
    title = details_from_post.get("title", None)
    contents = details_from_post.get("contents", None)
    date_of_event = details_from_post.get("date_of_event", None)
    reminder_time = details_from_post.get("reminder_time", None)
    user_id = details_from_post.get("user_id", None)
    entry_id = entryId
    my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT, REMINDERTIME
            FROM ENTRIES WHERE (ID = %s AND USERID = %s)""",
                      (entry_id, user_id,))
    one_entry = my_cursor.fetchone()
    connection.commit()
    if one_entry is not None:
        my_cursor.execute("""UPDATE ENTRIES SET TITLE = %s,CONTENTS = %s,
                             DATEOFEVENT = %s, REMINDERTIME = %s WHERE ID = %s
                             AND USERID = %s""", (title, contents,
                                                  date_of_event,
                                                  reminder_time,
                                                  entry_id, user_id,))
        my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT, REMINDERTIME
                FROM ENTRIES WHERE (ID = %s AND USERID = %s)""",
                          (entry_id, user_id,))
        one_entry = my_cursor.fetchone()
        connection.commit()
        return jsonify({"message": one_entry})
    return jsonify({"message": "The entry does not exist"})

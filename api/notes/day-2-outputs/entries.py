from datetime import datetime, timedelta
from flask import request, jsonify
from models import connection, my_cursor
from run import app




def add_entries():
  """Extracts user details from the post request, runs helper functions to
  confirm the user is registered, and inserts the user's details into the
  databse."""
  details_from_post = request.get_json()
  email = details_from_post.get("email", None)
  title = details_from_post.get("title", None)
  contents = details_from_post.get("contents", None)
  dateofevent = details_from_post.get("dateofevent", None)
  timetomodify = datetime.now() + timedelta(hours=24)
  remindertime = details_from_post.get("remindertime", None)
  user_id = details_from_post.get("user_id", None)
  check_nulls = {"email":email, "title":title, "contents":contents,
          "dateofevent":dateofevent, "remindertime": remindertime,
          "user_id": user_id}
  for k in check_nulls:
    if len(check_nulls[k]) <= 0:
      return jsonify({"message": k+" is empty"})
  my_cursor.execute("""INSERT INTO ENTRIES (TITLE, CONTENTS, DATEOFEVENT,
          TIMETOMODIFY, REMINDERTIME, USERID)
          VALUES (%s, %s, %s, %s, %s, %s);""", (title, contents,
          dateofevent, datetime.now() + timedelta(hours=24),
          remindertime, user_id))
  connection.commit()
  return jsonify({"message":"contents updated"})



def get_one_entry(entryId):
  """Extracts contents from the post request and responds with the entry."""
  user_id = 1
  entry_id = entryId
  my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT, REMINDERTIME
            FROM ENTRIES WHERE (ID = %s AND USERID = %s)""",
            (entry_id, user_id,))
  one_entry = my_cursor.fetchone()
  if len(one_entry) >1 :
    return jsonify({"message": one_entry})
  else:
    return jsonify({"message": "The entry does not exist"})


@app.route('/entries', methods=['GET'])
def get_all_entries():
  user_id = 1
  my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT, REMINDERTIME
            FROM ENTRIES WHERE USERID = %s;""", (user_id,))
  one_entry = my_cursor.fetchall()
  if len(one_entry) >1 :
    return jsonify({"message": one_entry})
  else:
    return jsonify({"message": "Your diary has no entries"})



def modify_entry(entryId):
  details_from_post = request.get_json()
  email = details_from_post.get("email", None)
  title = details_from_post.get("title", None)
  contents = details_from_post.get("contents", None)
  dateofevent = details_from_post.get("dateofevent", None)
  timetomodify = datetime.now() + timedelta(hours=24)
  remindertime = details_from_post.get("remindertime", None)
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
                          AND USERID = %s""", (title, contents, dateofevent,
                          remindertime, entry_id, user_id,))
    my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT, REMINDERTIME
            FROM ENTRIES WHERE (ID = %s AND USERID = %s)""",
            (entry_id, user_id,))
    one_entry = my_cursor.fetchone()
    connection.commit()
    return jsonify({"message": one_entry})
  else:
    return jsonify({"message": "The entry does not exist"})
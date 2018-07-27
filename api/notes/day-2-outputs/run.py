import datetime, psycopg2
from datetime import datetime, timedelta
from flask import Flask, request, jsonify


app = Flask(__name__)
app.config['SECRET_KEY'] = "TheOwner"

try:
  connection = psycopg2.connect(database="mydiary", user="postgres",
                password="actuarial", host="127.0.0.1",
                port="5432")
  my_cursor = connection.cursor()
except Exception as e:
  connection.rollback()
  print(str(e)+"Database conncetion failed!")


def create_user_table():
  try:
    user_table = my_cursor.execute('''CREATE TABLE USERS
          (ID                 SERIAL    PRIMARY KEY,
          FIRSTNAME           TEXT      NOT NULL,
          LASTNAME            TEXT      NOT NULL,
          USERNAME            TEXT      NOT NULL UNIQUE,
          EMAIL               TEXT      NOT NULL UNIQUE,
          PASSWORD            TEXT      NOT NULL,
          DATETIMEREGISTERED  TIMESTAMP NOT NULL);''')
    connection.commit()
    print("A table called USERS has been created")
    return user_table
  except Exception as e:
      connection.rollback()
      return str(e)+"Table USERS already exists"


def create_entries_table():
  try:
    user_table = my_cursor.execute('''CREATE TABLE ENTRIES
                    (ID             SERIAL    PRIMARY KEY,
                    TITLE           TEXT      NOT NULL,
                    CONTENTS        TEXT      NOT NULL,
                    DATEOFEVENT     TIMESTAMP   NOT NULL,
                    TIMETOMODIFY    TIMESTAMP   NOT NULL,
                    REMINDERTIME    TIMESTAMP   NOT NULL,
                    USERID          INT REFERENCES USERS
                    ON DELETE CASCADE);''')
    print("A table called ENTRIES has been created")
    connection.commit()
    return user_table
  except Exception as e:
      connection.rollback()
      return str(e)+"Table ENTRIES already exists"


@app.route('/auth/v1', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to my home page"})


@app.route('/auth/signup', methods=['POST'])
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


@app.route('/auth/login', methods=['GET', 'POST'])
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


@app.route('/entries', methods=['POST'])
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


@app.route('/entries/<int:entryId>', methods=['GET'])
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


@app.route('/entries/<int:entryId>', methods=['PUT'])
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

if __name__ == "__main__":
  app.run(debug = True, port=5000)
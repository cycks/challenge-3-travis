import datetime, psycopg2
from datetime import datetime, timedelta
from flask import Flask, request, jsonify

# from models import check_passwords_match, create_user, create_entry
# from models import check_user_in_database, get_all_diary_entries, get_one_entry
# from models import modify_entry, my_cursor, connection


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
# print(create_user_table())


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


def check_passwords_match(password, password2):
    if password == password2:
        return True
    return False  # else missing to improve code efficiency


def check_user_in_database(email, password):
    try:
        my_cursor.execute("""SELECT * FROM USERS WHERE (EMAIL = %s AND
                        PASSWORD = %s)""", (email, password,))
        return None in my_cursor.fetchone() 
    except Exception as e:
        connection.rollback()
        return "Invalid credentials."
# print(check_user_in_database("emaily", "passwordy"))

def check_email_and_username_exist(email, username):
    try:
        my_cursor.execute("""SELECT * FROM USERS WHERE EMAIL = %s AND 
          USERNAME = %s""", (email, username,))
        return my_cursor.fetchone() is not None
    except Exception as e:
        connection.rollback()
        return "False"
print(check_email_and_username_exist("emaily", "usernamey"))

def create_user(firstname, lastname, username, email, password):
    try:
        my_cursor.execute("""INSERT INTO USERS (FIRSTNAME, LASTNAME,
                                              USERNAME,EMAIL, PASSWORD,
                                              DATETIMEREGISTERED)
                          VALUES (%s, %s, %s, %s, %s, %s)""",
                          (firstname, lastname, username, email,
                          password, datetime.now()))
        connection.commit()
        return jsonify({"message": "user successfuly registered."})
    except Exception as e:
        connection.rollback()
        return jsonify({"message": "username or email already taken"})


def create_entry(title, contents, dateofentry, remindertime, user_id):
    diary_entry = [title, contents, dateofentry, remindertime, user_id]
    modify = datetime.now() + timedelta(hours=24)
    try:
        my_cursor.execute("""INSERT INTO ENTRIES (TITLE, CONTENTS, DATEOFEVENT,
                      TIMETOMODIFY, REMINDERTIME, USERID)
                      VALUES (%s, %s, %s, %s, %s, %s)""",
                      (title, contents, dateofentry, modify, remindertime,
                       user_id))
        connection.commit()
        return "comment successfuly entered"
    except Exception as e:
        connection.rollback()
        return str(e)+"comment not entered"


def get_all_diary_entries(user_id):
    try:
        my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT, REMINDERTIME
                      FROM ENTRIES WHERE USERID = %s""", (user_id,))
        all_entries = my_cursor.fetchall()
        connection.commit()
        return all_entries
    except Exception as e:
        connection.rollback()
        return "An unkonwn error occurred consult the developer"


def get_one_entry(entry_id, user_id):
    try:
        my_cursor.execute("""SELECT TITLE, CONTENTS, DATEOFEVENT, REMINDERTIME
                      FROM ENTRIES WHERE (ID = %s AND USERID = %s)""",
                      (entry_id, user_id,))
        one_entry = my_cursor.fetchone()
        connection.commit()
        return one_entry
    except Exception as e:
        connection.rollback()
        return "The entry you have entered does not exist"


def modify_entry(entry_id, user_id, title, contents, dateofevent,
                 remindertime):
    get_one_entry(entry_id, user_id)
    try:
        my_cursor.execute("""UPDATE ENTRIES SET TITLE = %s,CONTENTS = %s,
                          DATEOFEVENT = %s, REMINDERTIME = %s WHERE ID = %s
                          AND USERID = %s""", (title, contents, dateofevent,
                          remindertime, entry_id, user_id,))
        connection.commit()
        return "Entry updated."
    except Exception as e:
        connection.rollback()
        return "Entry not updated"


@app.route('/auth/v1', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to my home page"})


@app.route('/auth/signup', methods=['POST'])
def register():
    """Extracts user details from the post request, runs helper functions,
    and inserts the user's details into the databse."""
#    details_from_post = request.get_json()
    firstname = 'firstname'
    lastname = 'lastname'
    email = 'sikolia2.wycliffe@gmail.com'
    username = 'cycks'
    password = 'password'
    password2 = 'password'
    if check_passwords_match(password, password2) is True:
        if check_email_and_username_exist(email, username) is False:
            create_user(firstname, lastname, username, email, password)
            return jsonify({"message": "Successfully registered."})
        else:
            return jsonify({"message": "username or email already taken."})
    else:
        return jsonify({"message": "passwords must match"})


@app.route('/auth/sigin', methods=['GET', 'POST'])
def login():
    """Extracts user details from the post request, runs helper functions to
    confirm the user is registered, and inserts the user's details into the
    databse."""
    # details_from_post = request.get_json()
    email = 'sikolia21.wycliffe@gmail.com'
    password = 'password'
    if check_user_in_database(email, password) is not None:
        return "Successfully logged in."
    else:
        return "Invalid credentials"


@app.route('/entries', methods=['POST'])
def add_entries():
    """Loads datbase from the file, retrieves information
     from the request, and updates the information in the
     database."""
    details_from_post = request.get_json()
    email = 'sikolia2.wycliffe@gmail.com',
    entry = "Stand up with LFA"
    

@app.route('/api/v1/entries', methods=['GET'])
def get_entries():
    """Fetches information from the databse, gets 
    all user entries from the database, uses an 
    email provided in the code to retrieve entries
    from the ddatabase."""
    my_database = json.load(open("my_database.txt"))
    email = "sikolia21.wycliffe@gmail.com"
    user_entries = my_database.get(email, None)[3]
    return jsonify({"email": email,
                    "entries": user_entries})

@app.route('/api/v1/entries/<int:entryId>', methods=['GET'])
def get_one_entry(entryId):
    """Uses a default email to query my_database for the user details,
    retrieves user entries from the user details and uses an id sent
    from the request to fetch the entry in the user_entries. """
    my_database = json.load(open("my_database.txt"))
    email = "sikolia21.wycliffe@gmail.com"
    user_details = my_database.get(email, None)
    user_entries = user_details[3]
    requested_entry = user_entries[entryId]
    try:
        requested_entry = user_entries[entryId]
        return jsonify({"email": email,
                        "Requested_entry": requested_entry})
    except:
        return jsonify({"email": email,
                        "message": "entry does not exist"})

@app.route('/api/v1/entries/<int:entryId>', methods=['PUT'])
def modify_entry(entryId):
    """Uses a default email to query my_database for the user details,
    retrieves user entries from the user details and uses an id sent
    from the request to modify the entry in the user_entries."""
    my_database = json.load(open("my_database.txt"))
    details_from_post = request.get_json()
    entry = details_from_post.get("entry", None)
    email = details_from_post.get("email", None)
    user_details = my_database.get(email, None)
    user_entries = user_details[3]
    try:
        requested_entry = user_entries[entryId]
        user_entries[entryId] = entry
        json.dump(my_database, open("my_database.txt",'w'))
        return jsonify({"email": email,
                        "Requested_entry": entry})
    except:
        return jsonify({"email": email,
                        "message": "entry does not exist"})


if __name__ == "__main__":
    app.run(debug = True, port=5000)
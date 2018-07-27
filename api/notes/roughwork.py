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

def check_email_and_username_exist(email, username):
    try:
        my_cursor.execute("""SELECT * FROM USERS WHERE EMAIL = %s AND 
          USERNAME = %s""", (email, username,))
        detail = my_cursor.fetchone()
        if detail is None:
            return True
        return False
    except Exception as e:
        connection.rollback()
        return "An unkonwn error occurred."

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


if __name__ == "__main__":
    app.run(debug = True, port=5000)
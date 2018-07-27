import psycopg2
from datetime import datetime, timedelta

try:
    connection = psycopg2.connect(database="mydiary", user="postgres",
                                  password="actuarial", host="127.0.0.1",
                                  port="5432")
    my_cursor = connection.cursor()
except Exception as e:
    connection.rollback()
    print("Database conncetion failed!")


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
        return "Table USERS already exists"
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
        return "Table ENTRIES already exists"

# def check_user_details(firstname, lastname, username, email, password,
#                        password2):
#     user_identity = [firstname, lastname, username, email, password, password2]
#     for i in user_identity:
#         if i is None:
#             return str(i) + "is null"
#     return True  # No else statement to improve code efficiency


def check_passwords_match(password, password2):
    if password == password2:
        return True
    else:
        return  "passwords must match"


def create_user(firstname, lastname, username, email, password, password2):
    print(check_passwords_match(password, password2))
    try:
        my_cursor.execute("""INSERT INTO USERS (FIRSTNAME, LASTNAME,
                                                USERNAME,EMAIL, PASSWORD,
                                                DATETIMEREGISTERED)
                            VALUES (%s, %s, %s, %s, %s, %s)""",
                            (firstname, lastname, username, email,
                            password, datetime.now()))
        connection.commit()
        return "user successfuly registered."
    except Exception as e:
        connection.rollback()
        return "username or email already taken"


# print(create_user('', 'lastnamey', 'usernamey', 'emaily',
#                  'passwordy', 'password1y'))
def create_entry(title, contents, dateofentry, remindertime, user_id):
    diary_entry = [title, contents, dateofentry, remindertime, user_id]
    modify = datetime.now() + timedelta(hours=24)
    for i in diary_entry:
        if i is None:
            return "message"+str(i)+"is null"
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


# print(create_entry("title", "contents", datetime.now(),
#                    datetime.now() + timedelta(hours=14), 1))
def check_user_in_database(username, password):
    try:
        my_cursor.execute("""SELECT * FROM USERS WHERE (USERNAME = %s AND
                        PASSWORD = %s)""", (username, password,))
        return my_cursor.fetchone() is not None
    except Exception as e:
        connection.rollback()
        return "Please register first."
# print(check_user_in_database("usernamey", "passwordy"))


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
# print( get_all_diary_entries(1))


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
# print(get_one_entry(3, 1))


def modify_entry(entry_id, user_id, title, contents, dateofevent,
                 remindertime):
    get_one_entry(entry_id, user_id)
    try:
        my_cursor.execute("""UPDATE ENTRIES SET TITLE = %s,CONTENTS = %s,
                          DATEOFEVENT = %s, REMINDERTIME = %s WHERE ID = %s
                          AND USERID = %s""", (title, contents, dateofevent,
                          remindertime, entry_id, user_id,))
        connection.commit()
        return
    except Exception as e:
        connection.rollback()
        return "Entry not updated"


# print(modify_entry(4, 1, "title changed", "contents changed",
#                    datetime.now(), datetime.now() + timedelta(hours=14)))

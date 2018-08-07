""""file containing functions that interact with the database."""
from datetime import datetime
import psycopg2

try:
    connection = psycopg2.connect(database="mydiary", user="postgres",
                                  password="actuarial", host="127.0.0.1",
                                  port="5432")
    my_cursor = connection.cursor()
except psycopg2.DatabaseError:
    print("Database connection failed!")


def create_user_table():
    """Helper function used to create the user_table"""
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
    except psycopg2.DatabaseError:
        connection.rollback()
        return "Table USERS already exists"


def create_entries_table():
    """Helper function used to create an entries table."""
    try:
        entry_table = my_cursor.execute('''CREATE TABLE ENTRIES
                                      (ID             SERIAL      PRIMARY KEY,
                                      TITLE           TEXT        NOT NULL,
                                      CONTENTS        TEXT        NOT NULL,
                                      DATEOFEVENT     TIMESTAMP   NOT NULL,
                                      TIMETOMODIFY    TIMESTAMP   NOT NULL,
                                      REMINDERTIME    TIMESTAMP   NOT NULL,
                                      USERID          INT REFERENCES USERS
                                      ON DELETE CASCADE);''')
        print("A table called ENTRIES has been created")
        connection.commit()
        return entry_table
    except psycopg2.DatabaseError:
        connection.rollback()
        return "Table ENTRIES already exists"


def check_user_in_database(email, password):
    """Helper function used to check if a user is in the database."""
    my_cursor.execute("""SELECT ID FROM USERS WHERE EMAIL = %s AND
                      PASSWORD = %s;""", (email, password,))
    user_id = my_cursor.fetchone()
    connection.commit()
    if user_id:
        return user_id
    return False


def create_user(first_name, last_name, user_name, email, password):
    """Helper function used to create a user"""
    my_cursor.execute("""SELECT ID FROM USERS WHERE EMAIL = %s OR
                     USERNAME = %s;""", (email, user_name,))
    user_in_database = my_cursor.fetchone()
    if user_in_database is None:
        my_cursor.execute("""INSERT INTO USERS (FIRSTNAME, LASTNAME,
                                          USERNAME,EMAIL, PASSWORD,
                                          DATETIMEREGISTERED)
                          VALUES (%s, %s, %s, %s, %s, %s);""",
                          (first_name, last_name, user_name, email,
                           password, datetime.now()))
        connection.commit()
        return True
    return False


def validate_entry_contents(title, contents, date_of_entry, reminder_time):
    """Helper function used to validate diary entries."""
    diary_entry = [title, contents, date_of_entry, reminder_time]
    for entry in diary_entry:
        if len(entry) <= 5 or len(entry) >= 50 or "execute" in entry:
            return False
    return True


def create_entry(title, contents, date_of_entry, modify, reminder_time,
                 user_id):
    """Helper function used to create a diary entry."""
    my_cursor.execute("""INSERT INTO ENTRIES (TITLE, CONTENTS, DATEOFEVENT,
                      TIMETOMODIFY, REMINDERTIME, USERID)
                      VALUES (%s, %s, %s, %s, %s, %s);""",
                      (title, contents, date_of_entry, modify, reminder_time,
                       user_id))
    connection.commit()


def update_entry(entry_id, user_id, title, contents, date_of_event,
                 reminder_time):
    """Helper function used to update a diary entry."""
    my_cursor.execute("""SELECT ID FROM ENTRIES WHERE ID = %s AND
                     USERID = %s;""", (entry_id, user_id,))
    entry_in_database = my_cursor.fetchone()
    if entry_in_database:
        my_cursor.execute("""UPDATE ENTRIES SET TITLE = %s,CONTENTS = %s,
                          DATEOFEVENT = %s, REMINDERTIME = %s WHERE ID = %s
                          AND USERID = %s""",
                          (title, contents, date_of_event, reminder_time,
                           entry_id, user_id,))
        connection.commit()
        return True
    return False


def remove_entry(entry_id, user_id):
    """Helper function used to delete a diary entry."""
    my_cursor.execute("""SELECT ID FROM ENTRIES WHERE ID = %s AND
                     USERID = %s;""", (entry_id, user_id,))
    entry_in_database = my_cursor.fetchone()
    if entry_in_database:
        my_cursor.execute("""DELETE FROM ENTRIES WHERE ID = %s
                          AND USERID = %s""", (entry_id, user_id,))
        connection.commit()
        return True
    return False

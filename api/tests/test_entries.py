"""File used to test user diary entry endpoints"""

import unittest
import json

from __init__ import app


class TestFunctionality(unittest.TestCase):
    """A class used to test user entries."""

    @property
    def help_login_user(self):
        """Helper function used to login a user. sends a post request
        with valid credentials for a registered user, decodes the response,
        and converts the response into a dictionary. It then extracts a value
        from the dictionary with the key user_token and returns the token."""
        with app.test_client() as myapp:
            login_user = myapp.post('/api/v2/auth/login', json=dict(
                    email='sikolia2.wycliffe@gmail.com', password='password'))
            login_user = json.loads(login_user.data.decode("utf-8"))
            token = str(login_user.get("user_token", None))
        return token

    def test_add_entries(self):
        """log in a user then tests whether the application can add an
         entry."""
        with app.test_client() as myapp:
            response = myapp.post('/api/v2/entries?user_token='
                                  + self.help_login_user,
                                  json={"title": "Check Delete working",
                                        "contents": "Stand up with LFA",
                                        "date_of_event": "1532521128",
                                        "reminder_time": "1532521128"})
        self.assertEqual(response.status_code, 201,
                         msg='The status code should be 201')
        self.assertTrue(b'now in the database.' in response.data,
                        msg="'now in the database.' should be in the response")

    def test_add_invalid_entry(self):
        """log in a user then tests whether the application can add an
         invalid entry."""
        with app.test_client() as myapp:
            response = myapp.post('/api/v2/entries?user_token='
                                  + self.help_login_user,
                                  json={"title": "Che",
                                        "contents": "Stand up with LFA",
                                        "date_of_event": "1532521128",
                                        "reminder_time": "1532521128"})
        self.assertEqual(response.status_code, 411,
                         msg='The status code should be 411')
        self.assertTrue(b'should be less than five or' in response.data,
                        msg="'should be less than five or' should be in\
                         the response")

    def test_add_entry_by_invalid_user(self):
        """Tests whether a user can add an entry without logging in to
        the application."""
        with app.test_client() as myapp:
            response = myapp.post('/api/v2/entries',
                                  json={"title": "Check delete",
                                        "contents": "Stand up with LFA",
                                        "date_of_event": "1532521128",
                                        "reminder_time": "1532521128"})
        self.assertEqual(response.status_code, 401,
                         msg='The status code should be 401')
        self.assertTrue(b'Invalid token please' in response.data,
                        msg="'Invalid token please' should be in the response")

    def test_get_one_entry(self):
        """Log in a user then tests whether the user can get one valid entry
         from the diary."""
        with app.test_client() as myapp:
            response = myapp.get('/api/v2/entries/19?user_token='
                                 + self.help_login_user)
        self.assertEqual(response.status_code, 200,
                         msg='The status code should be 200')
        self.assertTrue(b'message' in response.data,
                        msg="'message' should be in the response")

    def test_get_one_invalid_entry(self):
        """log in a user then tests whether the application can get an
         invalid entry."""
        with app.test_client() as myapp:
            response = myapp.get('/api/v2/entries/0?user_token='
                                 + self.help_login_user)
        self.assertEqual(response.status_code, 403,
                         msg='The status code should be 403')
        self.assertTrue(b'The entry does not exist' in response.data,
                        msg="'The entry does not exist' should be in\
                             the response")

    def test_get_one_entry_invalid_user(self):
        """Tests whether a user can get an entry without logging in to
        the application."""
        with app.test_client() as myapp:
            response = myapp.get('/api/v2/entries/19')
        self.assertEqual(response.status_code, 401,
                         msg='The status code should be 401')
        self.assertTrue(b'Invalid token please' in response.data,
                        msg="'Invalid token please' should be in the response")

    def test_get_all_entries(self):
        """Log in a user then tests whether the user can get all entries
         from the diary."""
        with app.test_client() as myapp:
            response = myapp.get('/api/v2/entries?user_token='
                                 + self.help_login_user)
        self.assertEqual(response.status_code, 200,
                         msg='The status code should be 200')
        self.assertTrue(b'message' in response.data,
                        msg="'message' should be in the response")

    def test_get_all_entries_invalid_user(self):
        """Tests whether a user can get all entries without logging in to
        the application."""
        with app.test_client() as myapp:
            response = myapp.get('/api/v2/entries')
        self.assertEqual(response.status_code, 401,
                         msg='The status code should be 401')
        self.assertTrue(b'Invalid token please' in response.data,
                        msg="'Invalid token please' should be in the response")

    def test_modify_entry(self):
        """Log in a user then tests whether the user can get all entries
         from the diary."""
        with app.test_client() as myapp:
            response = myapp.post('/api/v2/entries/19?user_token='
                                  + self.help_login_user,
                                  json={"title": "Check",
                                        "contents": "Stand up with LFA",
                                        "date_of_event": "1532521128",
                                        "reminder_time": "1532521128"})
        self.assertEqual(response.status_code, 200,
                         msg='The status code should be 200')
        self.assertTrue(b'message' in response.data,
                        msg="'message' should be in the response")


if __name__ == "__main__":
    unittest.main()

"""File used to test user registration login and profile."""

import unittest
import json

from __init__ import app


class TestFunctionality(unittest.TestCase):
    """A class used to test users and home page."""

    def test_main_page(self):
        """sends a get request to the home page, extracts the response from
        the request and confirms that the status code from the response is
        200"""
        with app.test_client() as myapp:
            response = myapp.get('/api/v2/auth')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(b'Welcome to my home page' in response.data,
                            msg="""'Welcome to my home page' should be in
                            the response""")

    def test_register_used_email(self):
        """Tests that registration with an already registered email is not
        allowed"""
        with app.test_client() as myapp:
            response = myapp.post('/api/v2/auth/signup',
                                  json=dict(first_name='firstname',
                                            last_name='lastname',
                                            email='sikolia2.wycliffe@gmail.com',
                                            user_name='cycks1',
                                            password='password',
                                            password2='password'))
        self.assertEqual(response.status_code, 403,
                         msg='''The status code should be 403''')
        self.assertTrue(b'username or email already taken' in response.data,
                        msg="""'username or email already taken' should be in
                        the response""")

    def test_register_used_username(self):
        """Tests that registration with an already registered username is
        not allowed"""
        with app.test_client() as myapp:
            response = myapp.post('/api/v2/auth/signup',
                                  json=dict(first_name='firstname',
                                            last_name='lastname',
                                            email='sikolia21.wycliffe@gmail.com',
                                            user_name='cycks',
                                            password='password',
                                            password2='password'))
        self.assertEqual(response.status_code, 403,
                         msg='''The status code should be 403''')
        self.assertTrue(b'username or email already taken' in response.data,
                        msg="""'username or email already taken' should be in
                        the response""")

    def test_login_page(self):
        with app.test_client() as myapp:
            response = myapp.post('/api/v2/auth/login', json=dict(
                           email='sikolia2.wycliffe@gmail.com',
                           password='password'))
        self.assertEqual(response.status_code, 200,
                         msg='The status code should be 200')
        self.assertTrue(b'user_token' in response.data,
                        msg="'Invalid credentials' should be in the response")

    def test_login_with_wrong_password(self):
        with app.test_client() as myapp:
            response = myapp.post('/api/v2/auth/login', json=dict(
                           email='sikolia2.wycliffe@gmail.com',
                           password='password3'))
        self.assertEqual(response.status_code, 401,
                         msg='The status code should be 401')
        self.assertTrue(b'Invalid credentials' in response.data,
                        msg="'Invalid credentials' should be in the response")

    def test_login_with_wrong_email(self):
        with app.test_client() as myapp:
            response = myapp.post('/api/v2/auth/login', json=dict(
                                email='sikolia2241.wycliffe@gmail.com',
                                password='password'))
        self.assertEqual(response.status_code, 401,
                         msg='The status code should be 401')
        self.assertTrue(b'Invalid credentials' in response.data,
                        msg="'Invalid credentials' should be in the response")

    def test_fetch_authenticated_user_details(self):
        """log in a user then tests whether the application can fetch
        appropriate user details."""
        with app.test_client() as myapp:
            login_user = myapp.post('/api/v2/auth/login', json=dict(
                           email='sikolia2.wycliffe@gmail.com',
                           password='password'))
            login_user = json.loads(login_user.data.decode("utf-8"))
            token = str(login_user.get("user_token", None))
            response = myapp.get('/api/v2/auth/profile?user_token='+token)
        self.assertEqual(response.status_code, 200,
                         msg='The status code should be 200')
        self.assertTrue(b'message' in response.data,
                        msg="'message' should be in the response")

if __name__ == "__main__":
    unittest.main()

import unittest
# from mydiary import views
from run import app


class TestFunctionality(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.testing = True

    def test_main_page(self):
        '''sends a get request to the home page, extracts the response from
        the request and confrims that the status code from the response is
        200'''
        response = self.app.get('/auth/v2', follow_redirects=True)
        self.assertEqual(response.status_code, 200, msg='''The status code
                                                        should be 200''')
        self.assertTrue(b'Welcome to my home page' in response.data,
                        msg="""'Welcome to my home page' should be in
                        the response""")

    def test_register_new_user(self):
        response = self.app.post('api/v2/auth/v2/signup', data=dict(
                               firstname='firstname',
                               lastname='lastname',
                               email='sikolia2.wycliffe@gmail.com',
                               username='cycks',
                               password='password',
                               password2='password'),
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200, msg='''The status code
                                                        should be 200''')


    def test_register_used_email(self):
        response = self.app.post('api/auth/v2/signup', data=dict(
                               firstname='firstname',
                               lastname='lastname',
                               email='sikolia2.wycliffe@gmail.com',
                               username='cycks',
                               password='password',
                               password2='password'),
                               follow_redirects=True)
        response = self.app.post('api/auth//v2signup', data=dict(
                               firstname='firstname',
                               lastname='lastname',
                               email='sikolia2.wycliffe@gmail.com',
                               username='cycks',
                               password='password',
                               password2='password'),
                               follow_redirects=True)
        response = response.data.decode('utf-8')
        self.assertEqual(response.status_code, 200, msg='''The status code
                                                        should be 200''')

    def test_login_page(self):
        response = self.app.post('api/auth/v2/login', data=dict(
                           email='sikolia21.wycliffe@gmail.com',
                           password='password'), follow_redirects=True)
        self.assertEqual(response.status_code, 200,
                        msg='The status code should be 200')

    def test_login_with_wrong_password(self):
        response = self.app.post('api/auth/v2/login', data=dict(
                           email='sikolia21.wycliffe@gmail.com',
                           password='password2'), follow_redirects=True)
        self.assertEqual(response.status_code, 200,
                        msg='The status code should be 200')

    def test_login_with_wrong_email(self):
        response = self.app.post('api/auth/v2/login', data=dict(
                           email='sikolia21.wycliffe@gmail.com',
                           password='password2'), follow_redirects=True)
        self.assertEqual(response.status_code, 401,
                        msg='The status code should be 401')

    def test_add_entry(self):
        response = self.app.post('api/v2/entries', data=dict(
                               email='sikolia2.wycliffe@gmail.com',
                               entry="Stand up with LFA"),
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200,
                        msg='The status code should be 200')

    def test_get_all_entries(self):
        response = self.app.post('api/v2/entries', data=dict(
                               email = 'sikolia2.wycliffe@gmail.com'),
                               follow_redirects=True)
        self.assertEqual(response.status_code, 200,
                        msg='The status code should be 200')

    def test_get_one_entry(self):
        response = self.app.get('api/v2/entries/<int:3>',
                                follow_redirects = True)
        self.assertEqual(response.status_code, 200, msg='''The status code
                                                       should be 200''')

if __name__ == "__main__":
    unittest.main()
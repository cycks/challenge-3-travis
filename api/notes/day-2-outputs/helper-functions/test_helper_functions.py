import unittest
# from mydiary import views
from run import check_passwords_match, check_user_in_database
from run import check_email_and_username_exist, create_user, create_entry
from run import get_all_diary_entries



class TestHelperFunctions(unittest.TestCase):

    def test_passwords_match(self):
        response = check_passwords_match("password", "password")
        self.assertEqual(response, True,
                         msg="""Should return True for matching passwords""")

    def test_passwords_do_not_match(self):
        response = check_passwords_match("password1", "password")
        self.assertEqual(response, False,
                         msg="Should return False for different passwords")

    def test_check_user_in_database(self):
        response = check_user_in_database("emaily", "passwordy")
        self.assertEqual(response, False,
                         msg="Should return False for a registered user.")

    def test_check_user_not_in_database(self):
        response = check_user_in_database("email", "password")
        self.assertEqual(response, "Invalid credentials.",
                         msg="Should return True for a non-registered user.")

    def test_check_user_wrong_password(self):
        response = check_user_in_database("emaily", "password")
        self.assertEqual(response, "Invalid credentials.",
                         msg="""Should return 'Invalid credentials.' for a
                         non-registered user.""")

    def test_check_user_wrong_email(self):
        response = check_user_in_database("email", "passwordy")
        self.assertEqual(response, "Invalid credentials.",
                         msg="""Should return 'Invalid credentials.' for a
                         non-registered user.""")

    def test_check_email_and_username_does_not_exist(self):
        response = check_email_and_username_exist("emaily", "usernamey")
        self.assertEqual(response, True,
                        msg="""Should return True for an existing, username
                        or email.""")

    def test_check_email_and_username_exist(self):
        response = check_email_and_username_exist("email", "username")
        print("The response is", response)
        self.assertEqual(response, False,
                        msg="""Should return False for an non-existing,
                        username or email.""")

    
if __name__ == "__main__":
    unittest.main()

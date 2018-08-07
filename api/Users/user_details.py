"""This file contains a single class that is used to extract
user details from the post request."""
import jwt
from flask import request


class UserDetails:
    """A class used to extract user dtails from the post request"""
    def __init__(self, details_from_post=None):
        if details_from_post is None:
            self.details_from_post = request.get_json()
        else:
            self.details_from_post = details_from_post

    def get_first_name(self):
        """"Used to extract user's first name"""
        return self.details_from_post.get("first_name", None)

    def get_last_name(self):
        """Used to extract user's last name"""
        return self.details_from_post.get("last_name", None)

    def get_email(self):
        """"Used to extract user's email"""
        return self.details_from_post.get("email", None)

    def get_password(self):
        """Used to extract user's password"""
        return self.details_from_post.get("password", None)

    def get_password2(self):
        """Used to extract user's password2"""
        return self.details_from_post.get("password2", None)

    def get_user_name(self):
        """Used to extract user's username"""
        return self.details_from_post.get("user_name", None)

    def get_user_id(self):
        """Used to extract user's id"""
        try:
            user_id = jwt.decode(request.args.get("user_token"),
                                 "This is not the owner")['user']
            return user_id
        except jwt.exceptions.DecodeError:
            return False

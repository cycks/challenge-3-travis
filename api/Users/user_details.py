from flask import request

class UserDetails():

    def __init__(self, details_from_post = None):
        
        if details_from_post is None:
            self.details_from_post = request.get_json()
        else:
            self.details_from_post = details_from_post
    
    def get_id(self):
        return self.details_from_post.get("id", None)
    
    def get_firstname(self):
        return self.details_from_post.get("firstname", None)

    def get_lastname(self):
        return self.details_from_post.get("lastname", None)

    def get_email(self):
        return self.details_from_post.get("email", None)

    def get_password(self):
        return self.details_from_post.get("password", None)

    def get_password2(self):
        return self.details_from_post.get("password2", None)

    def get_username(self):
        return self.details_from_post.get("username", None)

"""This file contails a class that is used to extract diary contents
from a post request."""
# from datetime import datetime, timedelta

from Users.user_details import UserDetails


class UserEntries(UserDetails):
    """A class used to extract entry details from the post request."""
    def get_title(self):
        """A method used to extract the title from the post request."""
        return self.details_from_post.get("title", None)

    def get_contents(self):
        """A method used to extract the contents of an entry from the
         post request"""
        return self.details_from_post.get("contents", None)

    def get_date_of_event(self):
        """A method used to extract the date of the event from the
         post request"""
        return self.details_from_post.get("date_of_event", None)

    def get_reminder_time(self):
        """A method used to extract the reminder time from the
         post request."""
        return self.details_from_post.get("reminder_time", None)

    # def set_modify(self):
    #     """A method used to set the time to modify an entry."""
    #     return datetime.now() + timedelta(hours=24)

    def combine_entries(self):
        """combines all the entries into a dictionary."""
        check_nulls = {"title": self.get_title(),
                       "contents": self.get_contents(),
                       "date_of_event": self.get_date_of_event(),
                       "reminder_time": self.get_reminder_time(),
                       "user_id": UserDetails.get_user_id(self)}
        return check_nulls

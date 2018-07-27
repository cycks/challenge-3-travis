from flask import Flask

app = Flask(__name__)
app.secret_key = "This is not the owner"

from Users.users import assign_my_users_routes
from Entries.entries import assign_my_entries_routes
from endpoints import sikolia

app.register_blueprint(assign_my_users_routes)
app.register_blueprint(sikolia)
app.register_blueprint(assign_my_entries_routes)
from flask import Flask
# from flask_cors import CORS

from Users.users import assign_my_users_routes
from Entries.entries import assign_my_entries_routes
from endpoints import api_v2

app = Flask(__name__)
app.secret_key = "This is not the owner"


app.register_blueprint(assign_my_users_routes)
app.register_blueprint(api_v2)
app.register_blueprint(assign_my_entries_routes)

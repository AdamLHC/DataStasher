from flask import Flask

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = [
    {
        # uses local development mongodb as default
        "db": "datastasher-dev",
        "host": "localhost",
        "port": 27017,
        "alias": "default",
    }
]
app.config.from_envvar("SECRET_KEY")

from flask_mongoengine import MongoEngine

db = MongoEngine()
db.init_app(app)

from record import RecordApi
from file import FileApi

app.add_url_rule("/record/", view_func=RecordApi.as_view("record_api"))
app.add_url_rule("/file/<string:id>", view_func=FileApi.as_view("file_api"))

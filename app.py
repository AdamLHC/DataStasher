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
app.config.from_prefixed_env()

from flask_mongoengine import MongoEngine

db = MongoEngine()
db.init_app(app)

from record import record_api
from file import FileApi

app.register_blueprint(record_api)
app.add_url_rule("/file/<string:id>", view_func=FileApi.as_view("file_api"))

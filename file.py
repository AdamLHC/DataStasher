from flask import make_response
from flask.views import MethodView
from mongoengine import get_db
from bson.objectid import ObjectId
import gridfs


class FileApi(MethodView):
    def get(self, id):
        db = get_db()
        fs = gridfs.GridFS(db)
        file = fs.get(ObjectId(id))

        response = make_response(file.read())
        response.headers['Content-Type'] = file.content_type

        return response

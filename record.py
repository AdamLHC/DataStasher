import base64
from datetime import datetime
from io import BytesIO

from flask import abort, jsonify, request, send_file, make_response
from flask.views import MethodView
from mongoengine import ValidationError

from auth import auth_required
from data import Record, RecordAttachment


class RecordApi(MethodView):
    def get(self):
        return jsonify(Record.objects)

    @auth_required
    def post(self):
        if not request.is_json:
            abort(415)

        data = request.json

        if not 'title' in data:
            abort(400)

        new_record = Record(
            title=data.get('title'),
            description=data.get('description'),
            upload_date=datetime.now(),
            last_modify=datetime.now())

        for file_base64 in data.get('attachments'):
            file = base64.b64decode(file_base64)
            new_attachment = RecordAttachment()
            new_attachment.file.put(BytesIO(file))
            new_record.attachments.append(new_attachment)

        try:
            new_record.validate()
            new_record.save()
        except ValidationError:
            return make_response(
                jsonify({"message": "Invalid post format."}), 400
            )

        return send_file(BytesIO(file), 'application/jpeg')

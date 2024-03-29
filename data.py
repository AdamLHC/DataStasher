from mongoengine import (
    Document,
    EmbeddedDocument,
    StringField,
    DateTimeField,
    FileField,
    EmbeddedDocumentListField,
)


class RecordAttachment(EmbeddedDocument):
    file = FileField()


class Record(Document):
    title = StringField(Required=True)
    description = StringField()
    author = StringField()
    upload_date = DateTimeField()
    last_modify = DateTimeField()
    attachments = EmbeddedDocumentListField(RecordAttachment)


class User(Document):
    name = StringField(Required=True)
    pass_hash = StringField(Required=True)  # Password hash, NOT password itself.
    role = StringField()

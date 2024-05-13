from mongoengine import (
    connect,
    Document,
    StringField,
    ReferenceField,
    ListField,
    EmailField,
    BooleanField,
    CASCADE,
)


connect(db="goit-python-web-hw8", host="mongodb://localhost:27017")


class Contacts(Document):
    fullname = StringField(requared=True, max_length=50)
    email = EmailField(max_length=50, requared=True)
    is_send = BooleanField(default=False)
    subject = StringField(max_length=100, requared=True)
    text = StringField(requared=True)

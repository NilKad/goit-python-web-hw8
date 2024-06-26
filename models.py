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


class Author(Document):
    fullname = StringField(requared=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    # meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=20))
    quote = StringField()
    # meta = {"collection": "quotes"}


class Contact(Document):
    fullname = StringField(requared=True, max_length=50)
    email = EmailField(max_length=50, requared=True)
    is_send = BooleanField(default=False)
    subject = StringField(max_length=100, requared=True)
    text = StringField(requared=True)

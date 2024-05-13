import json

from mongoengine.errors import NotUniqueError

from models import Author, Quote


def create_author():
    with open("author.json", encoding="utf-8") as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(
                    fullname=el.get("fullname"),
                    born_date=el.get("born_date"),
                    born_location=el.get("born_location"),
                    description=el.get("description"),
                )
                author.save()
            except NotUniqueError as e:
                print(f'Author exist: {el.get("fullname")}')


def create_quote():
    with open("quotes.json", encoding="utf-8") as fd:
        data = json.load(fd)
        for el in data:
            author = Author.objects(fullname=el.get("author")).first()
            quote = Quote(quote=el.get("quote"), tags=el.get("tags"), author=author)
            quote.save()


if __name__ == "__main__":
    create_author()
    create_quote()

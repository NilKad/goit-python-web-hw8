import argparse
import re
import sys
import redis
from redis_lru import RedisLRU

from models import Author, Quote

host = "localhost"
port = 6379

client = redis.Redis(host=host, port=port, password=None)
cache = RedisLRU(client)


def exit_app(args):
    print("exit app")
    sys.exit(0)


@cache
def find_by_tags(tags: list) -> list[str | None]:
    print(f"find by {tags}")
    tags_regex = "|".join(tags)
    q = Quote.objects(tags__iregex=tags_regex)
    result = [quote.quote for quote in q]
    return result


@cache
def find_by_tag(tag: str) -> list[str | None]:
    return find_by_tags([tag])


@cache
def find_by_author(author: list[str]) -> list[str | None]:
    print(f"find by {author}")
    fullname = "|".join(author)
    a = Author.objects(fullname__iregex=fullname)
    q = Quote.objects(author__in=a)  # .only("quote")
    return [e.quote for e in q]


def parser(args_str: str):

    parser = argparse.ArgumentParser(description="Process name.")
    subparser = parser.add_subparsers()

    parser_name = subparser.add_parser("name")
    parser_name.add_argument("args", nargs="+", type=str)
    parser_name.set_defaults(func=find_by_author)

    parser_tag = subparser.add_parser("tag")
    parser_tag.add_argument("args", type=str)
    parser_tag.set_defaults(func=find_by_tag)

    parser_tags = subparser.add_parser("tags")
    parser_tags.add_argument("args", nargs="+", type=str)
    parser_tags.set_defaults(func=find_by_tags)

    parser_exit = subparser.add_parser("exit")
    parser_exit.set_defaults(func=exit_app)

    # args = parser.parse_args(args_str.split())
    args = parser.parse_args(re.split(r":\s*|\s*,\s*|\s+", args_str))

    return args.func(args.args if "args" in args else None)


if __name__ == "__main__":
    # par = "name: Aleksa Kadulin"
    # par = "name: Albert Einstein"
    # par = "name: Albert ".strip()
    # par = "tag: life"
    # par = "tags: life, live"
    # par = "tags: life,live"

    # print(parser(par))

    while True:
        try:
            command_input = input("Enter command: ").strip()
            print(parser(command_input))

        except KeyboardInterrupt:
            print("--------KeyboardInterrupt--------Exception, e:")
            sys.exit()
        except Exception as e:
            print("----------------Exception, e:", type(e))
        except SystemExit as se:
            ...
            # эта ошибка генерится при ошибке ввода - неправильной команде, и тогда цикл прекращается
            # print("--------Systemexit--------Exception", se)
        except:
            print("--------ALL--------Exception")

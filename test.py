import argparse


def fun_name(args_1):
    print("1!!!!")
    print(args_1)


# Создаем парсер аргументов
parser = argparse.ArgumentParser(description="Process name.")

# Добавляем аргумент name
# parser.add_argument("cmd")
subparser = parser.add_subparsers()
parser_name = subparser.add_parser("name:")
parser_name.add_argument("args", nargs="+", type=str)
parser_name.set_defaults(func=fun_name)
parser_tag = subparser.add_parser("tag:")

# parser.add_argument("args", type=str, nargs="+", help="Name to be processed.")

# Парсим аргументы командной строки
# args = parser.parse_args("name: Aleks Kadulin".split())
args = parser.parse_args()
# print(args.func())
args.func(args.args)
# print(args.cmd)
# print(args.args)

# Разделяем строку и берем второй элемент
# name = args.name.split(": ")[1]

# Выводим обработанное имя
# print(f"Name: {name}")

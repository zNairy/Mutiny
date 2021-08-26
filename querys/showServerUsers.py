from sqlite3 import connect
from pprint import pprint

def main():
    with connect('server.db') as database:
        cursor = database.cursor()

        cursor.execute('select codename, identifier from Users')
        pprint(cursor.fetchall())


if __name__ == '__main__':
    main()
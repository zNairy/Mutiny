from sqlite3 import connect
from pprint import pprint

def main():
    with connect('server.db') as database:
        cursor = database.cursor()

        cursor.execute('select userId, codename, identifier from users')
        pprint(cursor.fetchall())


if __name__ == '__main__':
    main()
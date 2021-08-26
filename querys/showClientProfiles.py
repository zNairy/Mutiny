from sqlite3 import connect
from pprint import pprint

def main():
    with connect('client.db') as database:
        cursor = database.cursor()

        cursor.execute('select * from profiles')
        pprint(cursor.fetchall())


if __name__ == '__main__':
    main()
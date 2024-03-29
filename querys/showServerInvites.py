from sqlite3 import connect
from pprint import pprint

def main():
    with connect('server.db') as database:
        cursor = database.cursor()

        cursor.execute("""
            select inviteId, receiver, codename, created, accepted, finished from invites
            join users on invites.sender = users.userId
        """)
        
        pprint(cursor.fetchall())


if __name__ == '__main__':
    main()